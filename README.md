

# Resume Parser

This project is a Python-based resume parser designed to extract key information from resume PDFs. It processes resumes in a structured format and extracts sections such as:

- Full Name
- Contact Information (email, phone, LinkedIn, etc.)
- Summary/Objective
- Skills
- Work Experience
- Education
- Certifications
- Projects

## Project Structure

The project consists of the following files and folders:

```
Resume Parser/
│
├── resume_parser.py         # Contains functions to parse and extract information from resume PDFs.
├── main.py                  # Main script that uses the functions from `resume_parser.py` to parse the resume.
├── main.ipynb               # Jupyter notebook that demonstrates how to use the parser with example data.
├── data/                    # Folder containing example resume PDFs used for testing the parser.
│   └── <resume_files.pdf>   # Example resume PDF files.
```

## Requirements

To run this project, you need to install the following Python libraries:

- `PyPDF2`
- `PyMuPDF` (fitz)
- `spacy`
- `re` (standard Python library)

You can install the required libraries using pip:

```
pip install PyPDF2 PyMuPDF spacy
```

Make sure to also download the `spacy` language model:

```
python -m spacy download en_core_web_sm
```

## How It Works

The `resume_parser.py` script contains functions to extract key sections from a resume PDF. The main functionality includes:

1. **Text Extraction**: Extracting text from PDF files using `PyPDF2` and `PyMuPDF` (fitz).
2. **Section Identification**: Using regular expressions and spaCy to identify different sections (e.g., "Skills", "Work Experience", etc.).
3. **Data Extraction**: Parsing the identified sections to extract relevant information such as dates, job titles, companies, responsibilities, skills, and more.
4. **Output**: The extracted data is returned in a structured dictionary format.

### Example Usage

To run the script:

1. **Modify PDF Path**: In the `main.py` file, specify the path to the resume PDF you want to parse.
2. **Run the Script**: Execute the `main.py` script.

```
python main.py
```

The script will output a dictionary with the parsed information from the resume. Here's an example output:

```python
{
    'Name': 'John Doe',
    'Summary': 'Experienced data scientist with a passion for machine learning...',
    'Skills': ['Python', 'Machine Learning', 'Data Analysis'],
    'Work Experience': [
        {'Company': 'Company A', 'Title': 'Data Analyst', 'Dates': 'Jan 2020 - Present', 'Responsibilities': 'Analyzed data to inform business decisions...'}
    ],
    'Education': 'BSc in Computer Science, University of XYZ, 2019',
    'Certifications': ['Certified Data Scientist', 'Machine Learning Specialist'],
    'Projects': ['Project A', 'Project B']
}
```

### Running the Jupyter Notebook

If you'd like to experiment with the parser interactively, you can use the Jupyter notebook (`main.ipynb`). This notebook provides step-by-step examples of how to use the `resume_parser.py` functions and parse sample resumes stored in the `data/` folder.

To run the notebook:

1. Launch Jupyter Notebook:

   ```
   jupyter notebook
   ```

2. Open `main.ipynb` and follow the instructions in the cells to run the parsing process on the provided resumes.

## Data Folder

The `data/` folder contains sample resume PDFs used for testing the parser. These resumes can be processed using the provided scripts to see the output.

## Assumptions and Limitations

### Assumptions:
- Each resume is assumed to have sections with standard titles like "Skills", "Work Experience", and "Education".
- Contact information like email and phone numbers is typically found at the beginning of the resume.
- Sections are identified based on keywords and font styles.

### Limitations:
- The parser might not handle resumes with very complex or non-standard layouts.
- Scanned resumes or images embedded in PDFs might not be processed correctly without OCR (Optical Character Recognition).
- Further handling might be needed for multi-column or intricate resume formats.

## Future Enhancements

- Handle more complex PDF layouts, including multi-column formats and tables.
- Implement OCR functionality to extract text from scanned image-based resumes.
- Improve the accuracy of section identification using machine learning techniques.



## Acknowledgements

- **PyPDF2**: Used for basic PDF text extraction.
- **PyMuPDF (fitz)**: Provides advanced PDF parsing capabilities.
- **spaCy**: A powerful NLP library for text processing.
- **Jupyter Notebook**: For interactive use and testing of the parser.


