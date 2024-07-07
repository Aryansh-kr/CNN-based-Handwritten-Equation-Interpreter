import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2
from predict import predict
import base64

st.set_page_config(page_title="Algebraic Equation Solver", page_icon="logo.png", initial_sidebar_state="auto")

# Set the background color and text color
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .css-1v0mbdj {
        color: black;
    }
    .css-1v0mbdj p {
        color: black;
    }
    .container {
        display: flex;
    }
    .logo-text {
        font-weight: 700;
        font-size: 50px;
        color: black;
        margin-left: -15px;
        padding: 15px;
    }
    .logo-img {
        display: none;  /* Hide the logo image */
    }
    .stAlert p {
        color: black;
    }
    .custom-subheader {
        color: black;
        font-size: 24px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Heading section with the logo
st.markdown(
    f"""
    <div class="container">
        <p class="logo-text">CNN based Handwritten Equation Interpreter</p>
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    stroke_width = st.slider(label="Adjust Stroke Width", value=5, min_value=3, max_value=10)
    stroke_color = st.color_picker(label="Stroke Color", value='#000000')
    bg_color = st.color_picker(label="Background Color", value='#FFFFFF')

    st.markdown(
        "<p style='text-align: center; font-size: 1.2em; color: black;'><a href='https://github.com/Sgvkamalakar/Hand-Written-Equation-Solver'>Source Code</a></p>",
        unsafe_allow_html=True)

drawing_mode = "freedraw"
realtime_update = True

data = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=realtime_update,
    height=300,
    width=700,
    drawing_mode=drawing_mode,
    key="full_app",
)

if st.button('Predict'):
    path = r'C:\Users\Lenovo\PycharmProjects\pythonProject\handwritten\Web_app\temp\temp.png'
    cv2.imwrite(path, data.image_data)
    try:
        eq, res = predict(path)
        st.markdown(f"#### <span style='color: black;'>Equation: **{eq}**</span>", unsafe_allow_html=True)

        x = str(res)
        res_length = len(x)
        width = 100
        font_size = 35
        if res_length > 3:
            width = 150
            font_size = 25

        padding_top = max(5, (40 - font_size) / 2)
        padding_bottom = max(5, (40 - font_size) / 2)
        style = f"background-color: black; height: 70px; width: {width}px; border-radius: 5px; padding-top: {padding_top}px; padding-bottom: {padding_bottom}px; margin-left: 150px; text-align: center;"

        label_style = "font-weight: bold; color: white; font-size: {font_size}px;"  # Updated color to white for result
        label_style = label_style.format(font_size=font_size)

        st.markdown("<h3 class='custom-subheader'>Result</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='{style}'><label style='{label_style}'>{res}</label></div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
