import io
import email
from typing import Optional

class FileParser:
    """Parses various file formats to extract text."""
    
    @staticmethod
    def parse_file(uploaded_file) -> Optional[str]:
        """
        Extract text from an uploaded file.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Extracted text string or None if failed
        """
        try:
            file_type = uploaded_file.type
            file_name = uploaded_file.name.lower()
            
            if "pdf" in file_type or file_name.endswith(".pdf"):
                return FileParser._parse_pdf(uploaded_file)
            elif "message/rfc822" in file_type or file_name.endswith(".eml"):
                return FileParser._parse_eml(uploaded_file)
            elif "text/plain" in file_type or file_name.endswith(".txt"):
                return FileParser._parse_txt(uploaded_file)
            else:
                return None
        except Exception as e:
            print(f"Error parsing file: {e}")
            return None

    @staticmethod
    def _parse_txt(uploaded_file) -> str:
        return uploaded_file.getvalue().decode("utf-8")

    @staticmethod
    def _parse_eml(uploaded_file) -> str:
        bytes_content = uploaded_file.getvalue()
        msg = email.message_from_bytes(bytes_content)
        
        # Extract subject and body
        subject = msg.get("subject", "")
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()
            
        return f"Subject: {subject}\n\n{body}"

    @staticmethod
    def _parse_pdf(uploaded_file) -> str:
        # Try importing PyPDF2, handle if missing
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            return "Error: PyPDF2 not installed. Please install it to parse PDFs."
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
