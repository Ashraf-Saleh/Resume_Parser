"""
Resume Parser Script

This Python script is designed to parse and extract structured information from a resume PDF document. 
It analyzes and extracts key sections of a resume, including:

    1. **Full Name**: The name of the individual, typically located at the top of the resume.
    2. **Contact Information**: Email, phone number, LinkedIn URL, and other professional contact details.
    3. **Summary or Objective**: A brief summary or career objective that often appears near the top of the resume.
    4. **Skills**: A list of relevant skills or competencies.
    5. **Work Experience**: Job history, including company names, job titles, employment dates, and responsibilities.
    6. **Education**: Academic background, including degrees, institutions, dates, and any additional relevant information.
    7. **Certifications**: Any professional certifications or training courses.
    8. **Projects**: Information on personal or professional projects undertaken by the individual.

The parser uses a combination of PDF text extraction techniques and section-based keyword matching to identify and extract relevant content. It is designed to handle common variations in resume formats and layout complexities.

Libraries and Tools:
    - **PyPDF2**: Used for extracting text from PDFs.
    - **PyMuPDF (fitz)**: Used to handle advanced PDF parsing and layout extraction.
    - **re**: Regular expressions are used to identify and extract sections based on keywords and patterns.
    - **spacy**: Natural language processing library used to analyze and process the text for key information extraction.

Assumptions:
    - **Section Titles**: Each section in the resume is assumed to be preceded by a standard title, such as "Skills", "Work Experience", "Education", or "Certifications".
    - **Text Structure**: Contact details (e.g., email, phone number) are typically located near the top of the document. Sections are assumed to start with recognizable keywords and end when a new section title begins or at the end of the document.
    - **Missing Information**: If a section is not found, the parser returns a default "Not found" message or empty list, ensuring that missing sections do not interrupt the parsing process.

Challenges Addressed:
    - **Layout Variations**: The parser uses flexible logic and regular expressions to accommodate different resume formats (e.g., one-column or multi-column layouts).
    - **Non-Linear Text Extraction**: PDFs often store text in non-linear ways, especially in resumes with complex formatting (e.g., two-column layouts). This script is built to handle text extraction issues and minimize errors, although complex layouts may still require further fine-tuning.

Functionality:
    - The script defines several helper functions for extracting specific sections, such as `extract_name`, `extract_summary`, `extract_skills`, and others.
    - It uses the `extract_sections_with_font_info` function to analyze the document's structure, aiding the parser in identifying section boundaries and content.
    - The main function, `parse_resume`, orchestrates the entire parsing process by reading the PDF, calling the relevant extraction functions, and returning a dictionary of the parsed data.

Usage:
    1. **Manual Setup**: The path to the resume PDF is manually assigned within the `main.py` script. Ensure the PDF file path is correct before running the script.
    2. **Run the Script**: Execute the script by running the `main.py` file. The script will process the resume and output a structured dictionary containing the parsed sections.
    
    Example:
        ```bash
        python main.py
        ```

Outputs:
    - The script outputs a dictionary, where each key corresponds to a section of the resume (e.g., 'Name', 'Skills', 'Work Experience') and the value is the parsed content of that section.

    Example Output:
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

Notes:
    - Ensure the PDF file is well-structured and text-based (i.e., not scanned images) for accurate parsing.
    - The parser is designed to be flexible, but resumes with highly customized formats or extensive use of images and tables may require additional pre-processing.

Future Enhancements:
    - The parser could be extended to handle more complex PDF layouts, including multi-column or image-heavy resumes.
    - Additional improvements could be made to the regex patterns to enhance section detection for more diverse resume formats.
    - Support for more sophisticated machine learning-based extraction techniques could be added to improve the accuracy of section classification.

"""



from typing import Dict, List, Optional, Union
import PyPDF2
import fitz  # PyMuPDF
import re
import spacy

