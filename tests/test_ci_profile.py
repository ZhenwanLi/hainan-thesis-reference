#!/usr/bin/env python3
"""Regression: every writable TeX tree must stay inside the runner root."""
from pathlib import Path
import tempfile
import re
import unittest

from ci_profile import make_profile


TREES = {'TEXDIR', 'TEXMFLOCAL', 'TEXMFSYSVAR', 'TEXMFSYSCONFIG',
         'TEXMFHOME', 'TEXMFVAR', 'TEXMFCONFIG'}


def check_profile(text, root):
    values = dict(line.split(' ', 1) for line in text.splitlines() if line.strip())
    missing = TREES - values.keys()
    if missing:
        raise ValueError('Missing independent writable trees: ' + ', '.join(sorted(missing)))
    for key in TREES:
        path = Path(values[key])
        if not path.is_absolute() or not path.is_relative_to(root):
            raise ValueError(f'{key} is outside the installation root')


class ProfileTest(unittest.TestCase):
    def test_old_partial_profile_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Missing independent writable trees'):
            check_profile('selected_scheme scheme-small\nTEXDIR /runner/texlive\n', Path('/runner/texlive'))

    def test_complete_profile_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='tex profile ') as temp:
            root = Path(temp).resolve() / 'texlive'
            check_profile(make_profile(root), root)
            self.assertIn('instopt_adjustpath 0', make_profile(root))

    def test_global_override_is_rejected(self):
        root = Path('/runner/texlive')
        profile = make_profile(root).replace('TEXMFSYSVAR /runner/texlive/texmf-var',
                                             'TEXMFSYSVAR /usr/local/texlive/2026/texmf-var')
        with self.assertRaisesRegex(ValueError, 'outside the installation root'):
            check_profile(profile, root)

    def test_profile_injection_is_rejected(self):
        with self.assertRaises(ValueError):
            make_profile('/runner/texlive\nTEXDIR /unexpected')

    def test_ci_collections_match_documented_2026_names(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / 'tests/ci_texlive.sh').read_text()
        install = next(line for line in workflow.splitlines() if ' install collection-' in line)
        expected = {'collection-xetex', 'collection-langchinese', 'collection-latexextra',
                    'collection-fontsrecommended', 'collection-bibtexextra',
                    'collection-pictures', 'collection-mathscience'}
        self.assertEqual(set(re.findall(r'collection-[a-z]+', install)), expected)
        documentation = (root / 'docs/BUILD.md').read_text()
        self.assertTrue(expected <= set(re.findall(r'collection-[a-z]+', documentation)))


if __name__ == '__main__':
    unittest.main()
