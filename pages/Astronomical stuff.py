import streamlit as st

################################ profile pic
import io
from PIL import Image
import base64

file = open("Korb_Erika_pic.jpg", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((150, 150))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 50px;
                background-position: 90px 50px;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: " ";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 50px;
                position: relative;
                top: 200px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

###############################

st.set_page_config(
    page_title="Astronomical stuff",
    page_icon=" ",layout = 'centered'
)



st.write("# Page under construction")

st.write(
    """
    Woops, you arrived here too early! """)
    
