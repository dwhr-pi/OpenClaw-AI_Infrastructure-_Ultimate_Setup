"""Offline scope inventory, never installs a package or reads credentials."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import gap_tools
from gap_native_build import specification


def report():
    matrix = json.loads((ROOT / 'config/source_install_readiness.json').read_text(encoding='utf-8'))
    native = json.loads((ROOT / 'config/docker_to_github.json').read_text(encoding='utf-8'))['tools']
    native = {item['id']: item for item in native}
    result = []
    for row in matrix['tools']:
        item = dict(row, installed=False, runtime_tested=False)
        if row['id'] in gap_tools.SPECS:
            spec = specification(row['id'], gap_tools.SPECS[row['id']])
            item.update(source='https://github.com/' + spec['repo'], commit=spec['pin'],
                        reserve_mb=spec['reserve_mb'], mode=spec['mode'])
        elif row['id'] in native and native[row['id']].get('recipe'):
            recipe = native[row['id']]['recipe']
            item.update(source='https://github.com/' + recipe['repo'], commit=recipe['pin'],
                        reserve_mb=recipe['disk_mb'], mode=recipe['kind'])
        result.append(item)
    return dict(schema_version=1, review_date=matrix['review_date'],
                scope='recipe-inventory-not-host-installation-status', tools=result)


if __name__ == '__main__':
    print(json.dumps(report(), indent=2, ensure_ascii=True))
