"""
utils/pdf_reader.py
====================
Extracts text content from uploaded PDF files.
Handles common edge cases like empty pages, encrypted PDFs, and bad uploads.

Uses PyPDF2 (legacy fallback) and pypdf (modern) for broad compatibility.
"""

import io
from typing import Tuple, Optional


def extract_text_from_pdf(uploaded_file) -> Tuple[str, Optional[str]]:
    """
    Extract all text from a Streamlit-uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object (from st.file_uploader)

    Returns:
        Tuple of (extracted_text: str, error_message: Optional[str])
        If extraction succeeds, error_message is None.
        If extraction fails, extracted_text is "" and error_message explains why.
    """
    try:
        # Read the file bytes into memory (Streamlit provides a file-like object)
        file_bytes = uploaded_file.read()

        # Validate size (10MB limit)
        if len(file_bytes) > 10 * 1024 * 1024:
            return "", "File too large. Please upload a PDF under 10MB."

        # Validate it's actually a PDF (PDF files start with %PDF)
        if not file_bytes.startswith(b"%PDF"):
            return "", "Invalid file. Please upload a valid PDF document."

        # Try pypdf first (newer, better maintained)
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))

            # Check for encryption
            if reader.is_encrypted:
                return "", "PDF is password-protected. Please upload an unencrypted PDF."

            text_parts = []
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                except Exception:
                    # Skip pages that fail to extract; continue with others
                    continue

            full_text = "\n\n".join(text_parts)

        except ImportError:
            # Fallback to PyPDF2 if pypdf not available
            import PyPDF2

            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))

            if reader.is_encrypted:
                return "", "PDF is password-protected. Please upload an unencrypted PDF."

            text_parts = []
            for page in reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                except Exception:
                    continue

            full_text = "\n\n".join(text_parts)

        # Clean up the extracted text
        full_text = clean_text(full_text)

        if not full_text.strip():
            return "", (
                "No readable text found in this PDF. "
                "It may be a scanned/image-only PDF. "
                "Please use a text-based PDF or convert it first."
            )

        return full_text, None

    except Exception as e:
        return "", f"Unexpected error reading PDF: {str(e)}"


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text by removing common artifacts.

    PDF extraction often introduces:
    - Extra whitespace
    - Repeated newlines
    - Strange unicode characters from encoding issues
    """
    if not text:
        return ""

    import re

    # Replace multiple spaces with single space
    text = re.sub(r" {2,}", " ", text)

    # Replace 3+ newlines with double newline (preserve paragraph structure)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove null bytes and other control characters (except newlines/tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    return text.strip()


def get_resume_metadata(uploaded_file) -> dict:
    """
    Extract metadata from a PDF (author, creation date, etc.)
    Returns a dict with whatever metadata is available.
    """
    metadata = {}
    try:
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset the file pointer after reading

        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))

        if reader.metadata:
            meta = reader.metadata
            metadata["author"]   = meta.get("/Author", "Unknown")
            metadata["creator"]  = meta.get("/Creator", "Unknown")
            metadata["pages"]    = len(reader.pages)
    except Exception:
        pass

    return metadata
