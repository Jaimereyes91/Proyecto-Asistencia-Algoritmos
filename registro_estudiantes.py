import sqlite3
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('asistencia.db')
cursor = conn.cursor()

# Función para agregar un estudiante
def agregar_estudiante():
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ")
    grado = input("Grado: ")
    seccion = input("Sección (A, B, C, etc.): ")
    qr = input("Código QR: ")

    cursor.execute('''
    INSERT INTO estudiantes (nombre, apellidos, fecha_nacimiento, grado, seccion, qr)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, apellidos, fecha_nacimiento, grado, seccion, qr))

    conn.commit()
    print("Estudiante agregado exitosamente.")
    generar_qr(qr)
    generar_carne(nombre, apellidos, grado, seccion, qr)
    print(f"Carné generado para el estudiante: {qr}.png")

# Función para editar un estudiante
def editar_estudiante():
    id_estudiante = input("ID del estudiante a editar: ")
    
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nueva_fecha = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
    nuevo_grado = input("Nuevo grado: ")
    nueva_seccion = input("Nueva sección: ")
    nuevo_qr = input("Nuevo código QR: ")
    
    cursor.execute('''
    UPDATE estudiantes
    SET nombre = ?, apellidos = ?, fecha_nacimiento = ?, grado = ?, seccion = ?, qr = ?
    WHERE id = ?
    ''', (nuevo_nombre, nuevo_apellido, nueva_fecha, nuevo_grado, nueva_seccion, nuevo_qr, id_estudiante))
    
    conn.commit()
    print("Estudiante actualizado exitosamente.")
    generar_qr(nuevo_qr)
    generar_carne(nuevo_nombre, nuevo_apellido, nuevo_grado, nueva_seccion, nuevo_qr)
    print(f"Carné actualizado para el estudiante: {nuevo_qr}.png")

# Función para borrar un estudiante
def borrar_estudiante():
    id_estudiante = input("ID del estudiante a borrar: ")
    
    cursor.execute('DELETE FROM estudiantes WHERE id = ?', (id_estudiante,))
    
    conn.commit()
    print("Estudiante borrado exitosamente.")

# Función para generar el código QR
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

    ruta_carpeta = 'C:/Users/dinae/documents/GIT DOCUMENTS/qr_codes'
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    ruta_guardado = os.path.join(ruta_carpeta, f'{codigo_estudiante}.png')
    img.save(ruta_guardado)
    print(f'Código QR guardado en: {ruta_guardado}')

# Función para generar el carné
def generar_carne(nombre, apellidos, grado, seccion, codigo_qr):
    ancho, alto = 600, 300
    img = Image.new('RGB', (ancho, alto), color=(245, 245, 245))

    font_path = "arial.ttf"
    try:
        font_titulo = ImageFont.truetype(font_path, 30)
        font_texto = ImageFont.truetype(font_path, 20)
    except IOError:
        font_titulo = font_texto = ImageFont.load_default()

    draw = ImageDraw.Draw(img)
    draw.rectangle([(10, 10), (ancho-10, alto-10)], outline="black", width=5)
    draw.text((ancho//2 - 100, 20), "Carné Estudiantil", fill="darkblue", font=font_titulo)
    draw.text((20, 100), f"Nombre: {nombre}", fill="black", font=font_texto)
    draw.text((20, 140), f"Apellidos: {apellidos}", fill="black", font=font_texto)
    draw.text((20, 180), f"Grado: {grado}", fill="black", font=font_texto)
    draw.text((20, 220), f"Sección: {seccion}", fill="black", font=font_texto)

    qr_path = f'C:/Users/dinae/documents/GIT DOCUMENTS/qr_codes/{codigo_qr}.png'
    qr_img = Image.open(qr_path)
    qr_img = qr_img.resize((100, 100))
    img.paste(qr_img, (450, 100))

    ruta_carpeta = 'C:/Users/dinae/documents/GIT DOCUMENTS/carnets'
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    ruta_guardado = os.path.join(ruta_carpeta, f'{codigo_qr}_carne.png')
    img.save(ruta_guardado)
    print(f'Carné guardado en: {ruta_guardado}')

# Menú principal para elegir acciones
def menu():
    while True:
        print("\n1. Agregar estudiante")
        print("2. Editar estudiante")
        print("3. Borrar estudiante")
        print("4. Salir")
        
        opcion = input("Elija una opción: ")
        
        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            editar_estudiante()
        elif opcion == "3":
            borrar_estudiante()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
if __name__ == "__main__":
    menu()

# Cerrar la conexión al finalizar
conn.close()
