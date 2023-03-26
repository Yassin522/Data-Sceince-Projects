import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_zrqthn6o.json")
img_school= Image.open("images/teacher mockup_014955.jpg")
img_portfolio = Image.open("images/Annotation 2022-02-05 163210.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am Yassin :wave:")
    st.title("Computer Science student from Syria")
    st.write(
        "I am highly motivated and committed to staying up-to-date with the latest technologies and industry best practices. I am a proactive learner who is always looking for opportunities to improve my skills and advance my career."
    )
    st.write("[Find me in Linkedin >](https://www.linkedin.com/in/yassin-abdulmahdi/)")

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("About me")
        st.write("##")
        st.write(
            """
            - As a student of Information Technology Engineering at Damascus University and a professional Flutter developer with over a year of experience, I have developed expertise in a range of technical skills including Firebase, version control with Git and GitHub, and connecting Flutter applications to backends. My objective is to continue applying these abilities as a Flutter developer while also learning new skills in the field of mobile application development.
            - In addition to my professional work, I am a competitive programmer with strong problem-solving skills, proficiency in algorithms and data structures, and experience participating in the ACM ICPC. I also volunteer with the RBCs team to help others learn the skills of Information Technology Engineering.
            - I am particularly interested in the field of artificial intelligence (AI). I have had the opportunity to study the principles of machine learning and explore the many applications of AI in a variety of contexts. I am particularly interested in the ways that AI can be used to improve decision-making, automate processes, and drive innovation.
            """
        )
        st.write("[Github>](https://github.com/Yassin522)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("My Portfolio")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_portfolio)
    with text_column:
        st.subheader("My portfolio using Flutter")
        st.write(
            """
             Responsive and Animated Portfolio Website & App it works perfectly on mobile and web
            """
        )
        st.markdown("[Link](ttps://github.com/Yassin522/MyPortfolio-Flutter)")
with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_school)
    with text_column:
        st.subheader("School Management System")
        st.write(
            """
            The project is an Flutter application for the student, teacher and parents
             and also a web application for the administration to control all school data
            """
        )
        st.markdown("[Link](https://www.linkedin.com/feed/update/urn:li:activity:6965249047607541760/)")

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/yasinalmhdi8@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
