# feh --bg-fill ~/.config/polybar/polybar-themes/onedark-theme/wallpaper/void-cool.png

# # picom --config ~/.config/polybar/polybar-themes/onedark-theme/picom/picom.conf &

# sh ~/.config/polybar/polybar-themes/onedark-theme/polybar/launch.sh &


#!/bin/bash

# Kill any existing polybar instance
killall -q polybar

# Wait until polybar has shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

#launch bar

# Launch polybar
polybar bar -c ~/.config/polybar/themes/one-dark/polybar/config &
