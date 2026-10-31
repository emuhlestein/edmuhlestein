#!/bin/sh
set -e

# Install if node_modules is missing or package.json is newer
if [ ! -d node_modules ] || [ package.json -nt node_modules ]; then
  echo "Installing npm dependencies..."
  npm install
fi

exec npm start