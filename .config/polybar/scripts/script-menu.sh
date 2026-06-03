

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

# #!/bin/bash

# ICON_RESOLUTIONS=""
# ICON_YOUTUBE=""
# ICON_AMBEROL=""
# ICON_OPACITY=""
# ICON_CALENDAR=""
# ICON_THEMES=" "
# ICON_POLYBAR=""

# SCRIPTS_DIR="$HOME/.config/polybar/scripts"
# CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

# choice=$(echo -e "── Personal ──
# $ICON_RESOLUTIONS  Fine!
# $ICON_CALENDAR  Mini Calendar

# ── Music / Apps ──
# $ICON_YOUTUBE  YouTube Downloader
# $ICON_AMBEROL  Amberol

# ── Appearance ──
# $ICON_OPACITY  Toggle Opacity
# $ICON_POLYBAR  Polybar Themes" \
# | rofi -dmenu -p " Menu:")

# case "$choice" in
#     "$ICON_RESOLUTIONS  Fine!") ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh ;;
#     "$ICON_CALENDAR  Mini Calendar") python3 "$CALENDAR_SCRIPT" ;;
#     "$ICON_YOUTUBE  YouTube Downloader") ~/.config/polybar/scripts/youtube-dl.sh ;;
#     "$ICON_AMBEROL  Amberol") ~/.config/polybar/scripts/amberol-dark.sh ;;
#     "$ICON_OPACITY  Toggle Opacity") "$SCRIPTS_DIR/toggle-opacity.sh" ;;

#     # NEW — Polybar Themes submenu
#     "$ICON_POLYBAR  Polybar Themes")
#         "$SCRIPTS_DIR/switch-polybar-theme.sh"
#         ;;
# esac







# #!/bin/bash

# ICON_RESOLUTIONS=""
# ICON_YOUTUBE=""
# ICON_AMBEROL=""
# ICON_OPACITY=""
# ICON_CALENDAR=""
# ICON_THEME=""       # Icon for themes
# ICON_ARROW=""        # Arrow for submenu

# SCRIPTS_DIR="$HOME/.config/polybar/scripts"
# CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

# main_menu() {
#     echo -e "── Personal ──
# $ICON_RESOLUTIONS  Fine!
# $ICON_CALENDAR  Mini Calendar

# ── Music / Apps ──
# $ICON_YOUTUBE  YouTube Downloader
# $ICON_AMBEROL  Amberol

# ── Appearance ──
# $ICON_OPACITY  Toggle Opacity
# $ICON_THEME  Polybar Themes $ICON_ARROW"
# }

# themes_menu() {
#     echo -e "── Polybar Themes ──
# Minimal Black
# Glass Blur
# Tokyo Night
# Catppuccin Mocha
# Neon Cyber

# ← Back"
# }

# # Show main menu
# choice=$(main_menu | rofi -dmenu -p " Menu:")

# case "$choice" in
#     "$ICON_RESOLUTIONS  Fine!") 
#         ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh 
#         ;;

#     "$ICON_CALENDAR  Mini Calendar") 
#         python3 "$CALENDAR_SCRIPT" 
#         ;;

#     "$ICON_YOUTUBE  YouTube Downloader") 
#         "$SCRIPTS_DIR/youtube-dl.sh" 
#         ;;

#     "$ICON_AMBEROL  Amberol") 
#         "$SCRIPTS_DIR/amberol-dark.sh" 
#         ;;

#     "$ICON_OPACITY  Toggle Opacity") 
#         "$SCRIPTS_DIR/toggle-opacity.sh" 
#         ;;

#     "$ICON_THEME  Polybar Themes $ICON_ARROW")
#         theme_choice=$(themes_menu | rofi -dmenu -p " Themes:")
#         case "$theme_choice" in
#             "Minimal Black")  "$SCRIPTS_DIR/switch-theme.sh" minimal-black ;;
#             "Glass Blur")     "$SCRIPTS_DIR/switch-theme.sh" glass-blur ;;
#             "Tokyo Night")    "$SCRIPTS_DIR/switch-theme.sh" tokyo-night ;;
#             "Catppuccin Mocha") "$SCRIPTS_DIR/switch-theme.sh" catppuccin ;;
#             "Neon Cyber")     "$SCRIPTS_DIR/switch-theme.sh" neon-cyber ;;
#             "← Back")         $0 ;; # reopen main menu
#         esac
#         ;;
# esac



