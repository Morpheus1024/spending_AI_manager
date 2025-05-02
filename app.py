from google_sheet_API import GoogleSheetsConnector

if __name__ == "__main__":
    # Initialize the Google Sheet API
    connector = GoogleSheetsConnector()
    print(connector.connected)
    
    connector.RANGE_NAME = 'Marzec 2025!H4:K98'
    data = connector.read_data_from_sheet(connector.RANGE_NAME)
    
    # print(data)