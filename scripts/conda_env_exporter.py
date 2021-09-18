#!/usr/bin/env python
"""
Export a Conda environment with --from-history, but also append
Pip-installed dependencies
Exports only manually-installed dependencies, excluding build versions, but
including Pip-installed dependencies.
Lots of issues requesting this functionality in the Conda issue tracker, no
sign of progress (as of March 2020).
TODO (?): support command-line flags -n and -p
"""
import re
import os
import subprocess
from functools import cmp_to_key

import ruamel.yaml


yaml = ruamel.yaml.YAML()


def export_env(history_only=False, include_builds=False):
    """ Capture `conda env export` output """
    cmd = ['conda', 'env', 'export']
    if history_only:
        cmd.append('--from-history')
        if include_builds:
            raise ValueError('Cannot include build versions with "from history" mode')
    if not include_builds:
        cmd.append('--no-builds')
    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except Exception:
        raise
    else:
        return yaml.load(cp.stdout)


def _is_history_dep(d, history_deps):
    if not isinstance(d, str):
        return False
    d_prefix = re.sub(r'=.*', '', d)
    return d_prefix in history_deps or d_prefix == 'python' or d_prefix == 'pip'


def _filter_pip_deps(dep):
    pkgs_to_remove = (
        'backports',
        'blinker',
        'cfgv',
        'click',
        'distlib',
        'filelock',
        'greenlet',
        'h11',
        'h2',
        'hpack',
        'hypercorn',
        'hyperframe',
        'identify',
        'importlib-resources',
        'itsdangerous',
        'jinja2',
        'mako',
        'markupsafe',
        'nodeenv',
        'platformdirs',
        'priority',
        'pyyaml',
        'ruamel-yaml-clib',
        'six',
        'toml',
        'virtualenv',
        'werkzeug',
        'wsproto',
        'zipp',
    )
    return not dep.startswith(pkgs_to_remove)


def _remove_pip_version(dep):
    pkgs_to_strip = (
        'psycopg2',
    )
    if dep.startswith(pkgs_to_strip):
        return dep.split("==")[0]
    else:
        return dep


def _clean_pip_deps(deps):
    filtered = [dep for dep in deps if _filter_pip_deps(dep)]
    return [_remove_pip_version(dep) for dep in filtered]


def _get_pip_deps(full_deps):
    for dep in full_deps:
        if isinstance(dep, dict) and 'pip' in dep:
            return _clean_pip_deps(dep['pip'])
    return []


def _clean_dep(dep):
    if 'python=' not in dep and 'pip=' not in dep:
        return dep.split('=')[0]
    if 'python=' in dep:
        return ".".join(dep.split('.')[0:2])
    return dep


def _sort_deps(i1, i2):
    # print(f"check {i1}  {i2}")
    if isinstance(i1, dict):
        return False
    if i1.startswith('python=') or i1.startswith('pip='):
        if i1.startswith('pip='):
            return 0 if isinstance(i2, str) and i2.startswith('python=') else -1
        else:
            # print(-1)
            return -1
    if i2.startswith('python=') or i2.startswith('pip='):
        if i2.startswith('pip='):
            return -1 if isinstance(i1, str) and i1.startswith('python=') else 0
        else:
            # print(0)
            return 0
    # print('std chk')
    # print(False if isinstance(i2, dict) else i2 > i1)
    return False if isinstance(i2, dict) else i2 > i1


def _combine_env_data(env_data_full, env_data_hist, old_env):
    old_git_deps = []
    old_prefix = None
    if old_env is not None:
        old_prefix = old_env.get('prefix')
        old_pip_deps = _get_pip_deps(old_env.get('dependencies', []))
        old_git_deps = [dep for dep in old_pip_deps if 'git+git' in dep]
    deps_full = env_data_full['dependencies']
    deps_hist = env_data_hist['dependencies']
    deps = sorted([_clean_dep(dep) for dep in deps_full if _is_history_dep(dep, deps_hist)], key=cmp_to_key(_sort_deps))

    pip_deps = _get_pip_deps(deps_full)
    pip_deps.extend(old_git_deps)

    env_data = {}
    env_data['name'] = 'rogerthat'
    env_data['channels'] = env_data_full['channels']
    env_data['dependencies'] = deps
    env_data['dependencies'].append({'pip': pip_deps})
    if old_prefix is not None:
        env_data['prefix'] = old_prefix

    return env_data


def main():
    print('\n\nStarting.\n\n')
    env_data_full = export_env()
    env_data_hist = export_env(history_only=True)
    old_env = None
    if os.path.exists('support/environment.yml'):
        with open('support/environment.yml', 'r') as fp:
            old_env = yaml.load(fp)
    env_data = _combine_env_data(env_data_full, env_data_hist, old_env)
    yaml.indent(sequence=2, offset=2)
    with open('support/environment.yml', 'w') as fp:
        yaml.dump(env_data, fp)
    print('\n\nDone.\n\n')


if __name__ == '__main__':
    main()
