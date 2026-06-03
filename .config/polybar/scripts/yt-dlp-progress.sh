#!/bin/bash

PROGRESS_FILE="/tmp/yt-dlp-progress"

if [ ! -f "$PROGRESS_FILE" ] || [ ! -s "$PROGRESS_FILE" ]; then
    printf " "
    exit
fi

read -r status pct < "$PROGRESS_FILE"

case "$status" in
    dl)
        int_pct=$(printf "%.0f" "$pct" 2>/dev/null || echo "$pct")
        filled=$((int_pct / 10))
        empty=$((10 - filled))
        bar=""
        for ((i=0; i<filled; i++)); do bar="${bar}■"; done
        for ((i=0; i<empty; i++)); do bar="${bar}□"; done
        printf " %s %d%%" "$bar" "$int_pct"
        ;;
    ok|er)
        file_time=$(stat -c %Y "$PROGRESS_FILE" 2>/dev/null || date -r "$PROGRESS_FILE" +%s 2>/dev/null || echo "0")
        now=$(date +%s)
        age=$((now - file_time))
        if [ "$status" = "ok" ] && [ "$age" -lt 8 ]; then
            printf " ✓ Done"
        elif [ "$status" = "er" ] && [ "$age" -lt 8 ]; then
            printf " ✗ Failed"
        else
            > "$PROGRESS_FILE"
            printf " "
        fi
        ;;
    *)
        printf " "
        ;;
esac
