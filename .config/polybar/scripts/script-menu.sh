#!/bin/bash

ICON_RESOLUTIONS=""
ICON_YOUTUBE=""
ICON_AMBEROL=""
ICON_OPACITY=""
ICON_CALENDAR=""

SCRIPTS_DIR="$HOME/.config/polybar/scripts"
CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

choice=$(echo -e "── Personal ──
$ICON_RESOLUTIONS  Fine!
$ICON_CALENDAR  Mini Calendar

── Music / Apps ──
$ICON_YOUTUBE  YouTube Downloader
$ICON_AMBEROL  Amberol

── Appearance ──
$ICON_OPACITY  Toggle Opacity" \
| rofi -dmenu -p " Menu:")

case "$choice" in
    "$ICON_RESOLUTIONS  Fine!") ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh ;;
    "$ICON_CALENDAR  Mini Calendar") python3 "$CALENDAR_SCRIPT" ;;
    "$ICON_YOUTUBE  YouTube Downloader") ~/.config/polybar/scripts/youtube-dl.sh ;;
    "$ICON_AMBEROL  Amberol") ~/.config/polybar/scripts/amberol-dark.sh ;;
    "$ICON_OPACITY  Toggle Opacity") "$SCRIPTS_DIR/toggle-opacity.sh" ;;
esac
