"""
Main script to handle resume parsing using the 'resume_parser' library.

This script parses a resume from a PDF file and extracts key sections into a dictionary.
The sections include:
- Name
- Summary
- Accounts (URLs and Emails)
- Skills
- Education
- Certifications
- Projects
- Work Experience

All extracted sections are stored in a dictionary for easy access.

Usage:
    - Manually set the PDF file path in the 'pdf_path' variable.
"""

import os
from resume_parser import (
    extract_text_from_pdf,
    extract_sections_with_font_info,
    extract_name,
    extract_summary,
    extract_accounts_from_resume,
    extract_skills,
    extract_education,
    extract_certifications,
    extract_projects,
    extract_work_experience
)

def parse_resume(pdf_path: str) -> dict:
    """
    Parses the resume from the provided PDF file and extracts key sections into a dictionary.

    Args:
        pdf_path (str): The path to the PDF file containing the resume.

    Returns:
        dict: A dictionary containing the extracted sections of the resume.
    """
    # Extract text from the resume PDF
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Extract sections with font information (for structured parsing)
    print("Extracting sections with font information...")
    sections = extract_sections_with_font_info(pdf_path)

    # Extract information for each section
    resume_data = {}

    # Extract name
    print("Extracting name...")
    name = extract_name(text)
    resume_data['Name'] = name if name else "Not found"

    # Extract summary
    print("Extracting summary...")
    summary = extract_summary(text)
    resume_data['Summary'] = summary if summary else "Not found"

    # Extract accounts (URLs, emails)
    print("Extracting accounts (URLs and emails)...")
    accounts = extract_accounts_from_resume(text)
    resume_data['Accounts'] = accounts if accounts else "Not found"

    # Extract skills
    print("Extracting skills...")
    skills = extract_skills(sections)
    resume_data['Skills'] = skills if skills else "Not found"

    # Extract education
    print("Extracting education...")
    education = extract_education(sections)
    resume_data['Education'] = education if education else "Not found"

    # Extract certifications
    print("Extracting certifications...")
    certifications = extract_certifications(sections)
    resume_data['Certifications'] = certifications if certifications else "Not found"

    # Extract projects
    print("Extracting projects...")
    projects = extract_projects(sections)
    resume_data['Projects'] = projects if projects else "Not found"

    # Extract work experience
    print("Extracting work experience...")
    work_experience = extract_work_experience(sections)
    resume_data['Work Experience'] = work_experience if work_experience else "Not found"

    return resume_data

def main():
    """
    Main function that parses the resume PDF and outputs the extracted sections in a dictionary.

    The function uses the manually assigned 'pdf_path' variable to specify the PDF file.
    It returns a dictionary of extracted sections and prints it.
    """
    # Manually set the path to your resume PDF here
    pdf_path = "data/Sample Resume for Assessment.pdf"  # Replace with the actual path to your resume PDF

    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return

    # Parse the resume and get the extracted sections
    resume_data = parse_resume(pdf_path)

    # Print the extracted resume data in a readable format
    print("\nExtracted Resume Data:")
    print("-" * 40)
    for section, content in resume_data.items():
        print(f"{section}: {content}")
    print("-" * 40)

if __name__ == "__main__":
    main()
