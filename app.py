import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.title("OCR за разпознаване на съставки 🧪")

# Списък с потенциално вредни съставки
harmful_ingredients = [
    "E621", "E622", "E623", "E624", "E625",  # глутамати
    "E102", "E110", "E122", "E124", "E129",  # оцветители
    "E200", "E202", "E210", "E211",          # консерванти
]

uploaded_file = st.file_uploader("Качи снимка на етикет", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    with st.spinner("Разпознаване на текст..."):
        reader = easyocr.Reader(['en', 'bg'])
        result = reader.readtext(np.array(image), detail=0)

        extracted_text = " ".join(result)
        st.subheader("📄 Разпознат текст:")
        st.write(extracted_text)

        # Търсене на вредни съставки
        found = []
        for ingredient in harmful_ingredients:
            if ingredient.lower() in extracted_text.lower():
                found.append(ingredient)

        st.subheader("⚠️ Намерени потенциално вредни съставки:")
        if found:
            for f in found:
                st.write(f"❗ {f}")
        else:
            st.write("✅ Не са открити вредни съставки.")
