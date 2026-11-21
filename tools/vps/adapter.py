"""Explicitly authorized GCP inspection and dedicated-host configuration; no cloud purchases."""
from contextlib import contextmanager
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import base64
import hashlib
import hmac
import ipaddress
import json
import math
import multiprocessing
import os
from pathlib import Path
import re
import shlex
import signal
import stat
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
MAX_BYTES = 1024 * 1024
ACTIONS = {'status', 'verify', 'configure', 'provision'}
USAGES = {'monitoring', 'ai_client', 'ai_inference', 'ai_training', 'mining',
          'crypto_node', 'validator', 'private_trading', 'public_trading', 'commercial'}
FIELDS = {'version', 'provider', 'account_ref', 'region', 'zone', 'resource_name', 'resource_id',
          'sku', 'os_image', 'architecture', 'usage', 'offer_id', 'owner', 'pricing', 'budget',
          'review', 'ssh', 'dedicated_host', 'service_public_key', 'bootstrap_sha256'}


class Guard(ValueError):
    """Messages are fixed codes, never provider bodies, paths or credential values."""


def strict_json(raw):
    def finite(value):
        number = float(value)
        if not math.isfinite(number):
            raise Guard('nonfinite_json')
        return number

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Guard('duplicate_json_field')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite,
                      parse_constant=lambda _: (_ for _ in ()).throw(Guard('nonfinite_json')))


def read_json(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise Guard('invalid_json_file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise Guard('invalid_json_file')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise Guard('invalid_json_file')
        return strict_json(raw)
    finally:
        os.close(descriptor)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=True).encode()).hexdigest()


