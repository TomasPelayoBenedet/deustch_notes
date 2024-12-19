#!/bin/bash

# Function to display usage information
show_usage() {
    echo "Usage: $0 <input_pdf> <output_pdf>"
    echo "Example: $0 input.pdf output.pdf"
    exit 1
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Error: Expected exactly 2 arguments"
    show_usage
fi

input_file="$1"
output_file="$2"

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' does not exist"
    exit 1
fi

# Check if input file is a PDF (basic check)
if [[ ! "$input_file" =~ \.pdf$ ]]; then
    echo "Warning: Input file doesn't have .pdf extension"
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if output directory is writable
output_dir=$(dirname "$output_file")
if [ ! -w "$output_dir" ]; then
    echo "Error: Cannot write to output directory '$output_dir'"
    exit 1
fi

# Convert input pdf into book
margin=40
((doublemargin = margin * 2))
pdfbook2 --paper=a4paper --short-edge -o $margin -i $doublemargin -t $margin -b $margin "$input_file"

# Set the new name for middle file
middle_file="$(dirname $input_file)/$(basename $input_file .pdf)-book.pdf"

# Check if Python script exists in the same directory as this script
script_dir=$(dirname "$0")
python_script="${script_dir}/rotateBook.py"

if [ ! -f "$python_script" ]; then
    echo "Error: Python script '$python_script' not found in the same directory"
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

# Execute the Python script
echo "Processing PDF file..."
python3 "$python_script" "$middle_file" "$output_file"

# Delete middle file just in case
if [ "$middle_file" != "$output_file" ]
then
    rm "$middle_file"
fi

# Check if the Python script executed successfully
if [ $? -eq 0 ]; then
    echo "PDF processing completed successfully"
else
    echo "Error occurred during PDF processing"
    exit 1
fi