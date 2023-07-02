import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon=" ",layout = 'centered'
)

#from PIL import Image

# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# my_logo = add_logo(logo_path="Korb_Erika_pic.jpg", width=50, height=60)
# st.sidebar.image(my_logo)

# # # OR

# # st.sidebar.image(add_logo(logo_path="your/logo/path", width=50, height=60)) 

import base64

with open("Korb_Erika_pic.jpg", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

#     st.sidebar.markdown(
#         f"""
#         <div style="display:table;margin-top:-20%;margin-left:50%;">
#             <img src="data:image/png;base64,{data}" width="150" height="150">
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# def add_logo():
#     st.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(https://github.com/erikakorb/website/blob/main/Korb_Erika_pic.jpg);
#                 background-repeat: no-repeat;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#             }
#             [data-testid="stSidebarNav"]::before {
#                 content: "My Company Name";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#                 top: 100px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: data;
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()

st.write("# Congratulations, you found me!")

st.write(
    """
    ##### Hi! I'm **Erika Korb**, a PhD student in Astrophysics at the University of Padua. """)
    
st.write( """  ###### At work, I play with stars and binaries by means of numerical simulations in the [DemoBlack](https://demoblack.com/) group. When I am not in front of a computer, I am likely biking somewhere and taking pictures of the wonders I bump into. Ah, and I enjoy wandering around my hometown: Venice. """)
    
st.write(
    """  ######  If you are curious to know more on my background, take a look at my [CV](https://github.com/erikakorb/CV/blob/main/CV.pdf).  If you are here for the fun and you want to see some fancy astrophysical project or a nice dashboard on Venice high tides, feel free to browse the sidebar. """)
    
st.image('VenicePartialEclipse.jpg', caption='In a warm summer evening of July 2018, a partial eclipsing Moon, Mars, and the San Marco bell tower met together...')
