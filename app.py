import streamlit as st
import requests
import base64

st.set_page_config(page_title="Generador de Imágenes Históricas", layout="wide")

st.title("🧠 Generador de Imágenes con IA - Escenas Históricas")
st.markdown("Ingresa una época y una acción, y genera imágenes cinematográficas con IA (SDXL 1.0 de Stability AI)")

# Formulario de entrada
with st.form("prompt_form"):
    epoch = st.text_input("📜 Época histórica", placeholder="Ej: Roma antigua, siglo I a.C.")
    action = st.text_input("🎬 Acción o escena", placeholder="Ej: Gladiadores luchando en el Coliseo al atardecer")
    submit = st.form_submit_button("Generar imágenes")

# API Key (usa secrets o variable oculta)
API_KEY = st.secrets["STABILITY_API_KEY"] if "STABILITY_API_KEY" in st.secrets else st.text_input("🔐 Tu API Key de Stability AI", type="password")

# Lógica de generación
if submit and epoch and action and API_KEY:
    with st.spinner("Generando imágenes..."):
        prompt = f"{epoch}, {action}, cinematic style, realistic, high detail"

        url = "https://api.stability.ai/v2beta/stable-image/generate/sdxl"
        headers = {
            "authorization": f"Bearer {API_KEY}",
            "accept": "application/json",
            "content-type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "output_format": "png",
            "samples": 5,
            "steps": 30,
            "cfg_scale": 8
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            images = response.json()["artifacts"]

            st.success("✅ ¡Imágenes generadas!")
            cols = st.columns(5)
            for idx, img in enumerate(images):
                image_data = base64.b64decode(img["base64"])
                with cols[idx]:
                    st.image(image_data, use_column_width=True)
                    st.download_button(
                        label="Descargar",
                        data=image_data,
                        file_name=f"imagen_{idx+1}.png",
                        mime="image/png"
                    )
        except Exception as e:
            st.error(f"❌ Error al generar imágenes: {e}")
