#!/bin/bash

echo "Running commands [dos2unix, chmod] on scripts..."

IFS=','

find . -type f -name "*.sh" -print0 | while IFS= read -r -d '' script; do
    echo "- $script"
    dos2unix "$script"
    chmod +x "$script"
done
