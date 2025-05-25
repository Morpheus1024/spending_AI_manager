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

from enum import Enum

load_dotenv()

#app = FastAPI()

class Transaction_type(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    NONE = "none"

class Transaction():
    def __init__(self, data: list):
        
        self.amount = data[0] if data[0] != '' else data[1]
        # zamiana np. 99,97 zł' do 99,97
        self.amount = float(self.amount.replace(' zł', '').replace(',', '.').replace(' ', ''))
        self.type: Transaction_type =  Transaction_type.NONE
        if data[0] != '':
            self.type = Transaction_type.EXPENSE
        elif data[1] != '':
            self.type = Transaction_type.INCOME
        else:
            raise ValueError("Both income and expense are empty")
        
        self.description:str = data[3]
        self.category:str = data[2]
        self.predicted_category:str = None
        

    def __repr__(self):
        return f"Wydatek(description={self.description}, amount={self.amount}, type={self.type}, category={self.category})"

class GoogleSheetsConnector():
    def __init__(self):
        self._creds = None
        self.SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self._SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
        self.RANGE_NAME = None
        self._service = None
        self._sheet = None
        self.connected = False
        self._authenticate()

    def _authenticate(self):
        try:
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
            self.connected = True
            self._sheet = self._service.spreadsheets() # Przenieś inicjalizację sheet tutaj
        except Exception as e:
            print(f'Error during authentication: {e}')
                
    def read_data_from_sheet(self, range_name: str):
        if range_name is None:
            raise ValueError("Range name cannot be None")
        try:
            result = self._sheet.values().get(spreadsheetId=self._SPREADSHEET_ID, range=range_name).execute()
            values = result.get('values', [])  # Bezpieczny dostęp do 'values'
            list_of_transactions = []
            for value in values:
                transaction = Transaction(value)
                print(transaction)
                list_of_transactions.append(transaction)
                    
            return list_of_transactions if list_of_transactions else []  # Zwróć [] zamiast None
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
    
