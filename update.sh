#!/bin/bash

CONFIG_FILE="update_config.txt"

[ ! -f "$CONFIG_FILE" ] && {
    echo "Error: $CONFIG_FILE not found"
    echo "Format: directory:command"
    exit 1
}

ORIGINAL_DIR=$(pwd)
trap "cd $ORIGINAL_DIR" EXIT

while IFS=: read -r directory command; do
    directory=$(echo "$directory" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    command=$(echo "$command" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    
    [[ ! "$directory" = /* ]] && directory="$ORIGINAL_DIR/$directory"
    directory=$(realpath -m "$directory")
    
    [ ! -d "$directory" ] && {
        echo "✗ $directory: Directory not found"
        continue
    }
    
    cd "$directory" &>/dev/null || {
        echo "✗ $directory: Cannot access directory"
        continue
    }
    
    if eval "$command" &>/dev/null; then
        echo "✓ $directory: Success"
    else
        echo "✗ $directory: Command failed"
    fi
    
    cd "$ORIGINAL_DIR" &>/dev/null
done < "$CONFIG_FILE"