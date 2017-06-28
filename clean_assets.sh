mkdir -p hoplite_assets/cleaned
for monster in $(ls hoplite_assets/mon*.png); do
    f=$(basename $monster)
    convert hoplite_assets/$f +repage -crop 24x24+4+12 -resize 45x45 hoplite_assets/cleaned/$f
done

