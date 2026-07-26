#!/bin/bash

set -euo pipefail

root_dir=$(git rev-parse --show-toplevel)
tmpdir=$(mktemp -d)
output=ajt_japanese.ankiaddon
readonly root_dir tmpdir output

"$root_dir/japanese/ajt_common/package.sh" \
	--package "AJT Japanese" \
	--name "AJT Japanese" \
	--root "japanese" \
	"$@"

if ! [[ -f $output ]]; then
	echo "Missing file: $output"
	exit 1
fi

if ! git -C "$root_dir/kanjigrid" diff --quiet --exit-code; then
	echo "kanjigrid working tree is dirty"
	exit 1
fi

# Create the desired directory structure inside tmpdir
mkdir -p -- "$tmpdir/kanjigrid"
mkdir -p -- "$tmpdir/kanjigrid/data"

# Copy contents
cp -a -- "$root_dir/kanjigrid/src"/*.py "$root_dir/kanjigrid/src"/*.json "$tmpdir/kanjigrid/"
cp -a -- "$root_dir/kanjigrid/data/." "$tmpdir/kanjigrid/data/"

# Add to zip
( cd -- "$tmpdir" && zip -ur "$root_dir/$output" "kanjigrid" ) # add "kanjigrid" from the PWD.

rm -rf -- "$tmpdir"
echo -e "Added kanjigrid to the archive."
