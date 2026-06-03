# #!/bin/bash

# MUSIC_DIR="$HOME/Music/YT"
# VIDEO_DIR="$HOME/Videos/YT"

# mkdir -p "$MUSIC_DIR" "$VIDEO_DIR"

# url=$(rofi -dmenu -p "🎥 Enter YouTube URL:")

# [ -z "$url" ] && exit

# choice=$(echo -e "🎵 Audio (mp3)\n📹 Video (mp4)" | rofi -dmenu -p "Download:")

# case "$choice" in
#     "🎵 Audio (mp3)")
#         yt-dlp -x --audio-format mp3 -o "$MUSIC_DIR/%(title)s.%(ext)s" "$url"
#         notify-send "✅ YouTube Downloader" "Saved as MP3 in $MUSIC_DIR"
#         ;;
#     "📹 Video (mp4)")
#         yt-dlp -f "bestvideo+bestaudio" -o "$VIDEO_DIR/%(title)s.%(ext)s" "$url"
#         notify-send "✅ YouTube Downloader" "Saved as MP4 in $VIDEO_DIR"
#         ;;
#     *)
#         notify-send "❌ YouTube Downloader" "Cancelled"
#         ;;
# esac









#!/bin/bash

MUSIC_DIR="$HOME/Music/YT"
VIDEO_DIR="$HOME/Videos/YT"

mkdir -p "$MUSIC_DIR" "$VIDEO_DIR"

# Ask for URL
url=$(rofi -dmenu -p "🎥 Enter YouTube URL:")
[ -z "$url" ] && exit

PROGRESS_FILE="/tmp/yt-dlp-progress"

run_ytdlp() {
    echo "dl 0" > "$PROGRESS_FILE"
    yt-dlp --newline "$@" 2>&1 | while IFS= read -r line; do
        if [[ "$line" =~ \[download\][[:space:]]+([0-9]+(\.[0-9]+)?)% ]]; then
            echo "dl ${BASH_REMATCH[1]}" > "$PROGRESS_FILE"
        fi
    done
    exit_code=${PIPESTATUS[0]}
    if [ $exit_code -eq 0 ]; then
        echo "ok 100" > "$PROGRESS_FILE"
    else
        echo "er 0" > "$PROGRESS_FILE"
    fi
    return $exit_code
}

# Choose Audio or Video
choice=$(echo -e "🎵 Audio (mp3)\n📹 Video (mp4)" | rofi -dmenu -p "Download:")
case "$choice" in
    "🎵 Audio (mp3)")
        run_ytdlp -x --audio-format mp3 -o "$MUSIC_DIR/%(title)s.%(ext)s" "$url" && \
            notify-send "✅ YouTube Downloader" "Saved as MP3 in $MUSIC_DIR" || \
            notify-send "❌ YouTube Downloader" "Download failed"
        ;;
    "📹 Video (mp4)")
        # Ask for resolution
        res=$(echo -e "1080p\n720p\n480p\n360p" | rofi -dmenu -p "Resolution:")
        case "$res" in
            "1080p") format="bestvideo[height<=1080]+bestaudio/best[height<=1080]" ;;
            "720p")  format="bestvideo[height<=720]+bestaudio/best[height<=720]" ;;
            "480p")  format="bestvideo[height<=480]+bestaudio/best[height<=480]" ;;
            "360p")  format="bestvideo[height<=360]+bestaudio/best[height<=360]" ;;
            *) notify-send "❌ YouTube Downloader" "Cancelled" ; exit ;;
        esac

        run_ytdlp -f "$format" -o "$VIDEO_DIR/%(title)s.%(ext)s" "$url" && \
            notify-send "✅ YouTube Downloader" "Saved $res MP4 in $VIDEO_DIR" || \
            notify-send "❌ YouTube Downloader" "Download failed"
        ;;
    *)
        notify-send "❌ YouTube Downloader" "Cancelled"
        ;;
esac
