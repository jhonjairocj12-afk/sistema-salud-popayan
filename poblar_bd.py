import sqlite3

def poblar_datos():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    
    # 1. Insertar categorías de servicio estándar
    categorias = [
        (1, 'Consulta médica'),
        (2, 'Urgencias'),
        (3, 'Salud mental'),
        (4, 'Atención materna')
    ]
    cursor.executemany("INSERT OR IGNORE INTO categoria_servicio (id_categoria, nombre) VALUES (?, ?)", categorias)
    
    # 2. Insertar las instituciones reales de la tabla aprobada
    instituciones = [
        (1, '1900100031', 'Hospital Universitario San José ESE', 'Cra. 6 #10N-142 (Barrio Bolívar)', 2.44991, -76.59992, '(602) 8234508', 'Pública', '2026-11-06'),
        (2, '1900100023', 'Hospital Susana López de Valencia', 'Calle 15 # 17A - 196 (Barrio La Ladera)', 2.437922, -76.619333, '(602) 8386363', 'Pública', '2026-11-06'),
        (3, '1900107025', 'Clínica la Estancia S.A', 'Calle 15N # 2-350 (Barrio La Estancia)', 2.450601, -76.597378, '(602) 833 1000', 'Privada', '2026-11-06'),
        (4, '1900109488', 'Clínica San Rafael de Popayán', 'Calle 18a Norte #5-20 (Barrio La Estancia)', 2.451736, -76.596600, '(602) 835 3810', 'Privada', '2026-11-06'),
        (5, '1900108297', 'Clínica Santa Gracia', 'Calle 15 N # 15-46 (Comuna 1)', 2.459317, -76.602837, '(602) 8375808', 'Privada', '2026-11-06')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO institucion (id_institucion, codigo_reps, nombre, direccion, latitud, longitud, telefono, naturaleza_juridica, fecha_verificacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', instituciones)
    
    # 3. Relacionar instituciones con servicios (por defecto las asociamos a Urgencias y Consulta médica para pruebas)
    relaciones = [
        (1, 2, '24 Horas'), # San José - Urgencias
        (1, 1, 'Lunes a Viernes'), # San José - Consulta
        (2, 2, '24 Horas'), # Susana López - Urgencias
        (3, 2, '24 Horas'), # La Estancia - Urgencias
        (3, 1, 'Lunes a Sábado'), # La Estancia - Consulta
        (4, 2, '24 Horas'), # San Rafael - Urgencias
        (5, 1, 'Lunes a Sábado') # Santa Gracia - Consulta
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO institucion_categoria (id_institucion, id_categoria, tipo_atencion)
        VALUES (?, ?, ?)
    ''', relaciones)
    
    conexion.commit()
    conexion.close()
    print("¡Base de datos poblada con las 5 instituciones reales de Popayán exitosamente!")

if __name__ == '__main__':
    poblar_datos()
    