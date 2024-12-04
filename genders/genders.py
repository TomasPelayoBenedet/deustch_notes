import csv
import subprocess
import os
from math import ceil

def read_csv_file(file_path):
    """
    Reads a CSV file and returns its contents as a sorted list
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        list: Sorted contents of the CSV file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            words = [row[0] for row in reader]  # Assuming one word per row
            return sorted(words, key=str.lower)  # Case-insensitive sort
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def split_data_by_row_limit(data, max_rows):
    """
    Splits data into chunks with a maximum number of rows
    
    Args:
        data (list): List of data rows
        max_rows (int): Maximum number of rows per chunk
        
    Returns:
        list: List of chunks
    """
    return [data[i:i + max_rows] for i in range(0, len(data), max_rows)]

def create_latex_document(maskulina_path, neutra_path, femenina_path, output_tex_file, rows_per_table=25):
    """
    Creates a LaTeX document with a three-column table for German word genders, with a row limit per table.
    
    Args:
        maskulina_path (str): Path to Maskulina CSV
        neutra_path (str): Path to Neutra CSV
        femenina_path (str): Path to Femenina CSV
        output_tex_file (str): Path where the output TEX file will be saved
        rows_per_table (int): Maximum number of rows per table
    """
    # Read and sort the CSV files
    maskulina_words = read_csv_file(maskulina_path)
    neutra_words = read_csv_file(neutra_path)
    femenina_words = read_csv_file(femenina_path)
    
    # Determine the maximum length for splitting
    max_length = max(len(maskulina_words), len(neutra_words), len(femenina_words))
    
    # Pad shorter lists to match max_length
    maskulina_words.extend([''] * (max_length - len(maskulina_words)))
    neutra_words.extend([''] * (max_length - len(neutra_words)))
    femenina_words.extend([''] * (max_length - len(femenina_words)))
    
    # Combine words into rows
    combined_data = list(zip(maskulina_words, neutra_words, femenina_words))
    
    # Split data into chunks based on rows_per_table
    chunks = split_data_by_row_limit(combined_data, rows_per_table)

    # Create LaTeX document content
    latex_content = r'''\documentclass{article}
\usepackage[margin=2cm]{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage[table,xcdraw]{xcolor}
\usepackage{fancyhdr}
\usepackage{lastpage}

\setlength{\abovecaptionskip}{0pt}
\setlength{\belowcaptionskip}{3pt}
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Page \thepage\ of \pageref{LastPage}}
\fancyhead[R]{Author: Tomás Pelayo}
\renewcommand{\headrulewidth}{0pt}

\begin{document}
'''

    for chunk in chunks:
        latex_content += r'''
\begin{table}[h!]
    \centering
    \renewcommand{\arraystretch}{1.5}
    \begin{tabular}{|>{\raggedright\arraybackslash}p{5cm}|>{\raggedright\arraybackslash}p{5cm}|>{\raggedright\arraybackslash}p{5cm}|}
        \hline
        \rowcolor{gray!20} \textbf{Maskulina (der)} & \textbf{Neutra (das)} & \textbf{Femenina (die)} \\
        \hline
'''
        for row in chunk:
            latex_content += f"        {row[0]} & {row[1]} & {row[2]} \\\\\hline\n"

        latex_content += r'''    \end{tabular}
\end{table}

\newpage
'''

    latex_content += r'\end{document}'

    # Create tex directory if it doesn't exist
    os.makedirs(os.path.dirname(output_tex_file), exist_ok=True)

    # Write content to the tex file
    with open(output_tex_file, 'w', encoding='utf-8') as file:
        file.write(latex_content)

def compile_latex(tex_file):
    """
    Compiles the LaTeX file to PDF using pdflatex
    
    Args:
        tex_file (str): Path to the TEX file to be compiled
    """
    try:
        # Run pdflatex twice to ensure references are updated correctly
        subprocess.run(['pdflatex', '-output-directory', os.path.dirname(tex_file), tex_file], check=True)
        subprocess.run(['pdflatex', '-output-directory', os.path.dirname(tex_file), tex_file], check=True)
        print(f"PDF successfully generated: {tex_file.replace('.tex', '.pdf')}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling PDF: {e}")
    except FileNotFoundError:
        print("Error: pdflatex is not installed or not in system PATH")

def main():
    # File paths
    genders_dir = "genders"
    tex_dir = "tex"
    
    maskulina_path = os.path.join(genders_dir, "Maskulina.csv")
    neutra_path = os.path.join(genders_dir, "Neutra.csv")
    femenina_path = os.path.join(genders_dir, "Femenina.csv")
    tex_file = os.path.join(tex_dir, "german_genders.tex")
    
    # Create LaTeX document
    create_latex_document(maskulina_path, neutra_path, femenina_path, tex_file, rows_per_table=34)
    
    # Compile PDF
    compile_latex(tex_file)

if __name__ == "__main__":
    main()
