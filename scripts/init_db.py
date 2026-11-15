import sqlite3

def inicializar_bd():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    
    # Tabla 1: categoria_servicio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categoria_servicio (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')
    
    # Tabla 2: institucion
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institucion (
            id_institucion INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_reps TEXT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL,
            telefono TEXT,
            naturaleza_juridica TEXT,
            fecha_verificacion TEXT
        )
    ''')
    
    # Tabla 3: institucion_categoria (Relación muchos a muchos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institucion_categoria (
            id_institucion INTEGER,
            id_categoria INTEGER,
            tipo_atencion TEXT,
            PRIMARY KEY (id_institucion, id_categoria),
            FOREIGN KEY (id_institucion) REFERENCES institucion(id_institucion),
            FOREIGN KEY (id_categoria) REFERENCES categoria_servicio(id_categoria)
        )
    ''')
    
    # Tabla 4: horario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horario (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_institucion INTEGER,
            id_categoria INTEGER,
            dia TEXT,
            hora_apertura TEXT,
            hora_cierre TEXT,
            atencion_24h INTEGER,
            FOREIGN KEY (id_institucion, id_categoria) REFERENCES institucion_categoria(id_institucion, id_categoria)
        )
    ''')
    
    conexion.commit()
    conexion.close()
    print("¡Base de datos y tablas creadas exitosamente!")

if __name__ == '__main__':
    inicializar_bd()
    