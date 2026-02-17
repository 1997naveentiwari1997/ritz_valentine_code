# python -m pip install requests
import streamlit as st
import base64
import random
import datetime
import requests
import os

# --- LOGGING FUNCTION ---
def log_action(action_type, details=""):
    """Writes logs to file AND prints them to the Streamlit Cloud console"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Get Device Details
    try:
        user_agent = st.context.headers.get("User-Agent", "Unknown Device")
    except:
        user_agent = "Unknown Device"
    
    # 2. Get Location
    try:
        geo = requests.get('http://ip-api.com', timeout=1).json()
        location = f"{geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')}"
    except:
        location = "Location Unknown"

    log_entry = f"[{timestamp}] | LOC: {location} | DEVICE: {user_agent} | ACTION: {action_type} | DETAILS: {details}"
    
    # WRITE TO FILE (For local testing)
    with open("sys_trace.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
        
    # PRINT TO CONSOLE (This makes it show up in your Streamlit Cloud logs)
    print(f"VALENTINE_LOG: {log_entry}")

# --- CONFIGURATION ---
# Replace with your actual image links
# BG_URL = "D:/NAVEEN_NEW_SOFTWARE/valentine_code/RITZ/BG.jpg" # Use direct links or local path
if os.path.exists("photo.jpg"):
    OUR_PHOTO = "photo.jpg" 
else:
    OUR_PHOTO = "" # Handle missing file

# Define Questions, Answers, and unique Images for each question
QUIZ_DATA = [
    {"question": "Date we saw each other for the first time?(ddmmyyyy)", "answer": "07022019", "image": "photo1.jpg", "img_width": 700, "img_height": 700},
    {"question": "What you use to call me?(first name)", "answer": "Aarush", "image": "photo2.jpg", "img_width": 700, "img_height": 400},
    {"question": "First thing i told you when i saw you for the first time?", "answer": "Will you marry me", "image": "photo3.jpg", "img_width": 700, "img_height": 700},
    {"question": "My favourite body part in your body?", "answer": "Nose", "image": "photo4.jpg", "img_width": 700, "img_height": 700},
    {"question": "What was our relationship as per you", "answer": "Time pass", "image": "photo5.jpg", "img_width": 700, "img_height": 700},
    {"question": "What was the first gift i gave you", "answer": "Ancklet", "image": "photo6.jpg", "img_width": 700, "img_height": 700}
]

# --- BACKGROUND & CSS ---
# 1. Function to convert local image to Base64
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file): return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_locally(local_img_path):
    bin_str = get_base64_of_bin_file(local_img_path)
    if not bin_str: return
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .header-box {{
        background-color: rgba(255, 75, 75, 0.9);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        border: 2px solid white;
    }}
    .valentine-question {{
        color: #C2185B;
        font-size: 25px;
        font-weight: bold;
        font-family: 'Comic Sans MS', cursive;
    }}
    /* Custom style for the quiz image to force height */
    .quiz-img-container img {{
        object-fit: cover; /* This crops the image to fill the box without stretching */
        border-radius: 15px;
        border: 3px solid white;
    }}
    </style>
    ''', unsafe_allow_html=True)

# Function to display resized image using HTML to force height
def display_resized_image(img_path, width, height):
    if not os.path.exists(img_path):
        st.error(f"Image {img_path} not found.")
        return
    file_ = open(img_path, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<div class="quiz-img-container"><img src="data:image/jpg;base64,{data_url}" width="{width}" height="{height}"></div>',
        unsafe_allow_html=True,
    )

set_bg_locally('BG.jpg')

# --- SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 'start'
    log_action("PAGE_OPENED", "User loaded the page")
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'no_pos' not in st.session_state:
    st.session_state.no_pos = 1

# --- APP LAYOUT ---

if st.session_state.step == 'start':
    st.markdown('<div class="header-box">Are you ready to answer this question on this Valentine?</div>', unsafe_allow_html=True)
    if st.button("Yes, I am! ❤️", use_container_width=True):
        log_action("BUTTON_CLICK", "Start Quiz")
        st.session_state.step = 'quiz'
        st.rerun()

elif st.session_state.step == 'quiz':
    st.markdown('<div class="header-box">A Little Love Quiz...</div>', unsafe_allow_html=True)
    
    current_q = QUIZ_DATA[st.session_state.quiz_index]
    
    # Use our new function to show image with custom height and width
    display_resized_image(current_q['image'], current_q['img_width'], current_q['img_height'])

    st.markdown(f'<p class="valentine-question">Question {st.session_state.quiz_index + 1}</p>', unsafe_allow_html=True)
    st.write(f"### {current_q['question']}")

    user_ans = st.text_input("Type your answer here:", key=f"input_{st.session_state.quiz_index}").lower().strip()
    
    if user_ans:
        is_correct = user_ans == current_q['answer'].lower().strip()
        log_action("QUIZ_ANSWER", f"Q{st.session_state.quiz_index+1}: {user_ans} (Correct: {is_correct})")
        
        if is_correct:
            st.success("Correct! You're so precious! ✨")
            st.balloons()
            if st.button("Proceed to Next ➡️", use_container_width=True):
                log_action("BUTTON_CLICK", f"Next Question from {st.session_state.quiz_index+1}")
                if st.session_state.quiz_index < len(QUIZ_DATA) - 1:
                    st.session_state.quiz_index += 1
                    st.rerun()
                else:
                    st.session_state.step = 'ask'
                    st.rerun()
        else:
            st.warning("Not quite! Think harder... ❤️")

    if st.session_state.quiz_index > 0:
        if st.button("⬅️ Previous Question", use_container_width=True):
            log_action("BUTTON_CLICK", "Previous Question")
            st.session_state.quiz_index -= 1
            st.rerun()

elif st.session_state.step == 'ask':
    st.markdown('<div class="header-box">The Final Question...</div>', unsafe_allow_html=True)
    if os.path.exists("photo3.jpg"):
        st.image("photo3.jpg", use_container_width=True)
    st.markdown("""
        <div style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)); 
             background-size: cover; background-position: center; padding: 50px; border-radius: 25px; 
             text-align: center; border: 5px solid white; color: white;">
            <h1 style="font-size: 35px; text-shadow: 2px 2px 8px #000000;">Will you be my Valentine?</h1>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("YES! 😍", use_container_width=True):
            log_action("FINAL_ANSWER", "YES")
            st.session_state.step = 'success'
            st.rerun()
            
    no_col_index = st.session_state.no_pos
    with cols[no_col_index]:
        if st.button("No 🥺", use_container_width=True):
            log_action("FINAL_ANSWER", "NO (Clicked)")
            st.session_state.no_pos = random.choice([1, 2, 3])
            st.toast("Too slow! You can't say no! 😉")
            st.rerun()

