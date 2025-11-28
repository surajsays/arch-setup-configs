#!/bin/bash

# Folder where wallpapers are stored
DIR="$HOME/Pictures/Wallpapers"

# Predefined list of wallpapers
WALLPAPERS=(
w3.png
peace.jpg
green-hill.jpg
wall4.png
sunflower.png
w1.png
wall3.png
night.png
wall2.png
hills.jpg
w2.png
nezuko-kamado.png
wall1.png   
)

# Show list in rofi
SELECTED=$(printf "%s\n" "${WALLPAPERS[@]}" | rofi -dmenu -i -p "Select wallpaper:")

# Apply selected wallpaper
if [ -n "$SELECTED" ]; then
    feh --bg-scale "$DIR/$SELECTED"
fi
