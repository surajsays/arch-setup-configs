

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



