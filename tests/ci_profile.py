#!/usr/bin/env python3
"""Write a complete non-root TeX Live profile; paths are independent keys."""
from pathlib import Path
import sys


def make_profile(root):
    root = Path(root).resolve()
    if any(char in str(root) for char in '\r\n'):
        raise ValueError('Installation root must be a single line')
    trees = {
        'TEXDIR': root,
        'TEXMFLOCAL': root / 'texmf-local',
        'TEXMFSYSVAR': root / 'texmf-var',
        'TEXMFSYSCONFIG': root / 'texmf-config',
        'TEXMFHOME': root / 'user/texmf',
        'TEXMFVAR': root / 'user/texmf-var',
        'TEXMFCONFIG': root / 'user/texmf-config',
    }
    return '\n'.join([
        'selected_scheme scheme-small',
        *(f'{key} {value}' for key, value in trees.items()),
        'tlpdbopt_install_docfiles 0',
        'tlpdbopt_install_srcfiles 0',
        'instopt_adjustpath 0',
        '',
    ])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 tests/ci_profile.py INSTALL_ROOT')
    print(make_profile(sys.argv[1]), end='')