# Load the English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        str: The extracted text as a single string.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def extract_sections_with_font_info(pdf_path: str) -> Dict[str, List[Dict[str, Union[str, float]]]]:
    """
    Extracts sections of a PDF with text and font details to assist with identifying 
    headers and section content.

    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        dict: Dictionary with section headers as keys and content as lists of 
              dictionaries with "text", "font_size", and "font_name".
    """
    document = fitz.open(pdf_path)
    sections = {}
    current_title = None
    current_content = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        font_size = span["size"]
                        font_name = span["font"]

                        # If a line is detected as a title
                        if re.match(r"^[A-Z]{4,}\b.*", text):
                            if current_title:
                                sections[current_title] = current_content
                            current_title = text
                            current_content = [{"text": text, "font_size": font_size, "font_name": font_name}]
                        else:
                            if current_title:
                                current_content.append({"text": text, "font_size": font_size, "font_name": font_name})

    if current_title:
        sections[current_title] = current_content

    document.close()
    return sections


def extract_name(text: str) -> Optional[str]:
    """
    Extracts a name from the resume text based on typical name formatting.

    Args:
        text (str): Full resume text as a single string.

    Returns:
        Optional[str]: Extracted name or None if not found.
    """
    lines = text.splitlines()
    name_pattern = re.compile(r"^[A-Z][a-zA-Z]*\s+[A-Z][a-zA-Z]*$")
    
    for line in lines:
        line = line.strip()
        if name_pattern.match(line):
            return line

    return None


def extract_summary(text: str) -> str:
    """
    Extracts the summary or objective section from the resume text.

    Args:
        text (str): Full resume text as a single string.

    Returns:
        str: Extracted summary text or an empty string if not found.
    """
    summary_title_pattern = (
    r"^(Summary|Professional Summary|Career Summary|Executive Summary|Summary of Qualifications|"
    r"Profile|Professional Profile|Personal Profile|Career Profile|Personal Summary|Overview|"
    r"Objective|Career Objective|Professional Objective|Statement|Introduction|About Me)\s*$"
    )

    uppercase_title_pattern = r"^[A-Z]{4,}\b.*"  # Matches lines that are fully uppercase with more than 4 characters
    name_pattern = r"^[A-Za-z\s]+$"  # Basic pattern to match a name (adjust as needed)

    lines = text.splitlines()
    summary_text = ""
    name_found = False
    is_capturing = False

    for line in lines:
        if re.match(summary_title_pattern, line, re.IGNORECASE):
            is_capturing = True
            continue
        elif is_capturing:
            if re.match(uppercase_title_pattern, line):
                break
            elif line.strip():
                summary_text += line.strip() + " "
                if line.strip().endswith('.'):
                    break
        elif re.match(name_pattern, line) and not name_found:
            name_found = True
        elif name_found and not is_capturing:
            summary_text = line.strip()
            is_capturing = True



    return summary_text.strip()


def extract_accounts_from_resume(text: str) -> Dict[str, List[str]]:
    """
    Extracts URLs and emails from the resume text.

    Args:
        text (str): Full resume text as a single string.
    
    Returns:
        dict: A dictionary with account types (domains) as keys and lists of URLs/emails as values.
    """
    pattern = r'(https?://)?(www\.)?([a-zA-Z0-9-]+)\.[a-zA-Z]+(/\S*)?|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    accounts: Dict[str, List[str]] = {}

    matches = re.findall(pattern, text)
    for match in matches:
        full_url = ''.join(match[:4])
        email = match[4]
        if full_url:
            domain_name = match[2]
            if domain_name:
                accounts.setdefault(domain_name, []).append(full_url)
        if email:
            email_domain = email.split('@')[1].split('.')[0]
            accounts.setdefault(email_domain, []).append(email)

    return accounts


def extract_skills(extracted_sections: Dict[str, List[Dict[str, Union[str, float]]]]) -> List[str]:
    """
    Extracts skills from sections based on keywords typically used in skill section headers.

    Args:
        extracted_sections (dict): Parsed sections with font info.

    Returns:
        list: A list of skills found in the resume.
    """
    skill_section_keywords = ["Skills", "Technical Skills", "Core Competencies"]
    skills: List[str] = []
    skills_pattern = re.compile(r"(" + "|".join(skill_section_keywords) + ")", re.IGNORECASE)

    for title, content in extracted_sections.items():
        if skills_pattern.search(title):
            skills += [item["text"] for item in content if item["font_size"] < content[0]["font_size"]]

    return skills