def exact(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise Guard('unexpected_or_missing_fields')


def pattern(value, expression):
    if not isinstance(value, str) or re.fullmatch(expression, value) is None:
        raise Guard('invalid_identifier')
    return value


def money(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{1,8}(?:\.[0-9]{1,6})?', value):
        raise Guard('price_unknown_or_invalid')
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise Guard('price_unknown_or_invalid') from error
    if not result.is_finite() or result < 0:
        raise Guard('price_unknown_or_invalid')
    return result


def recent(value, now):
    try:
        checked = date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise Guard('invalid_review_date') from error
    if not 0 <= (now.date() - checked).days <= 7:
        raise Guard('review_stale_or_future')


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (AttributeError, ValueError) as error:
        raise Guard('invalid_timestamp') from error
    if result.tzinfo is None:
        raise Guard('timezone_required')
    return result


def hostkey_fingerprint(key):
    if not isinstance(key, str):
        raise Guard('ed25519_public_key_required')
    parts = key.split()
    if len(parts) != 2 or parts[0] != 'ssh-ed25519':
        raise Guard('ed25519_public_key_required')
    try:
        raw = base64.b64decode(parts[1], validate=True)
    except ValueError as error:
        raise Guard('invalid_public_key') from error
    prefix = b'\x00\x00\x00\x0bssh-ed25519\x00\x00\x00\x20'
    if not raw.startswith(prefix) or len(raw) != len(prefix) + 32:
        raise Guard('invalid_public_key')
    return 'SHA256:' + base64.b64encode(hashlib.sha256(raw).digest()).decode().rstrip('=')


def validate(plan, offer, now=None):
    now = now or datetime.now(timezone.utc)
    exact(plan, FIELDS)
    if type(plan['version']) is not int or plan['version'] != 1:
        raise Guard('unsupported_plan_version')
    if plan['provider'] != 'gcp':
        raise Guard('provider_adapter_not_reviewed')
    if plan['offer_id'] != offer['id'] or plan['provider'] != offer['id'] or offer['kind'] != 'vm':
        raise Guard('offer_not_verified_vm_or_provider_mismatch')
    pattern(plan['account_ref'], r'[a-z][a-z0-9-]{4,28}[a-z0-9]')
    pattern(plan['region'], r'[a-z]+-[a-z]+[0-9]')
    pattern(plan['zone'], re.escape(plan['region']) + r'-[a-z]')
    pattern(plan['resource_name'], r'[a-z][a-z0-9-]{0,61}[a-z0-9]')
    pattern(plan['resource_id'], r'[0-9]{1,24}')
    pattern(plan['owner'], r'[a-z][a-z0-9-]{0,61}[a-z0-9]')
    pattern(plan['sku'], r'[a-z][a-z0-9-]{1,60}')
    pattern(plan['os_image'], r'projects/[a-z0-9-]+/global/images/[a-z0-9-]+')
    if plan['architecture'] not in {'x86_64', 'arm64'} or plan['usage'] not in USAGES:
        raise Guard('unsupported_architecture_or_usage')
    if type(plan['dedicated_host']) is not bool:
        raise Guard('dedicated_host_boolean_required')
    pattern(plan['bootstrap_sha256'], r'[a-f0-9]{64}')
    exact(plan['pricing'], {'currency', 'hourly', 'setup', 'extras', 'tax', 'reviewed_on', 'source_url'})
    price = plan['pricing']
    if price['currency'] not in {'EUR', 'USD'}:
        raise Guard('currency_not_reviewed')
    for field in ('hourly', 'setup', 'extras', 'tax'):
        money(price[field])
    if not isinstance(price['source_url'], str) or not price['source_url'].startswith('https://'):
        raise Guard('price_source_required')
    recent(price['reviewed_on'], now)
    exact(plan['budget'], {'amount', 'hours'})
    hours = plan['budget']['hours']
    if type(hours) is not int or not 1 <= hours <= 168:
        raise Guard('bounded_runtime_required')
    estimated = money(price['hourly']) * hours + sum(money(price[f]) for f in ('setup', 'extras', 'tax'))
    if estimated > money(plan['budget']['amount']):
        raise Guard('planned_cost_exceeds_authorized_budget')
    exact(plan['review'], {'usage_state', 'source_url', 'reviewed_on', 'account_state'})
    if plan['review']['usage_state'] not in {'allowed', 'forbidden', 'unverified'}:
        raise Guard('invalid_usage_review')
    if plan['review']['account_state'] not in {'existing_account_required', 'human_action_required',
                                               'terms_unclear', 'unavailable', 'unsupported'}:
        raise Guard('invalid_account_state')
    if not isinstance(plan['review']['source_url'], str) or not plan['review']['source_url'].startswith('https://'):
        raise Guard('usage_source_required')
    recent(plan['review']['reviewed_on'], now)
    exact(plan['ssh'], {'host', 'port', 'user', 'recovery_user', 'key_env', 'recovery_key_env',
                        'known_hosts_env', 'host_fingerprint', 'api_token_env'})
    ssh = plan['ssh']
    try:
        ipaddress.ip_address(ssh['host'])
    except (TypeError, ValueError) as error:
        raise Guard('literal_host_ip_required') from error
    if type(ssh['port']) is not int or ssh['port'] != 22:
        raise Guard('bootstrap_port_22_required')
    for field in ('user', 'recovery_user'):
        pattern(ssh[field], r'[a-z_][a-z0-9_-]{0,30}')
    for field in ('key_env', 'recovery_key_env', 'known_hosts_env', 'api_token_env'):
        pattern(ssh[field], r'OPENCLAW_VPS_[A-Z0-9_]{1,64}')
    if ssh['key_env'] == ssh['recovery_key_env'] or ssh['user'] == ssh['recovery_user']:
        raise Guard('independent_recovery_identity_required')
    pattern(ssh['host_fingerprint'], r'SHA256:[A-Za-z0-9+/]{43}')
    hostkey_fingerprint(plan['service_public_key'])
    return {'plan_hash': digest(plan), 'estimated_total': str(estimated),
            'registration': 'human_action_required', 'execution': 'explicit_authorization_required',
            'provision': 'blocked_no_hard_compute_cost_and_lifetime_enforcement',
            'usage_ready': plan['review']['usage_state'] == 'allowed'}


def protected(path, *, outside_repo=False):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or path == Path(path.anchor):
        raise Guard('absolute_normalized_path_required')
    for part in (path, *path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise Guard('linked_path_not_allowed')
    if outside_repo and (path == ROOT or ROOT in path.parents):
        raise Guard('external_private_path_required')
    return path


def authorize(plan, authorization, action, now=None):
    now = now or datetime.now(timezone.utc)
    exact(authorization, {'version', 'plan_hash', 'actions', 'valid_from', 'expires_at',
                          'budget_amount', 'max_hours', 'max_resources'})
    if type(authorization['version']) is not int or authorization['version'] != 1 or authorization['plan_hash'] != digest(plan):
        raise Guard('authorization_plan_mismatch')
    actions = authorization['actions']
    if not isinstance(actions, list) or not actions or any(not isinstance(a, str) or a not in ACTIONS for a in actions) or action not in actions:
        raise Guard('authorization_scope_missing')
    start, end = timestamp(authorization['valid_from']), timestamp(authorization['expires_at'])
    if not start <= now < end or not 0 < (end - start).total_seconds() <= 7 * 86400:
        raise Guard('authorization_expired_or_unbounded')
    if (type(authorization['max_resources']) is not int or authorization['max_resources'] != 1
            or type(authorization['max_hours']) is not int
            or authorization['max_hours'] != plan['budget']['hours']
            or money(authorization['budget_amount']) != money(plan['budget']['amount'])):
        raise Guard('authorization_budget_mismatch')


def _http_worker(url, token, pipe):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            raise Guard('http_redirect_blocked')
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        request = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token})
        with opener.open(request, timeout=10) as response:
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise Guard('provider_response_too_large')
            pipe.send((200, strict_json(raw)))
    except urllib.error.HTTPError as error:
        pipe.send((error.code, None))
    except Exception:
        pipe.send((0, None))
    finally:
        pipe.close()


def http_get(url, token, timeout):
    # DNS and TLS stay in our bounded child; no provider body or token is logged.
    context = multiprocessing.get_context('spawn')
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_http_worker, args=(url, token, sender), daemon=True)
    try:
        process.start()
        sender.close()
        if not receiver.poll(timeout):
            raise Guard('provider_timeout')
        return receiver.recv()
    finally:
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
            process.join(timeout=2)
            if process.is_alive():
                process.kill()
                process.join(timeout=2)
        sender.close()
        receiver.close()


