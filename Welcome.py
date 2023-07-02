import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon=" ",layout = 'centered'
)


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
                background-position: 100px 50px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.write("# Congratulations, you found me!")

st.write(
    """
    ##### Hi! I'm **Erika Korb**, a PhD student in Astrophysics at the University of Padua. """)
    
st.write( """  ###### At work, I play with stars and binaries by means of numerical simulations in the [DemoBlack](https://demoblack.com/) group. When I am not in front of a computer, I am likely biking somewhere and taking pictures of the wonders I bump into. Ah, and I enjoy wandering around my hometown: Venice. """)
    
st.write(
    """  ######  If you are curious to know more on my background, take a look at my [CV](https://github.com/erikakorb/CV/blob/main/CV.pdf).  If you are here for the fun and you want to see some fancy astrophysical project or a nice dashboard on Venice high tides, feel free to browse the sidebar. """)
    
st.image('VenicePartialEclipse.jpg', caption='In a warm summer evening of July 2018, a partial eclipsing Moon, Mars, and the San Marco bell tower met together...')
