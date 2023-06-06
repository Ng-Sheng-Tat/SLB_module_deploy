import streamlit as st
from PIL import Image

from streamlit_image_coordinates import streamlit_image_coordinates
image = Image.open("Image4.png")
value = streamlit_image_coordinates("https://placekitten.com/200/300")

st.write(value)