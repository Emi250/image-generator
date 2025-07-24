import streamlit as st
import requests
import base64

st.set_page_config(page_title="Generador de Imágenes Históricas", layout="wide")

st.title("🧠 Generador de Imágenes con IA - Escenas Históricas")
st.markdown("""
Ingresa una época histórica y una acción o escena para generar imágenes cinematográficas con IA.
Usamos **Stable Diffusion XL 1.0** de Stability AI, en formato horizontal 16:9 (1024x576 px).
""")

# Entrada usuario con formulario
with st.form("formulario_prompt"):
    epoch = st.text_input("📜 Época histórica", placeholder="Ej: Edad Media, siglo XV")
    action = st.text_input("🎬 Acción o escena", placeholder="Ej: Caballeros en batalla al amanecer")
    submitted = st.form_submit_button("Generar imágenes")

# API Key (desde secrets o input manual)
API_KEY = st.secrets.get("STABILITY_API_KEY") or st.text_input("🔐 Ingresa tu API Key de Stability AI", type="password")

engine_id = "stable-diffusion-xl-1024-v1-0"
url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

if submitted:
    if not epoch or not action:
        st.warning("Por favor, completa ambos campos antes de generar imágenes.")
    elif not API_KEY:
        st.warning("Por favor, ingresa tu API Key para poder usar la API.")
    else:
        prompt = f"{epoch}, {action}, cinematic, realistic, high detail, 16:9 aspect ratio"
        payload = {
            "text_prompts": [
                {"text": prompt}
            ],
            "cfg_scale": 8.0,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 576,
            "width": 1024,
            "samples": 5,
            "steps": 30
        }

        with st.spinner("Generando imágenes..."):
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                images = data.get("artifacts", [])

                if not images:
                    st.error("No se generaron imágenes. Intenta cambiar el prompt o intenta más tarde.")
                else:
                    st.success(f"✅ Se generaron {len(images)} imágenes.")
                    cols = st.columns(len(images))
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
                st.error(f"Error al generar imágenes: {e}")
