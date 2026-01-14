import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon=" ",layout = 'centered'
)

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
resized_img = img.resize((140, 140))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 200px;
                background-position: 90px 50px;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: " ";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 50px;
                position: relative;
                top: 500px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

###############################




#st.write("# Congratulations, you found me!")

st.write(
    """
    ##### Hi! I'm **Erika Korb**, an Astrophysics aand Staff Research Scientist""")

st.write(""" ###### Currently, I work at the Astronomical Observatory of the Valle d'Aosta ([OAVdA](https://www.oavda.it/)), in Italy, that is part of the Clément-Fillietroz Foundation ([FCF](https://www.oavda.it/chi-siamo)). """)
    
st.write( """  ###### My research covers a broad range of topics and expertise. I develop Artificial Intelligence solutions in the context of Technological Transfer to support ecological transition and contribute to environmental monitoring. I also continue the astrophysical research work started during my PhD, that I obtained at the Universityi of Padova in collaboration with the University of Heidelberg, where I spent 9 months collaborating with the  [DemoBlack](https://demoblack.com/) group. In my astrophysical research, I investigate stellar, binary evolution, and gravitational wave progenitors via population-synthesis simulations. In particular, I am part of the development and mainteinance team for the open-source [SEVN](https://sevncodes.gitlab.io/sevn/) population-synthesis code and I am a core member of the LISA Consortium.  
          """)
    
st.write(
    """  ######  If you are curious to know more on my professional background, take a look at my [CV](https://github.com/erikakorb/CV/blob/main/CV.pdf). If you are here to know a bit more about me, I can tell you that when I am not in front of a computer, I am likely biking or hiking somewhere and taking pictures of the wonders I bump into. If you are here for some fun and you want to see some fancy astrophysical project or a nice dashboard on Venice high tides, feel free to browse the sidebar (have I told you already that Venice is my hometown?). """)
    
st.image('VenicePartialEclipse.jpg', caption='In a warm summer evening of July 2018, a partial eclipsing Moon, Mars, and the San Marco bell tower met together...')