class GcpAdapter:
    def __init__(self, transport=http_get, sleep=time.sleep, clock=time.monotonic):
        self.transport, self.sleep, self.clock = transport, sleep, clock

    def status(self, plan, token):
        if not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9._~+/=-]{1,8192}', token):
            raise Guard('credential_reference_unavailable')
        url = ('https://compute.googleapis.com/compute/v1/projects/' + plan['account_ref']
               + '/zones/' + plan['zone'] + '/instances/' + plan['resource_name'])
        deadline = self.clock() + 30
        for attempt in range(2):
            remaining = deadline - self.clock()
            if remaining <= 0:
                raise Guard('provider_timeout')
            try:
                code, data = self.transport(url, token, min(12, remaining))
            except (TimeoutError, Guard):
                code, data = 0, None
            if code == 200:
                if not isinstance(data, dict) or str(data.get('id')) != plan['resource_id']:
                    raise Guard('resource_identity_mismatch')
                labels = data.get('labels', {})
                if (not isinstance(labels, dict) or labels.get('openclaw-owner') != plan['owner']
                        or labels.get('openclaw-plan') != digest(plan)[:32]):
                    raise Guard('resource_ownership_unproven')
                if data.get('name') != plan['resource_name'] or data.get('zone', '').rsplit('/', 1)[-1] != plan['zone']:
                    raise Guard('resource_location_mismatch')
                if data.get('machineType', '').rsplit('/', 1)[-1] != plan['sku']:
                    raise Guard('resource_sku_mismatch')
                return data
            if code not in (0, 429, 500, 502, 503, 504) or attempt:
                raise Guard('provider_status_failed_' + str(code))
            self.sleep(min(1, max(0, deadline - self.clock())))
        raise Guard('provider_status_failed')


