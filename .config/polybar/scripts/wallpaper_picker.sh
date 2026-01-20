#!/bin/bash

# Folder where wallpapers are stored
DIR="$HOME/Pictures/Wallpapers"

# Predefined list of wallpapers
WALLPAPERS=(
w3.png
peace.jpg
sunflower.png
w1.png
w2.png
wallhaven-382541.jpg
daniel-leone-185834.jpg
)

# Show list in rofi
SELECTED=$(printf "%s\n" "${WALLPAPERS[@]}" | rofi -dmenu -i -p "Select wallpaper:")

# Apply selected wallpaper
if [ -n "$SELECTED" ]; then
    feh --bg-scale "$DIR/$SELECTED"
fi
