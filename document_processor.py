import PyPDF2
import docx
import os

class DocumentProcessor:
    @staticmethod
    def read_pdf(file_path):
        """Read content from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content = ""
                
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
                
                return content
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return None
    
    @staticmethod
    def read_docx(file_path):
        """Read content from DOCX file"""
        try:
            doc = docx.Document(file_path)
            content = ""
            
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
                
            return content
        except Exception as e:
            print(f"Error reading DOCX: {str(e)}")
            return None
    
    @staticmethod
    def read_text_file(file_path):
        """Read content from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file: {str(e)}")
            return None
    
    @staticmethod
    def get_document_content(file_path):
        """Get content from document based on file extension"""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return DocumentProcessor.read_pdf(file_path)
        elif file_extension == '.docx':
            return DocumentProcessor.read_docx(file_path)
        elif file_extension in ['.txt', '.md']:
            return DocumentProcessor.read_text_file(file_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            return None
