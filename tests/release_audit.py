#!/usr/bin/env python3
"""Audit publishable files only; ignored build outputs stay local."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {'.md', '.tex', '.cls', '.bib', '.bst', '.sh', '.py', '.txt', '.yml', '.yaml'}
REQUIRED = ['README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'CONTRIBUTING.md', '.gitignore',
            'LICENSES/LPPL-1.3c.txt', 'sources/README.md', 'docs/BUILD.md', 'docs/RELEASE.md']


def ignored(path):
    return any(part in {'.git', '.build', 'reports', '__pycache__'} for part in path.parts) or path.suffix == '.pdf'


def main():
    errors, manifest = [], []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f'Missing required file: {name}')
    patterns = {
        'absolute personal path': r'/home/[A-Za-z0-9_.-]+/',
        'platform-only temp path': '/' + 'tmp/' + 'opencode',
        'private key header': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'GitHub token shape': r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
        'unversioned bibliography style': r'\\bibliographystyle\{gbt7714-numeric\}',
    }
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if ignored(relative):
            continue
        if path.is_symlink():
            errors.append(f'Symlink not allowed in release: {relative}')
            continue
        if not path.is_file():
            continue
        if path.suffix not in ALLOWED_SUFFIXES and relative.as_posix() not in {'LICENSE', '.gitignore'}:
            errors.append(f'Unapproved file type: {relative}')
            continue
        text = path.read_text(encoding='utf-8')
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                errors.append(f'{label}: {relative}')
        # Only local relative Markdown targets, no external URL crawling.
        if path.suffix == '.md':
            for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text):
                if target.startswith(('http:', 'https:', '#', 'mailto:')):
                    continue
                if not (path.parent / target.split('#', 1)[0]).exists():
                    errors.append(f'Broken local link: {relative}: {target}')
        manifest.append(dict(path=relative.as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    bst = ROOT / 'templates/海口经济学院/hkcu-gbt7714.bst'
    if bst.exists() and not all(term in bst.read_text()[:2500] for term in ['LaTeX Project Public License', 'Zeping Lee', 'hkcu-gbt7714']):
        errors.append('Local bst missing upstream attribution/license/renamed identity')
    report = ROOT / 'reports'
    report.mkdir(exist_ok=True)
    (report / 'release-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    for error in errors:
        print('FAIL', error)
    print(f'{"FAIL" if errors else "PASS"} release file audit: {len(manifest)} files')
    print('This is a limited mechanical scan, not a legal or complete privacy review.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
