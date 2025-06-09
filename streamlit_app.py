# ✅ FRONTEND: app.py (Streamlit UI with Quantified WELL Prompts)

import streamlit as st
from PIL import Image
import requests

st.set_page_config(page_title="WELL-AI Interior Redesign", layout="centered")

st.title("🧠 WELL-AI with Realistic Vision + LoRA (img2img)")

st.markdown("""
Upload your current interior image and select WELL features to enhance.  
We'll re-render the space using a high-quality Stable Diffusion model with optional LoRA styles for personalized redesigns.
""")

uploaded_image = st.file_uploader("📤 Upload interior image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    st.subheader("🧩 Select WELL Features")
    daylight = st.checkbox("Maximize Daylight")
    indoor_plants = st.checkbox("Add Indoor Plants")
    wood_materials = st.checkbox("Use Natural Wood Materials")
    lounge_area = st.checkbox("Create a Relaxation Area")
    acoustic_panels = st.checkbox("Improve Acoustic Comfort")

    st.subheader("📏 WELL Metrics (Optional)")
    with st.expander("🔧 Customize Details"):
        lux = st.slider("Ambient Light Level (lux)", 100, 1000, 500)
        greenery = st.slider("Greenery Coverage (%)", 0, 100, 25)
        stair_width = st.slider("Stair Width (m)", 0.5, 3.0, 1.5)
        noise_level = st.slider("Target Noise Level (dB)", 20, 70, 40)
        wood_pct = st.slider("Wood Material Coverage (%)", 0, 100, 30)

    lora_style = st.selectbox("🎨 Choose LoRA Style (optional):", [
        "None",
        "pastel-mix-lora",
        "modern-architecture-lora",
        "interior-studio-lora"
    ])

    # 🔄 ngrok 주소 자동 불러오기
    try:
        with open("ngrok_url.txt", "r") as f:
            NGROK_URL = f.read().strip()
    except:
        st.error("ngrok_url.txt not found. Please copy it from Colab.")
        st.stop()

    if st.button("🧠 Generate with AI"):
        with st.spinner("Enhancing your space with WELL principles..."):
            try:
                prompt_parts = []
                if daylight:
                    prompt_parts.append(f"soft natural daylight filtering through large windows, {lux} lux")
                if indoor_plants:
                    prompt_parts.append(f"indoor plants with {greenery}% area coverage")
                if wood_materials:
                    prompt_parts.append(f"natural wood surfaces covering {wood_pct}%")
                if lounge_area:
                    prompt_parts.append("relaxation lounge with soft seating and calm textures")
                if acoustic_panels:
                    prompt_parts.append(f"acoustic panels reducing noise to {noise_level} dB")
                prompt_parts.append(f"central staircase with width {stair_width}m to promote movement")
                prompt_parts.append("ultra realistic, architectural interior photography")
                if lora_style != "None":
                    prompt_parts.append(f"style hint: {lora_style.replace('-', ' ')}")

                prompt = ", ".join(prompt_parts)
                st.write("🔍 Prompt used:", prompt)

                files = {"image": uploaded_image}
                data = {"prompt": prompt, "lora": lora_style}

                response = requests.post(f"{NGROK_URL}/generate", files=files, data=data)

                if response.status_code == 200:
                    st.image(response.content, caption="🧠 AI-Generated Interior", use_column_width=True)
                    st.download_button(
                        label="📥 Download Result",
                        data=response.content,
                        file_name="redesigned_interior.png",
                        mime="image/png"
                    )
                else:
                    st.error("❌ Generation failed. Check backend.")

            except Exception as e:
                st.error(f"Unexpected error: {e}")
else:
    st.info("👈 Please upload an image to begin.")
