from __future__ import print_function

import os.path

from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

app = FastAPI()

class GoogleSheetsConnector():
    def __init__(self):
        self._creds = None
        self.SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self._SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
        self.RANGE_NAME = None
        self._service = None
        self._sheet = None
        self._authenticate()

    def _authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPE)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPE)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self._service = build('sheets', 'v4', credentials=self.creds)  # Przenieś inicjalizację service tutaj
        self._sheet = self._service.spreadsheets() # Przenieś inicjalizację sheet tutaj
                
    def read_data_from_sheet(self, range_name: str):
        if range_name is None:
            raise ValueError("Range name cannot be None")
        try:
            result = self._sheet.values().get(spreadsheetId=self._SPREADSHEET_ID, range=range_name).execute()
            values = result.get('values', [])  # Bezpieczny dostęp do 'values'
            return values if values else []  # Zwróć [] zamiast None
        except HttpError as err:
            print(f'Error reading sheet data: {err}')  # Loguj błąd
            return []  # Zwróć pustą listę w przypadku błędu
        
    
def get_google_sheet_connector() -> GoogleSheetsConnector:
    return GoogleSheetsConnector()
    
class TransactionData(BaseModel):
    description:str
    amount:float
    date:str
    category: Optional[str] = None
    
class PredictionResult(BaseModel):
    description: str
    prediction_category: str
    

@app.get("/transactions", response_model=List[PredictionResult])
async def get_transactions_and_categorize(
    sheet_connector: GoogleSheetsConnector = Depends(get_google_sheet_connector),
    range_name: str = "Marzec 2025!H4:K99"  # Zakres danych do odczytu
):
    values = sheet_connector.read_data_from_sheet(range_name)
    transactions: List[TransactionData] = []
    
    if not values: return []
    
    for row in values:
        try:
            spend = row[0]
            earn = row[1]
            category = row[2]
            description = row[3]
            transactions.append(
                TransactionData(
                    description=row[2],
                    amount=(row[1]),
                    transaction_data = row[2],
                )
            )
        except IndexError as e:
            print(f"Error processing row {row}: {e}")
            continue
                
    
                
