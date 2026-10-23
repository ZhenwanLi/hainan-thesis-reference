#!/usr/bin/env bash
# CI-only installer: explicit HTTPS repositories, bounded attempts, no root writes.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
: "${RUNNER_TEMP:?CI temporary directory is required}"
: "${GITHUB_PATH:?CI path export file is required}"

install_from() (
  set -euo pipefail
  repository="$1"
  attempt="$2"
  work="$RUNNER_TEMP/tex-attempt-$attempt"
  texroot="$work/texlive"
  mkdir -p "$work/installer"
  curl --fail --location --retry 2 --connect-timeout 15 --max-time 90 \
    "$repository/install-tl-unx.tar.gz" -o "$work/install-tl.tar.gz"
  tar -xzf "$work/install-tl.tar.gz" -C "$work/installer" --strip-components=1
  python3 "$ROOT/tests/ci_profile.py" "$texroot" > "$work/profile"
  timeout --kill-after=30s 8m perl "$work/installer/install-tl" \
    -profile "$work/profile" -repository "$repository"
  export PATH="$texroot/bin/x86_64-linux:$PATH"
  tlmgr --version | grep 'version 2026'
  for tree in TEXMFLOCAL TEXMFSYSVAR TEXMFSYSCONFIG TEXMFHOME TEXMFVAR TEXMFCONFIG; do
    path="$(kpsewhich -var-value="$tree")"
    case "$path" in "$texroot/"*) ;; *) echo "Unexpected $tree: $path" >&2; exit 1;; esac
  done
  timeout --kill-after=30s 10m tlmgr --repository "$repository" install collection-xetex collection-langchinese collection-latexextra collection-fontsrecommended collection-bibtexextra collection-pictures collection-mathscience
  # Export only a complete, verified installation. Failed attempts stay isolated.
  echo "$texroot/bin/x86_64-linux" >> "$GITHUB_PATH"
)

repositories=(
  'https://ctan.math.illinois.edu/systems/texlive/tlnet'
  'https://mirrors.mit.edu/CTAN/systems/texlive/tlnet'
)
attempt=0
for repository in "${repositories[@]}"; do
  attempt=$((attempt + 1))
  echo "::group::TeX Live mirror attempt $attempt: $repository"
  # Do not put install_from in an if: that disables errexit inside functions.
  set +e
  (set -e; install_from "$repository" "$attempt")
  status=$?
  set -e
  echo '::endgroup::'
  if [[ "$status" == 0 ]]; then exit 0; fi
  echo "::warning::TeX Live mirror attempt $attempt failed (exit $status); trying next mirror."
done
echo '::error::All TeX Live mirrors failed. No installation exported.' >&2
exit 1
