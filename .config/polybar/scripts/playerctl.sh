# #!/bin/bash

# # Get list of active players
# players=$(playerctl -l 2>/dev/null)

# # If no players, exit
# if [ -z "$players" ]; then
#     echo ""
#     exit
# fi

# # Find the player that is currently playing
# player=$(echo "$players" | while read -r p; do
#     status=$(playerctl -p "$p" status 2>/dev/null)
#     if [ "$status" = "Playing" ]; then
#         echo "$p"
#         exit
#     fi
# done)

# # If no active player is playing, fallback to the first one
# if [ -z "$player" ]; then
#     player=$(echo "$players" | head -n 1)
# fi

# # Get status
# status=$(playerctl -p "$player" status 2>/dev/null)

# # Choose control icon based on status
# if [ "$status" = "Playing" ]; then
#     control_icon=""  # pause
# elif [ "$status" = "Paused" ]; then
#     control_icon=""  # play
# else
#     control_icon=""  # stop
# fi

# # Map players to icons
# case "$player" in
#     vlc)
#         app_icon="󰕼"   # VLC cone
#         ;;
#     firefox)
#         app_icon=""   # Firefox
#         ;;
#     mpv)
#         app_icon=""   # MPV (Nerd Font play-circle)
#         ;;
#     spotify)
#         app_icon=""   # Spotify
#         ;;
#     *)
#         app_icon="󰝚"   # Generic play icon
#         ;;
# esac

# # Output app icon + status icon
# echo "$app_icon $control_icon"
















#!/bin/bash
# ~/.config/polybar/scripts/playerctl.sh
# Usage:
#   playerctl.sh                -> prints icon + status (for exec)
#   playerctl.sh play-pause     -> control command forwarded to preferred player
#   playerctl.sh previous       -> previous track
#   playerctl.sh next           -> next track
#   playerctl.sh position 5+    -> seek forward 5s
#   playerctl.sh position 5-    -> seek backward 5s

# find players
players=$(playerctl -l 2>/dev/null)

if [ -z "$players" ]; then
    echo ""
    exit
fi

# priority: amberol -> mpv -> first available
if playerctl -l | grep -q amberol; then
    player=amberol
elif playerctl -l | grep -q mpv; then
    player=mpv
else
    player=$(playerctl -l | head -n 1)
fi

# if arguments are given, forward them to playerctl for the chosen player
if [ $# -gt 0 ]; then
    playerctl -p "$player" "$@"
    exit $?
fi

# no args -> print icon + status (original behavior)
status=$(playerctl -p "$player" status 2>/dev/null)

if [ "$status" = "Playing" ]; then
    control_icon=""  # pause
elif [ "$status" = "Paused" ]; then
    control_icon=""  # play
else
    control_icon=""  # stop / unknown
fi

case "$player" in
   amberol|*Amberol)
        app_icon="󰓇"   # amberol uses the spotify icon here (you can change)
        ;;
    mpv)
        app_icon=""
        ;;
    firefox|*firefox*)
        app_icon="󰈸"   # Firefox logo
        ;;
    *)
        app_icon="󰝚"
        ;;
esac

echo "$app_icon $control_icon"
exit 0



