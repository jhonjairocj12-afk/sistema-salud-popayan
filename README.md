# 🏥 Sistema Web Georreferenciado de Servicios de Salud — Popayán

## 1. Nombre del Proyecto
* **Sistema Web Georreferenciado para la Orientación y Localización de Servicios de Salud en Popayán** *(sistema-salud-popayan)*

---

## 2. Objetivo
Desarrollar una herramienta tecnológica interactiva basada en tecnologías web y geoespaciales para facilitar a los ciudadanos la búsqueda, visualización y cálculo de proximidad a las instituciones prestadoras de servicios de salud (IPS, hospitales y centros de asistencia) en el casco urbano de Popayán, optimizando los tiempos de orientación y acceso a la atención médica.

---

## 3. Descripción
El sistema es una aplicación full-stack desarrollada en **Python** utilizando **Streamlit** para la interfaz gráfica de usuario. Permite realizar consultas dinámicas filtradas por tipo de atención (*Urgencias, Consulta médica, Salud mental, Atención materna*), geocodificando las ubicaciones de los usuarios y renderizando mapas interactivos mediante **Folium** y **Geopy**. La persistencia de los datos georreferenciados se gestiona a través de una base de datos relacional ligera en **SQLite3**, estructurada con scripts modulares de inicialización y población de registros.

La aplicación se encuentra desplegada y operativa en la nube para acceso público:
🔗 **[Enlace de la Aplicación en Vivo (Streamlit Cloud)](https://sistema-salud-popayangit-kvsbeu9et79mmfxatrpyxy.streamlit.app)**

---

## 4. Integrantes
* **Jhon Jairo Campo Jiménez** — Desarrollo del Sistema y Despliegue Cloud[cite: 1]
* **Fabian Alexander Castillo Cárdenas** — Pruebas Funcionales, Validación de Datos y Documentación[cite: 1]

**Institución:** Universidad Nacional Abierta y a Distancia (UNAD)
**Escuela:** Escuela de Ciencias Básicas Tecnología e Ingeniería 
**Programa:** Proyecto de Grado
**Grupo:** 202016907_56  
**Ubicación:** Popayán, Departamento del Cauca, Colombia[cite: 1]

---

## 5. Instrucciones de Uso

### A. Uso de la Aplicación en Línea
1. Haga clic en el enlace de la aplicación en vivo: [Ver Aplicación](https://sistema-salud-popayangit-kvsbeu9et79mmfxatrpyxy.streamlit.app).
2. Seleccione en el panel lateral el tipo de servicio médico que necesita o ingrese su ubicación/barrio de referencia en Popayán (ej. *Barrio Bolívar, La Esmeralda, Centro*). 
3. Visualice los resultados ordenados por proximidad y explore el mapa interactivo con las rutas y marcadores de las instituciones de salud.

## 📌 Recomendaciones y Consideraciones Técnicas

1. **Delimitación Geográfica:** La aplicación y sus consultas geoespaciales están diseñadas exclusivamente para operar dentro del casco urbano de **Popayán, Cauca**[cite: 1]. Por lo tanto, las búsquedas y cálculos de proximidad arrojarán resultados óptimos dentro de esta zona geográfica.
2. **Compatibilidad del Navegador (Traducción automática):** Se recomienda **no utilizar la traducción automática del navegador (como Google Traductores u otras extensiones) al español**, ya que la manipulación del DOM por parte de dichos traductores altera los componentes internos de Streamlit y puede generar conflictos de estado (por ejemplo, interrupciones o bloqueos al intentar retornar de la pantalla 3 a la pantalla 2).


