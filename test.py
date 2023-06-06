import streamlit as st
from PIL import Image

from streamlit_image_coordinates import streamlit_image_coordinates
image = Image.open("Image4.png")
image = image.convert("RGB")
value = streamlit_image_coordinates(image)

st.write(value)