def limited_run(command, *, timeout=30, env=None):
    output, overflow = bytearray(), []
    child_env = {k: v for k, v in os.environ.items() if k in ('PATH', 'SYSTEMROOT', 'TEMP', 'TMP')}
    child_env.update(LANG='C', LC_ALL='C', ANSIBLE_HOST_KEY_CHECKING='True',
                     ANSIBLE_CONFIG=os.devnull, ANSIBLE_SSH_ARGS='-o ControlMaster=no -o ControlPersist=no',
                     ANSIBLE_NOCOLOR='1', ANSIBLE_STDOUT_CALLBACK='ansible.posix.json')
    if env:
        child_env.update(env)
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, env=child_env, start_new_session=os.name == 'posix')

    def read():
        try:
            while chunk := process.stdout.read(4096):
                if len(output) + len(chunk) > MAX_BYTES:
                    overflow.append(True)
                    break
                output.extend(chunk)
        except OSError:
            overflow.append(True)

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    deadline = time.monotonic() + timeout
    try:
        while process.poll() is None:
            if overflow or time.monotonic() >= deadline:
                raise Guard('process_output_or_time_limit')
            time.sleep(0.05)
        reader.join(timeout=2)
        if reader.is_alive() or overflow or process.returncode:
            raise Guard('bounded_process_failed')
        return bytes(output)
    finally:
        if process.poll() is None or reader.is_alive():
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            elif process.poll() is None:
                process.kill()
            process.wait(timeout=3)
        reader.join(timeout=2)
        if not reader.is_alive():
            process.stdout.close()


def external_reference(name):
    value = os.environ.get(name)
    if not value:
        raise Guard('external_reference_missing')
    path = protected(value, outside_repo=True)
    if not path.is_file():
        raise Guard('external_reference_missing')
    return path


def check_known_hosts(plan, path):
    ssh = plan['ssh']
    if path.stat().st_size > MAX_BYTES:
        raise Guard('host_key_file_too_large')
    lines = path.read_text(encoding='utf-8').splitlines()
    expected = ssh['host']
    found = []
    for line in lines:
        parts = line.split()
        if not parts or parts[0].startswith('#'):
            continue
        # SSH must not also accept a wildcard/CA/second key ignored by our pin check.
        if len(parts) != 3 or parts[0] != expected:
            raise Guard('host_key_file_must_contain_only_exact_pin')
        found.append(' '.join(parts[1:3]))
    if len(found) != 1 or not hmac.compare_digest(hostkey_fingerprint(found[0]), ssh['host_fingerprint']):
        raise Guard('host_key_pin_mismatch')


FACTS = ('import json,os,platform,shutil,pwd; '
         'print(json.dumps(dict(system=platform.system(),architecture=platform.machine(),'
         'cpu=os.cpu_count(),free_disk=shutil.disk_usage("/").free,'
         'memory_pages=os.sysconf("SC_PHYS_PAGES"),page_size=os.sysconf("SC_PAGE_SIZE"),'
         'os_release=platform.freedesktop_os_release(),'
         'existing_llmops=any(p.pw_name=="llmops" for p in pwd.getpwall()),'
         'cgroups=os.path.exists("/sys/fs/cgroup/cgroup.controllers"),'
         'tun=os.access("/dev/net/tun",os.R_OK|os.W_OK),'
         'kernel_scope="metadata_only",uid=os.getuid())))')


