#!/bin/bash
# 這個腳本用於下載、解壓縮並執行 brush 應用程式

URL="https://github.com/ArthurBrussee/brush/releases/download/0.2.0/brush-app-x86_64-unknown-linux-gnu.tar.xz"
FILE="brush-app-x86_64-unknown-linux-gnu.tar.xz"

# Download the file (if it doesn't already exist)
if [ ! -f "$FILE" ]; then
  echo "📥Donwload brush app..."
  curl -L -o "$FILE" "$URL"  # -L: 自動跟隨重定向 (redirect)
else
  echo "✅Brush app already downloaded."
fi

# Extract the file
echo "📦Extracting brush..."
tar -xf "$FILE"  # -f: Specify the file to extract

# Locate the executable
cd brush-app-x86_64-unknown-linux-gnu/
EXEC="./brush_app"

# Grant execute permissions
chmod +x "$EXEC"

# Run the application
echo "🚀Run the application"
./"$EXEC"