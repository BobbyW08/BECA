"""
Google Drive Manager for BECA
Provides integration with Google Drive for file operations
"""
import os
import io
from typing import List, Dict, Optional
from pathlib import Path


class GoogleDriveManager:
    """Manages Google Drive operations"""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.service = None
        self.authenticated = False
        
    def authenticate(self) -> tuple[bool, str]:
        """
        Authenticate with Google Drive API
        
        Returns:
            Tuple of (success, message)
        """
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            import pickle
            
            SCOPES = ['https://www.googleapis.com/auth/drive']
            
            creds = None
            # Token file stores user's access and refresh tokens
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials, let user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        return False, f"Credentials file not found: {self.credentials_file}"
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('drive', 'v3', credentials=creds)
            self.authenticated = True
            return True, "Successfully authenticated with Google Drive"
            
        except ImportError:
            return False, "Required libraries not installed. Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client"
        except Exception as e:
            return False, f"Authentication error: {str(e)}"
    
    def list_files(self, folder_id: Optional[str] = None, max_results: int = 100) -> Dict:
        """
        List files in Google Drive
        
        Args:
            folder_id: Optional folder ID to list files from (None for root)
            max_results: Maximum number of files to return
            
        Returns:
            Dict with success, files list, error
        """
        if not self.authenticated:
            return {'success': False, 'files': [], 'error': 'Not authenticated'}
        
        try:
            query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
            query += " and trashed=false"
            
            results = self.service.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime, size, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            return {
                'success': True,
                'files': files,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'files': [],
                'error': str(e)
            }
    
    def search_files(self, query: str, max_results: int = 50) -> Dict:
        """
        Search for files in Google Drive
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            Dict with success, files list, error
        """
        if not self.authenticated:
            return {'success': False, 'files': [], 'error': 'Not authenticated'}
        
        try:
            search_query = f"name contains '{query}' and trashed=false"
            
            results = self.service.files().list(
                q=search_query,
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime, size, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            return {
                'success': True,
                'files': files,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'files': [],
                'error': str(e)
            }
    
    def download_file(self, file_id: str, destination: str) -> tuple[bool, str]:
        """
        Download a file from Google Drive
        
        Args:
            file_id: Google Drive file ID
            destination: Local destination path
            
        Returns:
            Tuple of (success, message)
        """
        if not self.authenticated:
            return False, "Not authenticated"
        
        try:
            from googleapiclient.http import MediaIoBaseDownload
            
            request = self.service.files().get_media(fileId=file_id)
            
            destination_path = Path(destination)
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(destination_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            
            return True, f"Downloaded to: {destination}"
            
        except Exception as e:
            return False, f"Download error: {str(e)}"
    
    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> tuple[bool, str, Optional[str]]:
        """
        Upload a file to Google Drive
        
        Args:
            file_path: Local file path to upload
            folder_id: Optional folder ID to upload to
            
        Returns:
            Tuple of (success, message, file_id)
        """
        if not self.authenticated:
            return False, "Not authenticated", None
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            file_path = Path(file_path)
            if not file_path.exists():
                return False, f"File not found: {file_path}", None
            
            file_metadata = {
                'name': file_path.name
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(str(file_path), resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            return True, f"Uploaded successfully. Link: {file.get('webViewLink')}", file.get('id')
            
        except Exception as e:
            return False, f"Upload error: {str(e)}", None
    
    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> tuple[bool, str, Optional[str]]:
        """
        Create a folder in Google Drive
        
        Args:
            folder_name: Name of the folder to create
            parent_id: Optional parent folder ID
            
        Returns:
            Tuple of (success, message, folder_id)
        """
        if not self.authenticated:
            return False, "Not authenticated", None
        
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, webViewLink'
            ).execute()
            
            return True, f"Folder created. Link: {folder.get('webViewLink')}", folder.get('id')
            
        except Exception as e:
            return False, f"Error creating folder: {str(e)}", None
    
    def sync_folder(self, local_folder: str, drive_folder_id: Optional[str] = None, 
                   direction: str = 'upload') -> Dict:
        """
        Sync a local folder with Google Drive
        
        Args:
            local_folder: Local folder path
            drive_folder_id: Google Drive folder ID (None for root)
            direction: 'upload', 'download', or 'both'
            
        Returns:
            Dict with sync results
        """
        if not self.authenticated:
            return {'success': False, 'error': 'Not authenticated'}
        
        results = {
            'uploaded': [],
            'downloaded': [],
            'errors': []
        }
        
        local_path = Path(local_folder)
        
        try:
            if direction in ['upload', 'both']:
                # Upload local files
                for file_path in local_path.rglob('*'):
                    if file_path.is_file():
                        success, message, file_id = self.upload_file(
                            str(file_path), 
                            drive_folder_id
                        )
                        if success:
                            results['uploaded'].append(str(file_path))
                        else:
                            results['errors'].append(f"{file_path}: {message}")
            
            if direction in ['download', 'both']:
                # Download Drive files
                drive_files = self.list_files(drive_folder_id)
                if drive_files['success']:
                    for file in drive_files['files']:
                        destination = local_path / file['name']
                        success, message = self.download_file(
                            file['id'], 
                            str(destination)
                        )
                        if success:
                            results['downloaded'].append(file['name'])
                        else:
                            results['errors'].append(f"{file['name']}: {message}")
            
            return {
                'success': True,
                'results': results,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'results': results,
                'error': str(e)
            }


# Global Google Drive manager instance
drive_manager = GoogleDriveManager()
