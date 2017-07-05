mkdir -p hoplite_assets/cleaned
for asset in $(ls hoplite_assets/*.png); do
    f=$(basename $asset)
    convert hoplite_assets/$f -trim +repage hoplite_assets/cleaned/$f
done

