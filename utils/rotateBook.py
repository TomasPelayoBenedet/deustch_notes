from PyPDF2 import PdfReader, PdfWriter
import os
import argparse

def rotate_even_pages(input_path, output_path, rotation_angle=180):
    """
    Rotate even-numbered pages in a PDF file.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path where the modified PDF will be saved
        rotation_angle (int): Angle of rotation (default: 180 degrees)
    """
    try:
        # Open the PDF file
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Process each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
            # Rotate even-numbered pages (note: page_num starts at 0)
            if (page_num + 1) % 2 == 0:  # Even page
                page.rotate(rotation_angle)
            
            writer.add_page(page)
        
        # Save the modified PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
            
        print(f"PDF processed successfully. Output saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Rotate even pages in a PDF file.')
    parser.add_argument('input_file', help='Path to the input PDF file')
    parser.add_argument('output_file', help='Path where the modified PDF will be saved')
    parser.add_argument('-r', '--rotation', type=int, default=180,
                        help='Rotation angle in degrees (default: 180)')

    # Parse arguments
    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return

    # Process the PDF
    rotate_even_pages(args.input_file, args.output_file, args.rotation)

if __name__ == "__main__":
    main()

