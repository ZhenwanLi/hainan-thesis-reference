#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
target="${1:-main}"
case "$target" in main|main-humanities|main-foreign|main-art) ;; *) echo "Unknown entry: $target" >&2; exit 2;; esac
[[ -f "$target.tex" ]] || { echo "Entry not available in this template: $target" >&2; exit 2; }
mode="${THESIS_FONTS:-preview}"
case "$mode" in preview|school) ;; *) echo "THESIS_FONTS must be preview or school" >&2; exit 2;; esac
for tool in xelatex bibtex; do
  command -v "$tool" >/dev/null || { echo "Missing dependency: $tool (see docs/BUILD.md)" >&2; exit 127; }
done
build="$PWD/.build/$target"
mkdir -p -- "$build"
export BIBINPUTS="$PWD:${BIBINPUTS:-}"
export BSTINPUTS="$PWD:${BSTINPUTS:-}"
run_tex() {
  xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -file-line-error \
    -jobname="$target" -output-directory="$build" \
    "\def\ThesisFontMode{$mode}\input{$target.tex}"
}
echo "Font mode: $mode (preview is NOT school typography)"
run_tex
if [[ "$target" != main-art ]]; then (cd -- "$build"; bibtex "$target"); fi
run_tex
run_tex
cp -- "$build/$target.pdf" "$target.pdf.tmp"
mv -- "$target.pdf.tmp" "$target.pdf"
echo "Complete: $target.pdf; log: .build/$target/$target.log"
