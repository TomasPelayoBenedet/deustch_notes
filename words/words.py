import csv
import subprocess
import os
from math import ceil

def count_words(text):
    """
    Counts the number of words in a text
    
    Args:
        text (str): Text to count words from
        
    Returns:
        int: Number of words
    """
    return len(str(text).split())

def split_data_by_word_limit(data, word_limit=70):
    """
    Splits data into chunks where each chunk has at most word_limit words
    
    Args:
        data (list): List of rows from CSV
        word_limit (int): Maximum number of words per chunk
        
    Returns:
        list: List of chunks where each chunk respects the word limit
    """
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for row in data:
        # Count words in current row
        row_word_count = sum(count_words(cell) for cell in row)
        
        # If adding this row would exceed the limit, start a new chunk
        if current_word_count + row_word_count > word_limit and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_word_count = 0
        
        current_chunk.append(row)
        current_word_count += row_word_count
    
    # Add the last chunk if it has any rows
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def create_latex_document(csv_file_path, output_tex_file, words_per_table=70):
    """
    Creates a LaTeX document from a CSV file with two side-by-side tables per page
    
    Args:
        csv_file_path (str): Path to the input CSV file
        output_tex_file (str): Path where the output TEX file will be saved
        words_per_table (int): Maximum number of words per table (default: 70)
    """
    # Read CSV
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    
    # Sort data by the first column
    data.sort(key=lambda x: x[0].lower())  # Case-insensitive sort
    
    # Split data into chunks respecting the word limit
    chunks = split_data_by_word_limit(data, words_per_table)
    
    # Calculate required pages
    total_chunks = len(chunks)
    chunks_per_page = 2  # 2 tables per page
    total_pages = ceil(total_chunks / chunks_per_page)

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
\renewcommand{\headrulewidth}{1pt}

\begin{document}
'''

    # Process data page by page
    for page in range(total_pages):
        start_idx = page * chunks_per_page
        end_idx = min(start_idx + chunks_per_page, total_chunks)
        
        # Add left table
        latex_content += r'''
\begin{minipage}{0.48\textwidth}
    \centering
    \renewcommand{\arraystretch}{1.5}
    \begin{tabular}{|>{\raggedright\arraybackslash}p{3.5cm}|>{\raggedright\arraybackslash}p{3.5cm}|}
        \hline
        \rowcolor{gray!20} \textbf{Deustch} & \textbf{English} \\
        \hline
'''
        # Add left table data
        for row in chunks[start_idx]:
            latex_content += f"        {row[0]} & {row[1]} \\\\\hline\n"

        latex_content += r'''    \end{tabular}
\end{minipage}%
'''

        # Add right table if there's data for it
        if start_idx + 1 < end_idx:
            latex_content += r'''\hfill
\begin{minipage}{0.48\textwidth}
    \centering
    \renewcommand{\arraystretch}{1.5}
    \begin{tabular}{|>{\raggedright\arraybackslash}p{3.5cm}|>{\raggedright\arraybackslash}p{3.5cm}|}
        \hline
        \rowcolor{gray!20} \textbf{Deustch} & \textbf{English} \\
        \hline
'''
            # Add right table data
            for row in chunks[start_idx + 1]:
                latex_content += f"        {row[0]} & {row[1]} \\\\\hline\n"

            latex_content += r'''    \end{tabular}
\end{minipage}
'''

        # Add page break if not the last page
        if page < total_pages - 1:
            latex_content += r'''
\newpage
'''

    latex_content += r'''
\end{document}
'''

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
    # File names and paths
    csv_file = "words/words.csv"  # Change this to your CSV file name
    tex_dir = "tex"  # Directory for tex files
    tex_file = os.path.join(tex_dir, "words.tex")
    
    # Create LaTeX document
    create_latex_document(csv_file, tex_file, words_per_table=90)
    
    # Compile PDF
    compile_latex(tex_file)

if __name__ == "__main__":
    main()