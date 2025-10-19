import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]


creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Заменить tablica на название вашей таблицы
sheet = client.open("tablica").sheet1

# Можно настроить на то, что нужно
def append_report(report_fio: str, report_cabinet: str, report_description: str):
    try:
        sheet.append_row([report_fio, report_cabinet, report_description])
        print("✅ Запись успешно добавлена в Google Sheets")
    except Exception as e:
        print(f"⚠️ Ошибка при добавлении в Google Sheets: {e}")