def extract_education(sections: Dict[str, List[Dict[str, Union[str, float]]]]) -> List[str]:
    """
    Extracts education details such as degree, institution, and dates.

    Args:
        sections (dict): Parsed sections with font info.

    Returns:
        list: A list of strings containing education details.
    """
    education_pattern = re.compile(r"(Education|Academic Background)", re.IGNORECASE)
    education_list: List[str] = []

    for title, content in sections.items():
        if education_pattern.search(title):
            education_list += [item["text"] for item in content if item["font_size"] < content[0]["font_size"]]

    return education_list


def extract_certifications(sections: Dict[str, List[Dict[str, Union[str, float]]]]) -> List[str]:
    """
    Extracts certifications from sections labeled with typical certification-related titles.

    Args:
        sections (dict): Parsed sections with font info.

    Returns:
        list: A list of certification titles.
    """
    certification_section_titles = ["Certification", "Certifications", "Licenses"]
    certification_pattern = re.compile(r"(" + "|".join(certification_section_titles) + ")", re.IGNORECASE)
    certifications: List[str] = []

    for title, content in sections.items():
        if certification_pattern.search(title):
            certifications += [item["text"] for item in content if item["font_size"] < content[0]["font_size"]]

    return certifications


def extract_projects(sections: Dict[str, List[Dict[str, Union[str, float]]]]) -> List[str]:
    """
    Extracts projects from sections labeled with typical project-related titles.

    Args:
        sections (dict): Parsed sections with font info.

    Returns:
        list: A list of project titles.
    """
    project_section_titles = ["Projects", "Project Experience"]
    project_pattern = re.compile(r"(" + "|".join(project_section_titles) + ")", re.IGNORECASE)
    projects: List[str] = []

    for title, content in sections.items():
        if project_pattern.search(title):
            projects += [item["text"] for item in content if item["font_size"] < content[0]["font_size"]]

    return projects


def extract_work_experience(sections: Dict[str, List[Dict[str, Union[str, float]]]]) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Extracts work experience details including job title, company, dates, and responsibilities.

    Args:
        sections (dict): Parsed sections with font info.

    Returns:
        list: A list of dictionaries containing work experience details.
    """
    work_experience_titles = ["Work Experience", "Professional Experience", "Employment History"]
    work_experience_pattern = re.compile(r"(" + "|".join(work_experience_titles) + ")", re.IGNORECASE)
    work_experience = []

    for title, content in sections.items():
        if work_experience_pattern.search(title):
            current_entry = {
                'title': None,
                'company': None,
                'dates': None,
                'responsibilities': []
            }
            collecting_responsibilities = False

            for i, line in enumerate(content[1:]):  # Skip title
                text = line['text'].strip()
                font_size = line['font_size']
                font_name = line['font_name']

                # Determine if the font is bold
                is_bold = "Bold" in font_name

                # Detect job title (Bold and biggest font size)
                if is_bold and font_size >= 10:
                    # If a job title is already found, save the previous entry and start a new one
                    if current_entry['title']:
                        work_experience.append(current_entry)
                        current_entry = {'title': None, 'company': None, 'dates': None, 'responsibilities': []}
                    
                    current_entry['title'] = text
                    collecting_responsibilities = False

                # Detect company name (same size as title but not bold)
                elif font_size >= 10 and not is_bold and current_entry['title'] and not current_entry['company']:
                    current_entry['company'] = text
                    collecting_responsibilities = False

                # Detect dates (smaller font size, look for dates or "Present")
                elif re.search(r'\b(\d{2}/\d{4}|\d{4})\b', text) or 'Present' in text:
                    current_entry['dates'] = text
                    collecting_responsibilities = True  # Start collecting responsibilities after date

                # Collect responsibilities (smaller font size and at least 3 words)
                elif collecting_responsibilities and font_size < 10:
                    if len(text.split()) > 3:  # Check for more than three words
                        current_entry['responsibilities'].append(text)

            # Append the last work experience entry
            if current_entry['title']:
                work_experience.append(current_entry)
            break  # Break after finding the first matching section

    return work_experience
