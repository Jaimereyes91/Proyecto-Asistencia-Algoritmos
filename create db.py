import sqlite3

conn = sqlite3.connect('asistencia.db')
cursor = conn.cursor()

#TABLA DE REGISTRO DE ESTUDIANTES
cursor.execute('''
CREATE TABLE IF NOT EXISTS estudiantes ( 
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    grado TEXT NOT NULL,
    seccion CHAR(1) NOT NULL,
    qr TEXT UNIQUE NOT NULL
)
''')

#TABLA DE REGISTRO DE ASISTENCIA
cursor.execute('''
CREATE TABLE IF NOT EXISTS asistencia (
    id INTEGER PRIMARY KEY,
    estudiante_id INTEGER,
    fecha TEXT NOT NULL,
    hora_entrada TEXT,
    hora_salida TEXT,
    FOREIGN KEY(estudiante_id) REFERENCES estudiantes(id)
)
''')

conn.commit()
conn.close()