def verify_ssh(plan, data, run=limited_run):
    addresses = set()
    for interface in data.get('networkInterfaces', []):
        addresses.update([interface.get('networkIP'), interface.get('ipv6Address')])
        addresses.update(access.get('natIP') for access in interface.get('accessConfigs', []))
    if plan['ssh']['host'] not in addresses:
        raise Guard('host_not_bound_to_provider_resource')
    known = external_reference(plan['ssh']['known_hosts_env'])
    check_known_hosts(plan, known)
    facts = []
    primary_key = external_reference(plan['ssh']['key_env'])
    recovery_key = external_reference(plan['ssh']['recovery_key_env'])
    if primary_key.samefile(recovery_key):
        raise Guard('independent_recovery_key_files_required')
    for user_field, key_field in (('user', 'key_env'), ('recovery_user', 'recovery_key_env')):
        key = external_reference(plan['ssh'][key_field])
        args = ['ssh', '-F', os.devnull, '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10',
                '-o', 'StrictHostKeyChecking=yes', '-o', 'GlobalKnownHostsFile=' + os.devnull,
                '-o', 'UserKnownHostsFile=' + str(known), '-o', 'IdentitiesOnly=yes',
                '-o', 'IdentityAgent=none', '-i', str(key), '-p', '22',
                plan['ssh'][user_field] + '@' + plan['ssh']['host'],
                'python3 -I -B -c ' + shlex.quote(FACTS)]
        result = strict_json(run(args, timeout=30))
        if (not isinstance(result, dict) or result.get('system') != 'Linux'
                or result.get('architecture') not in {'x86_64', 'aarch64'}):
            raise Guard('remote_platform_not_reviewed')
        expected_arch = 'aarch64' if plan['architecture'] == 'arm64' else 'x86_64'
        if result['architecture'] != expected_arch:
            raise Guard('remote_architecture_mismatch')
        facts.append(result)
    return {'ssh_verified': True, 'recovery_verified': True, 'facts': facts[0],
            'k3s_join_allowed': False, 'kernel_runtime_tested': False}


@contextmanager
def journal(root, plan):
    root = protected(root, outside_repo=True)
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == 'posix' and (root.stat().st_uid != os.getuid() or root.stat().st_mode & 0o077):
        raise Guard('private_state_permissions_required')
    lock = protected(root / (digest(plan) + '.lock'))
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError as error:
        raise Guard('operation_already_active_or_needs_review') from error
    try:
        yield root / (digest(plan) + '.json')
    finally:
        lock.rmdir()


