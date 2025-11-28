#!/usr/bin/env bash

PICOM_CONF="$HOME/.config/picom/picom.conf"

apps=("Kitty" "Firefox" "VSCode")
icons=("" "" "")

# Build submenu options
submenu=""
for i in "${!apps[@]}"; do
    submenu+="${icons[$i]}  ${apps[$i]}\n"
done

choice=$(echo -e "$submenu" | rofi -dmenu -p "Toggle opacity for:")

if [[ -z "$choice" ]]; then
    exit 0
fi

# Determine class name in picom.conf
case "$choice" in
    *Kitty*) CLASS="kitty" ;;
    *Firefox*) CLASS="firefox" ;;
    *VSCode*) CLASS="code-oss" ;;
esac

# Check current opacity line
if grep -q "\".*:class_g = '$CLASS'\"" "$PICOM_CONF"; then
    # Line exists → toggle comment
    if grep -q "^[[:space:]]*#.*:class_g = '$CLASS'" "$PICOM_CONF"; then
        # Currently commented → enable
        sed -i "/class_g = '$CLASS'/ s/^#//" "$PICOM_CONF"
        notify-send "Opacity Enabled" "$CLASS opacity restored."
    else
        # Currently active → disable
        sed -i "/class_g = '$CLASS'/ s/^/#/" "$PICOM_CONF"
        notify-send "Opacity Disabled" "$CLASS opacity removed."
    fi
else
    notify-send "Not Found" "No opacity rule for $CLASS found."
    exit 1
fi

# Reload picom smoothly
if pgrep picom >/dev/null; then
    kill -USR1 $(pidof picom)
else
    picom --experimental-backends --backend xrender --daemon &
fi

