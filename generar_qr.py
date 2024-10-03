import qrcode
import os

def generar_qr(codigo_estudiante):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(codigo_estudiante)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Definir la ruta donde se guardará el código QR
    ruta_carpeta = 'C:/Users/dinae/documents/GIT DOCUMENTS/qr_codes'
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)  # Crear la carpeta si no existe

    # Guardar el archivo en la carpeta
    ruta_guardado = os.path.join(ruta_carpeta, f'{codigo_estudiante}.png')
    img.save(ruta_guardado)
    print(f'Código QR guardado en: {ruta_guardado}')

# Probar la función
if __name__ == "__main__":
    codigo = input("Introduce el código del estudiante: ")
    generar_qr(codigo)
    print(f"Código QR generado para el estudiante: {codigo}.png")