# #!/bin/bash

# ICON_RESOLUTIONS=""
# ICON_YOUTUBE=""
# ICON_AMBEROL=""
# ICON_OPACITY=""
# ICON_CALENDAR=""
# ICON_THEME=""
# ICON_ARROW=""

# SCRIPTS_DIR="$HOME/.config/polybar/scripts"
# THEMES_DIR="$HOME/.config/polybar/menu"
# CALENDAR_SCRIPT="$HOME/Downloads/my-scripts/calender/mini-calender.py"

# # -----------------------------
# # MAIN MENU
# # -----------------------------
# main_menu() {
#     echo -e "── Personal ──
# $ICON_RESOLUTIONS  Fine!
# $ICON_CALENDAR  Mini Calendar

# ── Music / Apps ──
# $ICON_YOUTUBE  YouTube Downloader
# $ICON_AMBEROL  Amberol

# ── Appearance ──
# $ICON_OPACITY  Toggle Opacity
# $ICON_THEME  Polybar Themes $ICON_ARROW"
# }

# # -----------------------------
# # THEMES SUBMENU (DYNAMIC)
# # -----------------------------
# themes_menu() {
#     echo "── Polybar Themes ──"

#     # Loop through all .sh theme scripts
#     for script in "$THEMES_DIR"/*.sh; do
#         [ -e "$script" ] || continue
#         name=$(basename "$script" .sh)
#         echo "$name"
#     done

#     echo "← Back"
# }

# # -----------------------------------
# # Show MAIN MENU
# # -----------------------------------
# choice=$(main_menu | rofi -dmenu -p " Menu:")

# case "$choice" in
#     "$ICON_RESOLUTIONS  Fine!")
#         ~/Downloads/my-scripts/Resolutions/daily-resolutions.sh
#         ;;

#     "$ICON_CALENDAR  Mini Calendar")
#         python3 "$CALENDAR_SCRIPT"
#         ;;

#     "$ICON_YOUTUBE  YouTube Downloader")
#         "$SCRIPTS_DIR/youtube-dl.sh"
#         ;;

#     "$ICON_AMBEROL  Amberol")
#         "$SCRIPTS_DIR/amberol-dark.sh"
#         ;;

#     "$ICON_OPACITY  Toggle Opacity")
#         "$SCRIPTS_DIR/toggle-opacity.sh"
#         ;;

#     "$ICON_THEME  Polybar Themes $ICON_ARROW")
#         theme_choice=$(themes_menu | rofi -dmenu -p " Themes:")

#         if [[ "$theme_choice" == "← Back" ]]; then
#             exec "$0"      # reload main menu
#         elif [[ -f "$THEMES_DIR/$theme_choice.sh" ]]; then
#             bash "$THEMES_DIR/$theme_choice.sh"
#         fi
#         ;;
# esac



#!/bin/bash

ICON_YOUTUBE=""
ICON_AMBEROL=""
ICON_OPACITY=""
ICON_TIMER="󱎫"
ICON_THEME=""
ICON_ARROW=""

SCRIPTS_DIR="$HOME/.config/polybar/scripts"
THEMES_DIR="$HOME/.config/polybar/menu"
TIMER_SCRIPT="$SCRIPTS_DIR/timer.py"

# -----------------------------
# MAIN MENU
# -----------------------------
main_menu() {
    echo -e "── Utilities ──
$ICON_TIMER  Timer

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

    for script in "$THEMES_DIR"/*.sh; do
        [ -e "$script" ] || continue
        basename "$script" .sh
    done

    echo "← Back"
}

# -----------------------------------
# Show MAIN MENU
# -----------------------------------
choice=$(main_menu | rofi -dmenu -p " Menu:")

case "$choice" in
    "$ICON_TIMER  Timer")
        python3 "$TIMER_SCRIPT"
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
            exec "$0"
        elif [[ -f "$THEMES_DIR/$theme_choice.sh" ]]; then
            bash "$THEMES_DIR/$theme_choice.sh"
        fi
        ;;
esac