elif st.session_state.step == 'success':
    st.balloons()
    st.markdown('<div class="header-box">I Knew It! ❤️</div>', unsafe_allow_html=True)
    if os.path.exists(OUR_PHOTO):
        st.image(OUR_PHOTO, use_container_width=True)
    st.write("# I knew it! You love me a lot! 😍")
    st.markdown("---")
    st.write(" *\"You make every day feel like Valentine's Day.\"*")
    st.markdown("---")
    st.write(" *\"मै अब तक जान न पाया हु, क्यों तुझसे मिलने आया हु।\"*")
    st.write(" *\"तू मेरे दिल की धड़कन है, मै तेरे दर्पण की छाया हु।\"*")
    st.write(" *\"तू चाहे तो सपना कह ले, या अनहोनी घटना कह ले।\"*")
    st.write(" *\"मै जिस पथ से भी चल निकला, तेरे दर पे आ बैठा।\"*")
    st.write(" *\"मै तुझसे प्रीत लगा बैठा।\"*")
    st.write(" *\"ये प्यार दिए का तेल नहीं, दो चार घड़ी का मेल नहीं।\"*")
    st.write(" *\"ये तो युग युग का बंधन है, कोई गुड़ियों का खेल नहीं।\"*")
    st.write(" *\"तू चाहे दीवाना कह ले, या अल्हड़ मस्ताना कह ले।\"*")
    st.write(" *\"मैने जो भी रेखा खींची, तेरी तस्वीर बना बैठा।\"*")
    st.write(" *\"मै तुझसे प्रीत लगा बैठा।\"*")
    st.write("---")
    st.write(" *\"I'm the luckiest person to have you in my life.\"*")

def log_action(action_type, details=""):
    # ... your existing file-writing code ...
    
    # ADD THIS LINE to see logs in the Streamlit Cloud sidebar:
    print(f"LOG: {action_type} - {details}") 

