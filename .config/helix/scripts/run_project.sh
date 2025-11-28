#!/bin/bash
# ~/.config/helix/scripts/run_project.sh

# Get the current working directory (Helix runs scripts from project dir)
cd "$(pwd)"

# Try to detect project type and run appropriately
if [ -f "Cargo.toml" ]; then
    echo "🦀 Detected Rust project"
    kitty --hold bash -c "cargo run"
elif [ -f "package.json" ]; then
    echo "🟨 Detected Node project"
    kitty --hold bash -c "npm start || node index.js"
elif [ -f "main.py" ]; then
    echo "🐍 Running Python file"
    kitty --hold bash -c "python3 main.py"
elif [ -f "Makefile" ]; then
    echo "⚙️  Running Makefile"
    kitty --hold bash -c "make run || make"
else
    echo "❓ No known project type detected"
fi

