
import json
from pathlib import Path
from io import BytesIO

from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv


# Load environment variables from the project
load_dotenv()

from pathlib import Path
from pypdf import PdfReader


def read_pdf(pdf_path: Path) -> str:
    """Extract plain text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("No readable text found in PDF")

    return text


def parse_resume(pdf_bytes: bytes) -> dict:
    """Extract text from a PDF and convert it into structured JSON."""

    # Step 1: Extract text from PDF
    reader = PdfReader(BytesIO(pdf_bytes))
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    if not resume_text.strip():
        raise ValueError(
            "No readable text found in PDF. "
            "The PDF might be scanned or image-based."
        )

    print("\n--- Extracted Resume Text ---")
    print(resume_text)

    # Step 2: Initialize Groq client
    client = Groq()

    # Step 3: Ask AI to parse the resume
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert resume parser.

Convert the provided resume into valid JSON using this structure:

{
    "personal_info": {
        "name": null,
        "email": null,
        "phone": null
    },
    "skills": [],
    "experience": [
        {
            "company": null,
            "role": null,
            "duration": null,
            "description": null,
            "skills_used": []
        }
    ],
    "education": [],
    "projects": [],
    "achievements": []
}

Rules:
- Extract all relevant information.
- Keep each experience entry separate.
- Do not invent or assume information.
- Use null for missing scalar values.
- Use empty arrays for missing lists.
- Return valid JSON only.
"""
            },
            {
                "role": "user",
                "content": resume_text
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    # Step 4: Convert JSON string into a Python dictionary
    result = json.loads(response.choices[0].message.content)

    # Step 5: Display parsed JSON
    print("\n--- Parsed Resume JSON ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    return result


if __name__ == "__main__":
    # Automatically locate PDF files in the backend folder
    backend_folder = Path(__file__).parent
    pdf_files = sorted(backend_folder.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the backend folder.")
        print(f"Folder checked: {backend_folder}")

    elif len(pdf_files) == 1:
        pdf_path = pdf_files[0]

        print(f"Resume found: {pdf_path.name}")
        print("Starting resume parsing...")

        try:
            result = parse_resume(pdf_path.read_bytes())

            # Save the parsed result as JSON
            output_path = backend_folder / "parsed_resume.json"
            output_path.write_text(
                json.dumps(result, indent=4, ensure_ascii=False),
                encoding="utf-8"
            )

            print("\nResume converted into JSON successfully!")
            print(f"JSON saved to: {output_path}")

        except Exception as error:
            print(f"\nResume parsing failed: {error}")

    else:
        print("Multiple PDF files found. Please keep only one resume PDF")
        print("in the backend folder to avoid selecting the wrong file.")

        for pdf_path in pdf_files:
            print(f" - {pdf_path.name}")
