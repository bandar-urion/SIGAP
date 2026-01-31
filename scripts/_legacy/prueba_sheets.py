import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Definir credenciales y alcance (Scope)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)

# 2. Autenticar al cliente
client = gspread.authorize(creds)

# 3. Abrir tu hoja de cálculo
# Asegúrate de que el nombre sea EXACTO al de tu archivo en Google Drive
sheet = client.open("ControlGastos").sheet1  # .sheet1 selecciona la primera pestaña

# 4. Leer datos (Prueba de lectura)
print("Leyendo la celda A1...")
valor_a1 = sheet.acell('A1').value
print(f"El valor en A1 es: {valor_a1}")

# 5. Escribir datos (Prueba de escritura)
print("Escribiendo en la celda B2...")
sheet.update_acell('B2', '¡Hola desde Python, Martín!')
print("¡Escritura completada!")