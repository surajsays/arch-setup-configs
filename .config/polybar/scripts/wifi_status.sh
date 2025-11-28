#!/bin/bash

# if nmcli radio wifi | grep -q "enabled"; then
#     echo "%{F#00FF00}%{F-}"   # Green icon if Wi-Fi ON
# else
#     echo "%{F#FF0000}%{F-}"   # Red icon if Wi-Fi OFF
# fi



#!/bin/bash

# Interface name (check with nmcli d)
IFACE="wlan0"

# Temp file to store last status
STATE_FILE="/tmp/wifi_status_last"

# Get current status
status=$(nmcli -t -f WIFI g)   # enabled/disabled
connected=$(nmcli -t -f DEVICE,STATE d | grep "$IFACE" | cut -d: -f2)

# Determine current state
if [[ "$status" == "enabled" ]]; then
    if [[ "$connected" == "connected" ]]; then
        icon="%{F#00FF00}%{F-}"
        current_state="connected"
    else
        icon="%{F#FFFF00}%{F-}"
        current_state="enabled_no_net"
    fi
else
    icon="%{F#FF0000}%{F-}"
    current_state="disabled"
fi

# Read last state
last_state=$(cat "$STATE_FILE" 2>/dev/null || echo "")

# Send notification if state changed
if [[ "$current_state" != "$last_state" ]]; then
    case $current_state in
        connected)
            ssid=$(nmcli -t -f ACTIVE,SSID dev wifi | grep '^yes' | cut -d: -f2)
            notify-send " Wi-Fi Connected" "Connected to $ssid"
            ;;
        enabled_no_net)
            notify-send " Wi-Fi Enabled" "Not connected to any network"
            ;;
        disabled)
            notify-send "❌ Wi-Fi Disabled"
            ;;
    esac
    echo "$current_state" > "$STATE_FILE"
fi

# Output for Polybar
echo "$icon"

