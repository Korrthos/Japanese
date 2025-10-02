#!/bin/bash

set -euo pipefail

readonly root_dir=$(git rev-parse --show-toplevel)

"$root_dir/japanese/ajt_common/package.sh" \
	--package "AJT Japanese" \
	--name "AJT Japanese" \
	--root "japanese" \
	"$@"

readonly output=ajt_japanese.ankiaddon

if ! [[ -f $output ]]; then
	echo "Missing file: $output"
	exit 1
fi

readonly tmpdir=$(mktemp -d)
# Create the desired directory structure inside tmpdir
mkdir -p "$tmpdir/kanjigrid"
mkdir -p "$tmpdir/kanjigrid/data"

# Copy contents
cp -a -- "$root_dir/kanjigrid/src"/*.py "$root_dir/kanjigrid/src"/*.json "$tmpdir/kanjigrid/"
cp -a -- "$root_dir/kanjigrid/data/." "$tmpdir/kanjigrid/data/"

# Add to zip

( cd -- "$tmpdir" && zip -ur "$root_dir/$output" "kanjigrid" ) # add "kanjigrid" from the PWD.

rm -rf -- "$tmpdir"

echo -e "Added kanjigrid to the archive."
