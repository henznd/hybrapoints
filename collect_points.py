import os
import json
import requests
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Paramètres
WALLET = "0x19bF8d22f9772b1F349a803e5B640087f3d29C2a"
SHEET_ID = "1dqAx5719sRx_J1Ce34Of0eIXCk275wyLcJcIusIRMwg"
SHEET_NAME = "Sheet1"

# Récupérer les credentials du compte de service depuis la variable d'environnement
creds_json = os.environ.get("GOOGLE_SHEETS_CREDS")
if not creds_json:
    raise Exception("La variable d'environnement GOOGLE_SHEETS_CREDS n'est pas définie.")
creds_dict = json.loads(creds_json)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)

# Ouvrir le Google Sheet
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.worksheet(SHEET_NAME)

# Appel API Hybra
url = f"https://server.hybra.finance/api/points/user/{WALLET}"
resp = requests.get(url)
data = resp.json()["data"]
total_points = data["totalPoints"]
rank = data["rank"]

# Timestamp actuel (UTC)
timestamp = datetime.utcnow().isoformat()

# Ajouter la ligne dans le Google Sheet
worksheet.append_row([timestamp, total_points, rank])
print(f"Ajouté : {timestamp}, {total_points}, {rank}") 