import streamlit as st
import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Servicios de salud en Popayán",
    page_icon="🏥",
    layout="wide"
)

def conectar_bd():
    return sqlite3.connect('database.db')

import requests

def obtener_ruta_osrm(origen_coords, destino_coords):
    """
    Calcula la ruta real, distancia y tiempo estimado usando OSRM (Gratuito).
    origen_coords: (lat, lon)
    destino_coords: (lat, lon)
    """
    try:
        # OSRM recibe las coordenadas en formato lon,lat
        url = f"http://router.project-osrm.org/route/v1/driving/{origen_coords[1]},{origen_coords[0]};{destino_coords[1]},{destino_coords[0]}?overview=full&geometries=geojson"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['routes']:
                route = data['routes'][0]
                duracion_segundos = route['duration'] # Duración en segundos
                distancia_metros = route['distance']   # Distancia en metros
                
                # Coordenadas de la ruta para dibujar la línea (viene como [lon, lat], Folium necesita [lat, lon])
                geometria = route['geometry']['coordinates']
                coordenadas_ruta = [[coord[1], coord[0]] for coord in geometria]
                
                minutos = round(duracion_segundos / 60)
                km = round(distancia_metros / 1000, 2)
                
                return coordenadas_ruta, minutos, km
    except Exception as e:
        print(f"Error consultando OSRM: {e}")
    
    return None, 0, 0

# Inicializar estados de navegación y variables de sesión
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'
if 'categoria_seleccionada' not in st.session_state:
    st.session_state.categoria_seleccionada = None
if 'institucion_seleccionada' not in st.session_state:
    st.session_state.institucion_seleccionada = None
if 'direccion_usuario' not in st.session_state:
    st.session_state.direccion_usuario = ""
if 'coords_usuario' not in st.session_state:
    st.session_state.coords_usuario = (2.4447, -76.6057)

