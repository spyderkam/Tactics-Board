#!/bin/bash

# Usage: ./replace_string.sh "old_string" "new_string" /path/to/directory

OLD_STRING=$1
NEW_STRING=$2
DIRECTORY=$3

# Check if all arguments are provided
if [ -z "$OLD_STRING" ] || [ -z "$NEW_STRING" ] || [ -z "$DIRECTORY" ]; then
  echo "Usage: $0 OLD_STRING NEW_STRING DIRECTORY"
  exit 1
fi

# Find and replace
find "$DIRECTORY" -type f -exec sed -i '' "s/$OLD_STRING/$NEW_STRING/g" {} +

echo "Replacement completed."