import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set the provided API key directly
api_key = "AIzaSyBYQ7zoXf6ffAkxRSvu4ChscRFfgrFIllA"
genai.configure(api_key=api_key)

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Gemini calorie analyzer")
st.header("Gemini calorie analyzer")

input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit_button = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calorie intake
in the below format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
"""

if submit_button:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("The Response is")
    st.write(response)