def geocodificar_direccion(direccion):
    try:
        geolocator = Nominatim(user_agent="sistema_salud_popayan")
        location = geolocator.geocode(f"{direccion}, Popayán, Cauca, Colombia", timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Error en geocodificación: {e}")
    return None

# ==========================================
# PANTALLA 1: INICIO
# ==========================================
if st.session_state.pagina == 'inicio':
    st.markdown("### **Servicios de salud en Popayán**")
    st.caption("Encuentra dónde ser atendido y qué tan cerca está")
    
    st.warning("Aviso: este sistema solo informa y orienta. No diagnostica enfermedades ni reemplaza la atención de profesionales de la salud.")
    
    st.markdown("#### **1. ¿Qué servicio necesitas?**")
    categorias = ["Consulta médica", "Urgencias", "Salud mental", "Atención materna"]
    cols = st.columns(len(categorias))
    
    for i, cat in enumerate(categorias):
        with cols[i]:
            is_selected = st.session_state.categoria_seleccionada == cat
            btn_type = "primary" if is_selected else "secondary"
            if st.button(cat, use_container_width=True, type=btn_type):
                st.session_state.categoria_seleccionada = cat
                st.rerun()

    st.markdown("#### **2. ¿Dónde estás?**")
    direccion_input = st.text_input("Escribe tu dirección o barrio (ejemplo: Barrio Bolívar, La Esmeralda, Centro)", value=st.session_state.direccion_usuario)
    st.session_state.direccion_usuario = direccion_input
    
    col_dir1, col_dir2 = st.columns([1, 4])
    with col_dir1:
        if st.button("Usar mi ubicación", use_container_width=True):
            st.session_state.direccion_usuario = "Parque Caldas, Centro, Popayán"
            st.success("Ubicación establecida en: Parque Caldas (Centro)")
            st.rerun()

    st.markdown("---")
    
    if st.button("Buscar instituciones", type="primary", use_container_width=True):
        errores = []
        if not st.session_state.categoria_seleccionada:
            errores.append("Por favor selecciona una categoría de servicio.")
        if not st.session_state.direccion_usuario or st.session_state.direccion_usuario.strip() == "":
            errores.append("⚠️ Debes ingresar una dirección o barrio.")
            
        if errores:
            for err in errores:
                st.error(err)
        else:
            with st.spinner("Geocodificando ubicación y calculando distancias..."):
                coords = geocodificar_direccion(st.session_state.direccion_usuario)
                if coords:
                    st.session_state.coords_usuario = coords
                else:
                    st.session_state.coords_usuario = (2.4447, -76.6057)
                    st.warning("No se encontró la dirección exacta, usando ubicación referencial en Popayán.")
            
            st.session_state.pagina = 'resultados'
            st.rerun()

# ==========================================
# CONTENEDOR AISLADO PARA RESULTADOS Y DETALLE
# ==========================================
elif st.session_state.pagina in ['resultados', 'detalle']:
    
    # Creamos el contenedor maestro aislado con st.empty()
    placeholder_principal = st.empty()
    
    with placeholder_principal.container():
        
        # ------------------------------------------
        # VISTA DE RESULTADOS
        # ------------------------------------------
        if st.session_state.pagina == 'resultados':
            if st.button("← Nueva búsqueda"):
                st.session_state.pagina = 'inicio'
                st.rerun()
                
            st.markdown(f"### **Resultados: {st.session_state.categoria_seleccionada}**")
            st.caption(f"Ordenados de la institución más cercana a la más lejana | Ubicación: {st.session_state.direccion_usuario}")
            
            conexion = conectar_bd()
            query = "SELECT * FROM institucion"
            df_instituciones = pd.read_sql(query, conexion)
            conexion.close()
            
            lista_resultados = []
            for _, row in df_instituciones.iterrows():
                coords_inst = (row['latitud'], row['longitud'])
                distancia_km = geodesic(st.session_state.coords_usuario, coords_inst).km
                lista_resultados.append({
                    'id_institucion': row['id_institucion'],
                    'codigo_reps': row['codigo_reps'],
                    'nombre': row['nombre'],
                    'direccion': row['direccion'],
                    'telefono': row['telefono'],
                    'latitud': row['latitud'],
                    'longitud': row['longitud'],
                    'naturaleza_juridica': row['naturaleza_juridica'],
                    'fecha_verificacion': row['fecha_verificacion'],
                    'distancia': distancia_km
                })
                
            lista_resultados = sorted(lista_resultados, key=lambda x: x['distancia'])
            
            col_lista, col_mapa = st.columns([1, 1])
            
            with col_lista:
                if not lista_resultados:
                    st.info("No se encontraron instituciones disponibles.")
                else:
                    for inst in lista_resultados:
                        with st.container(border=True):
                            st.markdown(f"**📍 {inst['nombre']}**")
                            st.text(f"Dirección: {inst['direccion']}, Popayán")
                            st.text(f"Teléfono: {inst['telefono']}")
                            st.caption(f"Distancia estimada: {inst['distancia']:.2f} km")
                            if st.button("Ver detalle", key=f"btn_{inst['id_institucion']}"):
                                st.session_state.institucion_seleccionada = inst['id_institucion']
                                st.session_state.pagina = 'detalle'
                                st.rerun()
                            
            with col_mapa:
                st.markdown("#### Mapa Interactivo de Resultados")
                mapa_popayan = folium.Map(location=st.session_state.coords_usuario, zoom_start=14)
                
                folium.Marker(
                    location=st.session_state.coords_usuario,
                    popup=f"Tu Ubicación: {st.session_state.direccion_usuario}",
                    icon=folium.Icon(color="blue", icon="user", prefix="fa")
                ).add_to(mapa_popayan)
                
                for inst in lista_resultados:
                    folium.Marker(
                        location=(inst['latitud'], inst['longitud']),
                        popup=f"{inst['nombre']} ({inst['distancia']:.2f} km)",
                        icon=folium.Icon(color="red", icon="hospital", prefix="fa")
                    ).add_to(mapa_popayan)
                    
                components.html(mapa_popayan._repr_html_(), height=450)

        # ------------------------------------------
        # VISTA DE DETALLE
        # ------------------------------------------
        elif st.session_state.pagina == 'detalle':
            if st.button("← Volver a los resultados"):
                st.session_state.pagina = 'resultados'
                st.rerun()
                
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM institucion WHERE id_institucion = ?", (st.session_state.institucion_seleccionada,))
            inst = cursor.fetchone()
            conexion.close()
            
            if inst:
                coords_inst = (inst[4], inst[5])
                distancia_actual = geodesic(st.session_state.coords_usuario, coords_inst).km
                
                st.markdown(f"### **{inst[2]}**")
                st.info(f"🏷️ Categoría: {st.session_state.categoria_seleccionada}")
                
                col_det1, col_det2 = st.columns([1, 1])
                
                with col_det1:
                    with st.container(border=True):
                        st.markdown(f"**Dirección:** {inst[3]}, Popayán")
                        st.markdown(f"**Distancia:** {distancia_actual:.2f} km desde tu ubicación")
                        st.markdown(f"**Código REPS:** {inst[1]}")
                        st.markdown(f"**Tipo de atención:** Urgencias, atención presencial")
                        st.markdown(f"**Teléfono:** {inst[6]}")
                        st.markdown(f"**Naturaleza jurídica:** {inst[7]}")
                        st.markdown(f"**Datos verificados el:** {inst[8]}")
                        
                        st.markdown("---")
                        st.markdown("#### **Horario de atención**")
                        st.text("Lunes a viernes: 24 horas")
                        st.text("Sábados, domingos y festivos: 24 horas")
                        
                with col_det2:
                    st.markdown("#### Ruta y Ubicación Exacta")
            
            # Consultar ruta real usando OSRM
            coords_inst = (inst[4], inst[5])
            ruta_coords, tiempo_min, distancia_km = obtener_ruta_osrm(st.session_state.coords_usuario, coords_inst)
            
            # Mostrar métricas estilo Maps
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric(label="⏱️ Tiempo estimado en carro", value=f"{tiempo_min} minutos")
            with col_m2:
                st.metric(label="🛣️ Distancia por vía", value=f"{distancia_km} km")
            
            # Crear mapa centrado entre el usuario y el hospital
            mapa_detalle = folium.Map(location=[inst[4], inst[5]], zoom_start=15)
            
            # Si OSRM devolvió la ruta por las calles, la dibujamos
            if ruta_coords:
                folium.PolyLine(
                    locations=ruta_coords,
                    color="#2b8cbe",
                    weight=5,
                    opacity=0.8
                ).add_to(mapa_detalle)
            
            # Marcador del Hospital
            folium.Marker(
                location=[inst[4], inst[5]],
                popup=inst[2],
                icon=folium.Icon(color="red", icon="hospital", prefix="fa")
            ).add_to(mapa_detalle)
            
            # Marcador del Usuario
            folium.Marker(
                location=st.session_state.coords_usuario,
                popup="Tu Ubicación",
                icon=folium.Icon(color="blue", icon="user", prefix="fa")
            ).add_to(mapa_detalle)
            
            components.html(mapa_detalle._repr_html_(), height=400)
                    
            st.warning("Solo informa y orienta; no reemplaza la atención médica")
        

