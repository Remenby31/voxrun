#!/bin/bash
# Voxtral Voice Toggle - Press hotkey to start recording, press again to transcribe

VOXTRAL_DIR="/home/remenby/projects/voxtral"
PYTHON="$VOXTRAL_DIR/venv/bin/python"
LOCKFILE="/tmp/voxtral_recording.lock"
AUDIOFILE="/tmp/voxtral_audio.wav"
TRANSCRIBE_SCRIPT="$VOXTRAL_DIR/voxtral_transcribe.py"
OVERLAY_SCRIPT="$VOXTRAL_DIR/voxtral_overlay.py"

export LD_PRELOAD=/usr/lib/libgtk4-layer-shell.so

# Kill any existing overlay
pkill -f "voxtral_overlay.py" 2>/dev/null

if [ -f "$LOCKFILE" ]; then
    # Stop recording
    PID=$(cat "$LOCKFILE")
    kill "$PID" 2>/dev/null
    rm "$LOCKFILE"

    # Show processing overlay
    "$PYTHON" "$OVERLAY_SCRIPT" "Transcription en cours..." "processing" 30000 &
    OVERLAY_PID=$!

    # Transcribe
    RESULT=$("$PYTHON" "$TRANSCRIBE_SCRIPT" "$AUDIOFILE" 2>/dev/null)

    # Kill processing overlay
    kill $OVERLAY_PID 2>/dev/null
    pkill -f "voxtral_overlay.py" 2>/dev/null

    if [ -n "$RESULT" ]; then
        # Copy to clipboard
        echo -n "$RESULT" | wl-copy

        # Show result overlay
        "$PYTHON" "$OVERLAY_SCRIPT" "$RESULT" "result" 5000 &
    else
        "$PYTHON" "$OVERLAY_SCRIPT" "Transcription échouée" "result" 3000 &
    fi

    rm -f "$AUDIOFILE"
else
    # Start recording - show overlay
    "$PYTHON" "$OVERLAY_SCRIPT" "Enregistrement" "recording" 60000 &

    # Record in background
    parecord --channels=1 --rate=16000 --format=s16le --file-format=wav "$AUDIOFILE" &
    echo $! > "$LOCKFILE"
fi
