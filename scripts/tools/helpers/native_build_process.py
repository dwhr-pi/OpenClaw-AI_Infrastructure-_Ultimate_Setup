"""Stream process diagnostics with bounded memory and explicit process status."""
from collections import deque
import os
import signal
import subprocess
import threading
import time


def run(args, cwd, env, timeout=7200, heartbeat=30, label='Build'):
    print('Befehl:', ' '.join(map(str, args)), flush=True)
    process = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, errors='replace', start_new_session=os.name == 'posix')
    print(label + 'prozess gestartet; PID:', process.pid, flush=True)
    tail = deque(maxlen=256)
    errors = []

    def read():
        try:
            for chunk in iter(lambda: process.stdout.readline(4096), ''):
                tail.append(chunk)
                print(chunk, end='', flush=True)
        except Exception as error:
            errors.append(error)

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    deadline = None if timeout is None else time.monotonic() + timeout
    started = time.monotonic()
    try:
        while True:
            remaining = None if deadline is None else deadline - time.monotonic()
            if remaining is not None and remaining <= 0:
                raise subprocess.TimeoutExpired(args, timeout)
            try:
                code = process.wait(timeout=heartbeat if remaining is None else min(heartbeat, remaining))
                break
            except subprocess.TimeoutExpired:
                budget = ('kein automatisches Zeitlimit' if deadline is None else
                          'Restbudget: ' + str(max(0, round(deadline - time.monotonic()))) + ' s')
                print(label + ' laeuft; PID:', process.pid, 'Dauer:', round(time.monotonic() - started),
                      's;', budget,
                      '(Prozess noch nicht beendet, kein Fortschritts-/Erfolgsnachweis).', flush=True)
        reader.join(timeout=5)
        if reader.is_alive() or errors:
            raise OSError('Build-Ausgabe nicht vollstaendig lesbar; kein Erfolgsnachweis.')
        print(label + 'prozess beendet; PID:', process.pid, 'Exit:', code, flush=True)
        if code < 0:
            print(label + ' durch Signal beendet:', -code,
                  '; SIGKILL kann OOM bedeuten, ist aber kein OOM-Nachweis. Kernel-/WSL-Logs pruefen.', flush=True)
        if code:
            raise subprocess.CalledProcessError(code, args, output=''.join(tail))
        return ''.join(tail).strip()
    except BaseException as error:
        if process.poll() is None or reader.is_alive():
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                if process.poll() is None:
                    process.kill()
            process.wait()
        if isinstance(error, subprocess.TimeoutExpired):
            error.output = ''.join(tail)
            print('Zeitlimit erreicht:', timeout, 'Sekunden. Teil-Ausgabe steht im aktuellen Log;'
                  ' Ursache (langsamer Prozess/Netzwerk/Haenger) daraus pruefen, kein OOM-Nachweis.', flush=True)
        print(label + ' abgebrochen; PID:', process.pid, 'Exit:', process.returncode,
              '(Timeout/Signal/Fehler; kein Erfolgsnachweis).', flush=True)
        raise
    finally:
        reader.join(timeout=5)
        if not reader.is_alive():
            process.stdout.close()
