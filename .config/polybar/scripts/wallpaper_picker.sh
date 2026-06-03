#!/bin/bash

# Folder where wallpapers are stored
DIR="$HOME/Pictures/Wallpapers"

# Predefined list of wallpapers
WALLPAPERS=(
    a_group_of_palm_trees.jpg
w3.png
a_house_on_stilts_on_a_lake.jpg
a_cartoon_of_a_dinosaur_swimming_in_water.png
bicycle.png
a_cartoon_of_a_couple_of_tentacles.png
27.png
a_road_leading_to_mountains.jpg
a_bird_flying_over_a_beach.jpg
sunflower.png
w1.png
10.png
a_cartoon_of_a_dinosaur_swimming_in_water.jpg
black.jpg
a_person_sitting_on_a_beach.jpg
w2.png
wallhaven-382541.jpg
calm.jpg
a_bicycle_leaning_against_a_wall.jpg
a_rocky_landscape_with_trees_and_water_in_the_background.jpg
a_graphic_design_of_a_bird.png
daniel-leone-185834.jpg
)


# Show list in rofi
SELECTED=$(printf "%s\n" "${WALLPAPERS[@]}" | rofi -dmenu -i -p "Select wallpaper:")

# Apply selected wallpaper
if [ -n "$SELECTED" ]; then
    feh --bg-scale "$DIR/$SELECTED"
fi
