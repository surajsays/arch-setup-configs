# #!/bin/bash

# ICON_RESOLUTIONS=""
# ICON_YOUTUBE=""
# ICON_AMBEROL=""
# ICON_OPACITY=""
# ICON_CALENDAR=""

# SCRIPTS_DIR="$HOME/.config/polybar/scripts"
# CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

# choice=$(echo -e "── Personal ──
# $ICON_RESOLUTIONS  Fine!
# $ICON_CALENDAR  Mini Calendar

# ── Music / Apps ──
# $ICON_YOUTUBE  YouTube Downloader
# $ICON_AMBEROL  Amberol

# ── Appearance ──
# $ICON_OPACITY  Toggle Opacity" \
# | rofi -dmenu -p " Menu:")

# case "$choice" in
#     "$ICON_RESOLUTIONS  Fine!") ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh ;;
#     "$ICON_CALENDAR  Mini Calendar") python3 "$CALENDAR_SCRIPT" ;;
#     "$ICON_YOUTUBE  YouTube Downloader") ~/.config/polybar/scripts/youtube-dl.sh ;;
#     "$ICON_AMBEROL  Amberol") ~/.config/polybar/scripts/amberol-dark.sh ;;
#     "$ICON_OPACITY  Toggle Opacity") "$SCRIPTS_DIR/toggle-opacity.sh" ;;
# esac




#!/bin/bash

ICON_RESOLUTIONS=""
ICON_YOUTUBE=""
ICON_AMBEROL=""
ICON_OPACITY=""
ICON_CALENDAR=""
ICON_THEME=""
ICON_ARROW=""

SCRIPTS_DIR="$HOME/.config/polybar/scripts"
THEMES_DIR="$HOME/.config/polybar/menu"
CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

# -----------------------------
# MAIN MENU
# -----------------------------
main_menu() {
    echo -e "── Personal ──
$ICON_RESOLUTIONS  Fine!
$ICON_CALENDAR  Mini Calendar

── Music / Apps ──
$ICON_YOUTUBE  YouTube Downloader
$ICON_AMBEROL  Amberol

── Appearance ──
$ICON_OPACITY  Toggle Opacity
$ICON_THEME  Polybar Themes $ICON_ARROW"
}

# -----------------------------
# THEMES SUBMENU (DYNAMIC)
# -----------------------------
themes_menu() {
    echo "── Polybar Themes ──"

    # Loop through all .sh theme scripts
    for script in "$THEMES_DIR"/*.sh; do
        [ -e "$script" ] || continue
        name=$(basename "$script" .sh)
        echo "$name"
    done

    echo "← Back"
}

# -----------------------------------
# Show MAIN MENU
# -----------------------------------
choice=$(main_menu | rofi -dmenu -p " Menu:")

case "$choice" in
    "$ICON_RESOLUTIONS  Fine!")
        ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh
        ;;

    "$ICON_CALENDAR  Mini Calendar")
        python3 "$CALENDAR_SCRIPT"
        ;;

    "$ICON_YOUTUBE  YouTube Downloader")
        "$SCRIPTS_DIR/youtube-dl.sh"
        ;;

    "$ICON_AMBEROL  Amberol")
        "$SCRIPTS_DIR/amberol-dark.sh"
        ;;

    "$ICON_OPACITY  Toggle Opacity")
        "$SCRIPTS_DIR/toggle-opacity.sh"
        ;;

    "$ICON_THEME  Polybar Themes $ICON_ARROW")
        theme_choice=$(themes_menu | rofi -dmenu -p " Themes:")

        if [[ "$theme_choice" == "← Back" ]]; then
            exec "$0"      # reload main menu
        elif [[ -f "$THEMES_DIR/$theme_choice.sh" ]]; then
            bash "$THEMES_DIR/$theme_choice.sh"
        fi
        ;;
esac

