#!/bin/bash

# Define the output file
output_file="Config.in"

# Clear the output file if it exists
> "$output_file"

# Iterate over all directories under ./package
for dir in package/*/; do
  # Check if it's a directory
  if [ -d "$dir" ]; then
    # Generate the desired line and append it to the output file
    echo "source \"\$BR2_EXTERNAL_RASPI3_IMG_CLS_PATH/${dir}Config.in\"" >> "$output_file"
  fi
done

echo "Config file list has been generated in $output_file."