def configure(plan, state_root, ssh_result, run=limited_run, post_verify=None):
    if not plan['dedicated_host'] or not ssh_result.get('recovery_verified'):
        raise Guard('dedicated_host_and_recovery_required')
    playbook = ROOT / 'ansible/vps_bootstrap.yml'
    if hashlib.sha256(playbook.read_bytes()).hexdigest() != plan['bootstrap_sha256']:
        raise Guard('bootstrap_source_changed_since_authorization')
    with journal(state_root, plan) as state:
        if state.exists():
            protected(state)
            record = read_json(state)
            if record != {'plan_hash': digest(plan), 'phase': 'configured'}:
                raise Guard('prior_incomplete_operation_requires_review')
            apply = False
        else:
            if ssh_result.get('facts', {}).get('existing_llmops') is not False:
                raise Guard('existing_service_account_requires_separate_migration')
            with state.open('x', encoding='utf-8') as stream:
                json.dump({'plan_hash': digest(plan), 'phase': 'intent'}, stream)
            state.chmod(0o600)
            apply = True
        key = external_reference(plan['ssh']['key_env'])
        known = external_reference(plan['ssh']['known_hosts_env'])
        with tempfile.TemporaryDirectory(prefix='bootstrap-', dir=state.parent) as temporary:
            inventory = Path(temporary) / 'inventory.json'
            variables = Path(temporary) / 'vars.json'
            common = shlex.join(['-F', os.devnull, '-o', 'StrictHostKeyChecking=yes',
                                 '-o', 'GlobalKnownHostsFile=' + os.devnull,
                                 '-o', 'UserKnownHostsFile=' + str(known), '-o', 'IdentityAgent=none',
                                 '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes',
                                 '-o', 'ControlMaster=no', '-o', 'ControlPersist=no'])
            inventory.write_text(json.dumps({'all': {'children': {'vps': {'hosts': {'target': {
                'ansible_host': plan['ssh']['host'], 'ansible_user': plan['ssh']['user'],
                'ansible_port': 22, 'ansible_ssh_private_key_file': str(key),
                'ansible_ssh_common_args': common}}}}}}), encoding='utf-8')
            variables.write_text(json.dumps({'bootstrap_key_access_confirmed': True,
                                             'bootstrap_dedicated_host_confirmed': True,
                                             'llmops_ssh_public_key': plan['service_public_key']}), encoding='utf-8')
            command = ['ansible-playbook', '-i', str(inventory), str(ROOT / 'ansible/vps_bootstrap.yml'),
                       '--extra-vars', '@' + str(variables)]

            def check():
                result = strict_json(run(command + ['--check'], timeout=900))
                stats = result.get('stats', {}).get('target', {})
                if not stats or stats.get('failures') != 0 or stats.get('unreachable') != 0:
                    raise Guard('ansible_check_not_verified')
                return stats

            check()
            if apply:
                result = strict_json(run(command, timeout=900))
                stats = result.get('stats', {}).get('target', {})
                if not stats or stats.get('failures') != 0 or stats.get('unreachable') != 0:
                    raise Guard('ansible_apply_not_verified')
            if check().get('changed') != 0:
                raise Guard('ansible_idempotence_not_verified')
            if post_verify is None or not post_verify().get('recovery_verified'):
                raise Guard('post_configuration_recovery_not_verified')
        replacement = state.with_suffix('.next')
        with replacement.open('x', encoding='utf-8') as stream:
            json.dump({'plan_hash': digest(plan), 'phase': 'configured'}, stream)
        replacement.chmod(0o600)
        os.replace(replacement, state)
    return {'configured': True, 'idempotence_check_passed': True, 'model_or_cluster_start_requested': False,
            'host_services_may_change': True,
            'ssh_reloaded_by_bootstrap_if_changed': True, 'k3s_join_allowed': False}


def execute(action, plan, offer, authorization=None, *, apply=False, state_root=None,
            provider=None, run=limited_run, now=None):
    decision = validate(plan, offer, now)
    if action in {'plan', 'validate'}:
        return decision
    if action == 'teardown':
        if apply:
            raise Guard('destructive_teardown_not_implemented')
        return {'preview_only': True, 'deleted': False, 'ownership_verified': False,
                'resource_id': plan['resource_id'], 'plan_hash': decision['plan_hash']}
    if action not in ACTIONS:
        raise Guard('unknown_action')
    if not apply:
        return {'executed': False, 'authorization_required': True, **decision}
    if not authorization:
        raise Guard('operator_authorization_required')
    authorize(plan, authorization, action, now)
    if action == 'provision':
        # Estimates and alert budgets cannot enforce VM cost or lifetime ceilings.
        raise Guard('provision_blocked_no_hard_cost_and_lifetime_enforcement')
    if plan['provider'] != 'gcp':
        raise Guard('live_adapter_not_implemented_for_provider')
    if plan['review']['account_state'] != 'existing_account_required':
        raise Guard('human_account_or_terms_verification_required')
    if action == 'configure' and (not decision['usage_ready'] or not plan['dedicated_host']):
        raise Guard('usage_terms_or_dedicated_host_unconfirmed')
    adapter = provider or GcpAdapter()
    token = os.environ.get(plan['ssh']['api_token_env'])
    data = adapter.status(plan, token)
    if action == 'status':
        return {'resource_verified': True, 'ownership_verified': True, 'plan_hash': digest(plan),
                'state': data.get('status') if data.get('status') in {'RUNNING', 'TERMINATED', 'STOPPED'} else 'other'}
    verified = verify_ssh(plan, data, run)
    if action == 'verify':
        return verified
    if state_root is None:
        raise Guard('external_state_directory_required')
    if os.name != 'posix':
        raise Guard('live_configuration_requires_posix_controller')
    return configure(plan, state_root, verified, run, post_verify=lambda: verify_ssh(plan, data, run))
