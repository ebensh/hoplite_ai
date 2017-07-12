mkdir -p hoplite_assets/cleaned
for asset in $(ls hoplite_assets/*.png); do
    f=$(basename $asset)
    convert hoplite_assets/$f -trim +repage -background "#000000" -transparent-color "#000000" -flatten hoplite_assets/cleaned/$f
    #convert hoplite_assets/$f -trim +repage -flatten hoplite_assets/cleaned/$f
done

