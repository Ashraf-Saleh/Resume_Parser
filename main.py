"""
Resume Parser Script

This Python script parses a resume PDF document and extracts key information, including:
    1. Full Name
    2. Contact Information (e.g., email, phone, LinkedIn)
    3. Summary or Objective statement
    4. Skills (as a list)
    5. Work Experience (including company, job title, dates, and responsibilities)
    6. Education (degree, institution, dates, and additional information)
    7. Certifications (if present)
    8. Projects (if present)

The parser is designed to be flexible and robust to variations in resume formats. It uses text 
extraction libraries (e.g., pdfminer) to convert PDF content into structured text, which it then 
processes using regular expressions and keyword-based logic to identify and extract relevant sections. 

Libraries:
    - pdfminer: For PDF text extraction.
    - re: For regular expressions used to identify key sections of the resume.

Assumptions:
    - Each section is headed by common titles such as "Skills", "Work Experience", "Education", 
      or "Certifications". The parser identifies sections based on these titles and gathers data until 
      the next title or the end of the document.
    - Contact details like email and phone numbers are located near the beginning of the document.
    - Not all resumes contain all sections; the parser handles missing information gracefully by 
      returning empty fields for absent sections.

Challenges:
    - Variations in resume layouts: To address inconsistencies across resume formats, the parser 
      uses flexible regex patterns and general keywords for section identification.
    - Two-column layouts and non-linear text extraction: PDFs can store text non-linearly, especially 
      in multi-column formats. This parser is designed to mitigate these issues, but complex layouts 
      may still require further handling.

Usage:
    To run this script, pass a resume PDF file to the main function. The function will output a 
    structured dictionary containing the parsed information.

"""
