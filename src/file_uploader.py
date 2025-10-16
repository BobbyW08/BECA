"""
File Uploader for BECA
Handles various file types and extracts content for processing
"""
import os
import io
from typing import Dict, Optional, Tuple
from pathlib import Path


class FileUploader:
    """Handles file uploads and content extraction"""
    
    SUPPORTED_EXTENSIONS = {
        # Text files
        '.txt', '.md', '.markdown', '.rst',
        # Code files
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
        '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
        # Web files
        '.html', '.htm', '.css', '.scss', '.sass', '.less',
        # Config files
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
        '.xml', '.env',
        # Data files
        '.csv', '.tsv',
        # Documentation
        '.pdf', '.docx', '.doc',
        # Spreadsheets
        '.xlsx', '.xls',
        # Images (for OCR or analysis)
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'
    }
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
    def is_supported(self, filename: str) -> bool:
        """Check if file type is supported"""
        ext = Path(filename).suffix.lower()
        return ext in self.SUPPORTED_EXTENSIONS
    
    def save_upload(self, file_data, filename: str) -> Tuple[bool, str, Optional[Path]]:
        """
        Save uploaded file to uploads directory
        
        Returns:
            Tuple of (success, message, file_path)
        """
        try:
            if not self.is_supported(filename):
                ext = Path(filename).suffix
                return False, f"Unsupported file type: {ext}", None
            
            # Create unique filename if file exists
            file_path = self.upload_dir / filename
            if file_path.exists():
                base = file_path.stem
                ext = file_path.suffix
                counter = 1
                while file_path.exists():
                    file_path = self.upload_dir / f"{base}_{counter}{ext}"
                    counter += 1
            
            # Save file
            if isinstance(file_data, bytes):
                file_path.write_bytes(file_data)
            else:
                # Assume it's a file-like object
                with open(file_path, 'wb') as f:
                    f.write(file_data.read() if hasattr(file_data, 'read') else file_data)
            
            return True, f"File uploaded successfully: {file_path.name}", file_path
            
        except Exception as e:
            return False, f"Error saving file: {str(e)}", None
    
    def extract_content(self, file_path: Path) -> Dict[str, any]:
        """
        Extract content from uploaded file based on type
        
        Returns:
            Dict with 'success', 'content', 'metadata', 'error'
        """
        try:
            ext = file_path.suffix.lower()
            
            # Text-based files
            if ext in {'.txt', '.md', '.markdown', '.rst', '.py', '.js', '.ts',
                      '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp', '.cs',
                      '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
                      '.html', '.htm', '.css', '.scss', '.sass', '.less',
                      '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
                      '.xml', '.env'}:
                return self._extract_text(file_path)
            
            # CSV files
            elif ext in {'.csv', '.tsv'}:
                return self._extract_csv(file_path)
            
            # PDF files
            elif ext == '.pdf':
                return self._extract_pdf(file_path)
            
            # Word documents
            elif ext in {'.docx', '.doc'}:
                return self._extract_docx(file_path)
            
            # Excel files
            elif ext in {'.xlsx', '.xls'}:
                return self._extract_excel(file_path)
            
            # Images
            elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}:
                return self._extract_image_info(file_path)
            
            # SVG (text-based)
            elif ext == '.svg':
                return self._extract_text(file_path)
            
            else:
                return {
                    'success': False,
                    'content': None,
                    'error': f'No extractor for {ext} files'
                }
                
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'error': str(e)
            }
    
    def _extract_text(self, file_path: Path) -> Dict:
        """Extract plain text content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'metadata': {
                    'type': 'text',
                    'size': len(content),
                    'lines': content.count('\n') + 1
                },
                'error': None
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def _extract_csv(self, file_path: Path) -> Dict:
        """Extract CSV content"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            
            # Convert to markdown table for better readability
            content = df.to_markdown(index=False)
            
            return {
                'success': True,
                'content': content,
                'metadata': {
                    'type': 'csv',
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns)
                },
                'error': None
            }
        except ImportError:
            # Fallback to basic CSV reading
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                'success': True,
                'content': content,
                'metadata': {'type': 'csv'},
                'error': 'pandas not available, showing raw CSV'
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def _extract_pdf(self, file_path: Path) -> Dict:
        """Extract PDF content"""
        try:
            import PyPDF2
            
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                
                content = '\n\n'.join(text)
                
                return {
                    'success': True,
                    'content': content,
                    'metadata': {
                        'type': 'pdf',
                        'pages': len(reader.pages)
                    },
                    'error': None
                }
        except ImportError:
            return {
                'success': False,
                'content': None,
                'error': 'PyPDF2 not installed. Run: pip install PyPDF2'
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def _extract_docx(self, file_path: Path) -> Dict:
        """Extract Word document content"""
        try:
            import docx
            
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            content = '\n\n'.join(paragraphs)
            
            return {
                'success': True,
                'content': content,
                'metadata': {
                    'type': 'docx',
                    'paragraphs': len(paragraphs)
                },
                'error': None
            }
        except ImportError:
            return {
                'success': False,
                'content': None,
                'error': 'python-docx not installed. Run: pip install python-docx'
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def _extract_excel(self, file_path: Path) -> Dict:
        """Extract Excel content"""
        try:
            import pandas as pd
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_content = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_content.append(f"## Sheet: {sheet_name}\n\n{df.to_markdown(index=False)}")
            
            content = '\n\n'.join(sheets_content)
            
            return {
                'success': True,
                'content': content,
                'metadata': {
                    'type': 'excel',
                    'sheets': len(excel_file.sheet_names),
                    'sheet_names': excel_file.sheet_names
                },
                'error': None
            }
        except ImportError:
            return {
                'success': False,
                'content': None,
                'error': 'pandas and openpyxl not installed. Run: pip install pandas openpyxl'
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def _extract_image_info(self, file_path: Path) -> Dict:
        """Extract image information (basic metadata)"""
        try:
            from PIL import Image
            
            with Image.open(file_path) as img:
                return {
                    'success': True,
                    'content': f"Image file: {file_path.name}\nSize: {img.size[0]}x{img.size[1]}\nFormat: {img.format}\nMode: {img.mode}",
                    'metadata': {
                        'type': 'image',
                        'width': img.size[0],
                        'height': img.size[1],
                        'format': img.format,
                        'mode': img.mode
                    },
                    'error': 'Note: OCR not implemented. Install pytesseract for text extraction from images.'
                }
        except ImportError:
            return {
                'success': True,
                'content': f"Image file: {file_path.name}",
                'metadata': {'type': 'image'},
                'error': 'Pillow not installed. Run: pip install Pillow'
            }
        except Exception as e:
            return {'success': False, 'content': None, 'error': str(e)}
    
    def process_upload(self, file_data, filename: str) -> Dict:
        """
        Complete upload and extraction process
        
        Returns:
            Dict with success, message, content, metadata
        """
        # Save file
        success, message, file_path = self.save_upload(file_data, filename)
        
        if not success:
            return {
                'success': False,
                'message': message,
                'content': None,
                'metadata': None
            }
        
        # Extract content
        extraction = self.extract_content(file_path)
        
        return {
            'success': extraction['success'],
            'message': message,
            'content': extraction.get('content'),
            'metadata': extraction.get('metadata'),
            'file_path': str(file_path),
            'error': extraction.get('error')
        }


# Global file uploader instance
file_uploader = FileUploader()
