#!/usr/bin/env python3
"""Exercise the real CI shell entry with offline failing/successful tools."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MirrorTest(unittest.TestCase):
    def run_installer(self, mode):
        with tempfile.TemporaryDirectory(prefix='ci mirrors ') as temp:
            temp = Path(temp)
            tools = temp / 'tools'
            tools.mkdir()
            scripts = {
                'curl': 'if [[ "$MODE" == download-fail ]] && [[ "$*" == *illinois* ]]; then exit 22; fi\nexit 0\n',
                'tar': 'exit 0\n',
                'timeout': 'printf "%s\\n" "$*" >> "$RUNNER_TEMP/timeouts"\nshift 2\nexec "$@"\n',
                'perl': '''
printf '%s\\n' "$*" >> "$RUNNER_TEMP/attempts"
if [[ "$MODE" == all-fail ]] || { [[ "$MODE" == install-fail ]] && [[ "$*" == *illinois* ]]; }; then exit 1; fi
profile="$3"
root="$(sed -n 's/^TEXDIR //p' "$profile")"
mkdir -p "$root/bin/x86_64-linux"
for tool in tlmgr kpsewhich; do
  cp "$FAKE_TOOLS/$tool" "$root/bin/x86_64-linux/$tool"
done
''',
                'tlmgr': '''
if [[ "$1" == --version ]]; then
  if [[ "$MODE" == wrong-version ]]; then echo 'TeX Live version 2027'; else echo 'TeX Live version 2026'; fi
  exit 0
fi
printf '%s\\n' "$*" >> "$RUNNER_TEMP/collections"
if [[ "$MODE" == collections-fail ]] && [[ "$*" == *illinois* ]]; then exit 1; fi
exit 0
''',
                'kpsewhich': '''
root="$(dirname "$(dirname "$(dirname "$0")")")"
if [[ "$MODE" == escape ]]; then echo /outside/texmf; else echo "$root/texmf-test"; fi
''',
            }
            for name, body in scripts.items():
                path = tools / name
                path.write_text('#!/bin/bash\nset -eu\n' + body)
                path.chmod(0o755)
            env = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ['PATH'],
                       RUNNER_TEMP=str(temp), GITHUB_PATH=str(temp / 'exported-path'),
                       MODE=mode, FAKE_TOOLS=str(tools))
            result = subprocess.run(['bash', str(ROOT / 'tests/ci_texlive.sh')],
                                    env=env, capture_output=True, text=True, timeout=15)
            files = {name: (temp / name).read_text() if (temp / name).exists() else ''
                     for name in ['attempts', 'collections', 'timeouts', 'exported-path']}
            return result, files

    def test_failed_install_switches_mirror_before_export(self):
        result, files = self.run_installer('install-fail')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(files['attempts'].splitlines()), 2)
        self.assertIn('mit.edu', files['collections'])
        self.assertEqual(len(files['exported-path'].splitlines()), 1)

    def test_failed_collections_switches_mirror(self):
        result, files = self.run_installer('collections-fail')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(files['collections'].splitlines()), 2)

    def test_failed_download_skips_install_and_switches_mirror(self):
        result, files = self.run_installer('download-fail')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(files['attempts'].splitlines()), 1)
        self.assertIn('mit.edu', files['attempts'])

    def test_wrong_major_version_is_never_exported(self):
        result, files = self.run_installer('wrong-version')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(files['exported-path'])
        self.assertFalse(files['collections'])

    def test_all_mirrors_fail_closed(self):
        result, files = self.run_installer('all-fail')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(files['attempts'].splitlines()), 2)
        self.assertFalse(files['exported-path'])

    def test_outside_tree_is_never_exported(self):
        result, files = self.run_installer('escape')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(files['exported-path'])

    def test_success_is_bounded_and_does_not_try_second_mirror(self):
        result, files = self.run_installer('success')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(files['attempts'].splitlines()), 1)
        self.assertIn('--kill-after=30s 8m', files['timeouts'])
        self.assertIn('--kill-after=30s 10m', files['timeouts'])


if __name__ == '__main__':
    unittest.main()
