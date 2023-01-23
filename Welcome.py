import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon=" ",layout = 'centered'
)


st.write("# Congratulations, you found me!")

st.write(
    """
    ##### Hi! I'm **Erika Korb**, a PhD student in Astrophysics at the University of Padua. """)
    
st.write( """  ###### At work, I play with stars and binaries by means of numerical simulations in the [DEMOBLACK](https://demoblack.com/) group. In my free time, I play with codes as well. Ah, and I enjoy wandering aroung my hometown: Venice. """)
    
st.write(
    """  ######  If you are curious to see some fancy astrophysical project or a nice dashboard on Venice high tides, feel free to browse the sidebar. """)
    
st.image('VenicePartialEclipse.jpg', caption='In a hot summer evening of July 2018, a partial eclipsing Moon, Mars, and the San Marco bell tower met together...')
