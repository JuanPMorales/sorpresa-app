import streamlit as st
import random
import time
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ==========================================
# CONFIGURACIÓN
# ==========================================
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM", "")
CHAT_ID = os.getenv("CHAT_ID", "")
NOMBRES_VALIDOS = os.getenv("NOMBRES_VALIDOS").split(",")

# Planes y su clasificación
PLANES_EN_CASA = ["🎲 Juegos en casa", "🎬 Películas en casa", "🧩 Armar rompecabezas", "🎨 Pintar", "👨‍🍳 Te preparo una cena", "☕ Tarde de café y charla", "📖 Leer juntos", "🎮 Noche de videojuegos"]
PLANES_SALIDA = ["🎬 Cine", "🍽️ Salir a cenar", "🧺 picnic", "🌼 Puebliar", "🛼 Patinar", "🍦 Ir por un helado", "🚶 Caminar", "🎳 Bolos"]
# Equilibrar probabilidades: 50% en casa, 50% de salida
TODAS_LAS_OPCIONES = PLANES_EN_CASA * 2 + PLANES_SALIDA * 5

st.set_page_config(page_title="Sorpresa", layout="centered")

# ==========================================
# CARGAR ESTILOS CSS EXTERNOS
# ==========================================
def cargar_css(archivo_css):
    with open(archivo_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llamamos a la función apuntando a la carpeta css
cargar_css("css/style.css")

# ==========================================
# LÓGICA DE ESTADOS
# ==========================================
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = 1
if 'actividad_elegida' not in st.session_state:
    st.session_state.actividad_elegida = ""
if 'es_salida' not in st.session_state:
    st.session_state.es_salida = False
if 'hora_personalizada' not in st.session_state:
    st.session_state.hora_personalizada = False

# ==========================================
# PANTALLA 1: LOGIN
# ==========================================
if st.session_state.pantalla == 1:
    st.markdown("<h2 class='centrado'>🔒<br>Esto se desbloquea<br>con tu nombre o tu apodo ❤️</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        nombre = st.text_input("", placeholder="escribe tu nombre o apodo...", key="nombre_input")
        
        # Validar con el botón
        if st.button("↩ Entrar", use_container_width=True):
            nombre_limpio = nombre.lower().strip()
            nombres_validos_limpios = [n.strip().lower() for n in NOMBRES_VALIDOS]
            if nombre_limpio in nombres_validos_limpios:
                st.session_state.pantalla = 2
                st.rerun()
            elif nombre:
                st.markdown("<p class='error-texto'>No es tu nombre ni tu apodo 👀</p>", unsafe_allow_html=True)
        
        # Validar cuando presiona Enter (si el input tiene focus)
        nombre_limpio = nombre.lower().strip()
        nombres_validos_limpios = [n.strip().lower() for n in NOMBRES_VALIDOS]
        if nombre and nombre_limpio in nombres_validos_limpios:
            st.session_state.pantalla = 2
            st.rerun()

# ==========================================
# PANTALLA 2: LA RULETA (TRAGAMONEDAS)
# ==========================================
elif st.session_state.pantalla == 2:
    st.markdown("<h3 class='centrado'>Vamos a hacer...</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        caja_tragamonedas = st.empty()
        
        if not st.session_state.actividad_elegida:
             caja_tragamonedas.markdown("<div class='tragamonedas'>❓ ❓ ❓</div>", unsafe_allow_html=True)
        else:
             caja_tragamonedas.markdown(f"<div class='tragamonedas'>{st.session_state.actividad_elegida}</div>", unsafe_allow_html=True)
        
        if st.button("🔄 Girar", use_container_width=True):
            for _ in range(15):
                actividad_temporal = random.choice(TODAS_LAS_OPCIONES)
                caja_tragamonedas.markdown(f"<div class='tragamonedas'>{actividad_temporal}</div>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            eleccion = random.choice(TODAS_LAS_OPCIONES)
            caja_tragamonedas.markdown(f"<div class='tragamonedas'>{eleccion}</div>", unsafe_allow_html=True)
            st.session_state.actividad_elegida = eleccion
            st.session_state.es_salida = eleccion in PLANES_SALIDA
            st.rerun()

        if st.session_state.actividad_elegida:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Elegir {st.session_state.actividad_elegida}", use_container_width=True):
                st.session_state.pantalla = 3
                st.rerun()

# ==========================================
# PANTALLA 3: ELEGIR DÍA Y/O HORA
# ==========================================
elif st.session_state.pantalla == 3:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Mostrar calendario para elegir fecha (para todos los planes)
        st.markdown("<h3 class='centrado'>¿Qué día quieres? 📅</h3>", unsafe_allow_html=True)
        
        fecha_elegida = st.date_input(
            "",
            value=datetime.now().date(),
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=30),
            label_visibility="collapsed"
        )
        
        st.markdown("<h3 class='centrado'>¿A qué hora? ⏰</h3>", unsafe_allow_html=True)
        
        opciones_hora = ["5pm", "6pm", "7pm", "8pm", "9pm", "🕐 Otra hora"]
        hora_seleccionada = st.radio(
            "",
            opciones_hora,
            label_visibility="collapsed"
        )
        
        # Si selecciona "Otra hora", mostrar inputs personalizados
        if hora_seleccionada == "🕐 Otra hora":
            col_hora, col_am_pm = st.columns([1, 1])
            with col_hora:
                hora_num = st.number_input(
                    "Hora:",
                    min_value=1,
                    max_value=12,
                    value=7,
                    step=1
                )
            with col_am_pm:
                periodo = st.radio(
                    "Período:",
                    ["AM", "PM"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
            hora = f"{int(hora_num)}{periodo}"
        else:
            hora = hora_seleccionada
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Confirmar", use_container_width=True):
            try:
                fecha_formateada = fecha_elegida.strftime("%d/%m/%Y")
                mensaje_bot = f"¡Plan confirmado! 🎉\nActividad: {st.session_state.actividad_elegida}\nFecha: {fecha_formateada}\nHora: {hora}"
                url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={mensaje_bot}"
                requests.get(url)
            except Exception as e:
                pass
            
            st.session_state.hora_elegida = hora
            st.session_state.fecha_elegida = fecha_elegida
            st.session_state.pantalla = 4
            st.rerun()

# ==========================================
# PANTALLA 4: FINALIZAR
# ==========================================
elif st.session_state.pantalla == 4:
    fecha_formateada = st.session_state.fecha_elegida.strftime("%d/%m/%Y") if hasattr(st.session_state, 'fecha_elegida') else ""
    
    st.markdown(f"""
    <div class='centrado'>
        <h3>ya eres hermosa,<br>pero estate lista! ❤️</h3>
        <p style='color:#ff4b4b; font-weight:bold;'>📅 {fecha_formateada} a las {st.session_state.hora_elegida}</p>
        <p style='color:#ff4b4b; font-weight:bold;'>$ dirección: tu casa (pasaré por ti xd)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.image("https://media.giphy.com/media/26BRv0ThflsHCqDrG/giphy.gif", use_container_width=True)