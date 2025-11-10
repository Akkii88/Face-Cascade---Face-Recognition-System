import streamlit as st
from PIL import Image
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Face Recognition System",
    page_icon="📸",
    layout="wide",
)

# ---------------- BACKGROUND VIDEO + EFFECTS ----------------
video_html = """
<video autoplay muted loop id="bg-video">
    <source src="media/ai_bg.mp4" type="video/mp4">
</video>

<div class="overlay"></div>
<canvas id="particles"></canvas>

<style>
/* ---------- Background Video ---------- */
#bg-video {
    position: fixed;
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    z-index: -3;
    object-fit: cover;
    filter: brightness(40%) blur(1px);
}

/* ---------- Glowing Gradient Overlay ---------- */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 30%, rgba(0,255,255,0.15), transparent 70%),
                radial-gradient(circle at 80% 70%, rgba(255,0,255,0.15), transparent 70%);
    z-index: -2;
    animation: glowShift 10s ease-in-out infinite alternate;
}
@keyframes glowShift {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}

/* ---------- Particle Animation Canvas ---------- */
#particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    pointer-events: none;
}

/* ---------- Body & Fonts ---------- */
body {
    font-family: 'Poppins', sans-serif;
}

/* ---------- Glassmorphism Cards ---------- */
.main-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 40px 60px;
    margin-top: 50px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.47);
    border: 1px solid rgba(255, 255, 255, 0.25);
}

/* ---------- Titles ---------- */
.big-title {
    text-align: center;
    font-size: 60px;
    font-weight: 900;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

/* ---------- Buttons ---------- */
.stButton button {
    width: 100%;
    background: linear-gradient(45deg, #00dbde, #fc00ff);
    color: white;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    box-shadow: 0 0 20px rgba(252, 0, 255, 0.4);
    transition: all 0.3s ease-in-out;
}
.stButton button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 30px rgba(0, 219, 222, 0.8);
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    margin-top: 70px;
    font-size: 16px;
    color: #e0e0e0;
    font-weight: 500;
}
</style>

<script>
/* ---------- Floating Particle Effect ---------- */
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let particles = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function createParticles(count) {
  for (let i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 2 + 1,
      dx: (Math.random() - 0.5) * 0.6,
      dy: (Math.random() - 0.5) * 0.6,
      color: `hsla(${Math.random() * 360}, 100%, 70%, 0.8)`
    });
  }
}
createParticles(120);

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();

    p.x += p.dx;
    p.y += p.dy;

    if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
    if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
  });
  requestAnimationFrame(animateParticles);
}
animateParticles();
</script>
"""
st.markdown(video_html, unsafe_allow_html=True)


# ---------------- ATTRACTIVE SIDEBAR DESIGN ----------------
st.markdown("""
<style>
/* Sidebar Base */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,20,40,0.8) 0%, rgba(30,30,60,0.7) 100%);
    backdrop-filter: blur(20px);
    border-right: 2px solid rgba(255,255,255,0.1);
    box-shadow: 4px 0 20px rgba(0,0,0,0.3);
}

/* Sidebar Title */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h1 {
    color: #00fff5;
    text-align: center;
    text-shadow: 0 0 8px rgba(0,255,255,0.6);
    font-weight: 800;
}

/* Sidebar Links */
[data-testid="stSidebar"] a {
    color: #e0e0e0 !important;
    font-weight: 600 !important;
    font-size: 17px !important;
    text-decoration: none !important;
    border-radius: 8px;
    padding: 10px 14px;
    display: block;
    transition: all 0.3s ease-in-out;
}

/* Hover effect for sidebar links */
[data-testid="stSidebar"] a:hover {
    background: linear-gradient(90deg, #00dbde, #fc00ff);
    color: white !important;
    box-shadow: 0 0 12px rgba(0,255,255,0.5);
    transform: translateX(5px);
}

/* Sidebar Section Title (the "app" label) */
[data-testid="stSidebar"] section div:first-child {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00dbde, #fc00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- OPTIONAL SIDEBAR CONTENT ----------------
with st.sidebar:
    st.markdown("<h2>🤖 AI System</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.markdown("---")
    st.markdown("### 📋 Navigation")

# ---------------- NAVIGATION BAR ----------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
with col2:
    if st.button("🧑 Register"):
        st.session_state.page = "register"
with col3:
    if st.button("📷 Recognition"):
        st.session_state.page = "recognition"
with col4:
    if st.button("🕓 History"):
        st.session_state.page = "history"
with col5:
    if st.button("ℹ️ About"):
        st.session_state.page = "about"

if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- PAGE CONTENTS ----------------
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">🤖 AI Face Recognition System</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2920/2920244.png", width=270)
    with col2:
        st.markdown("""
        ### 👋 Welcome to the Future of Authentication  
        This intelligent **AI-powered Face Recognition System** uses advanced computer vision to:
        - 🧠 Detect faces using Haar Cascade  
        - 🔐 Recognize registered users in real-time  
        - 📊 Track logins and attendance automatically  
        - ⚙️ Ensure privacy and accuracy  

        ---
        🚀 **Start Exploring:**  
        Choose an option from the top navigation or click below to begin.
        """)
        if st.button("✨ Launch Face Recognition"):
            with st.spinner("Activating camera & models..."):
                time.sleep(1.5)
            st.session_state.page = "recognition"

    st.markdown('<div class="footer">Made with ❤️ by <b>Riya</b> | UI Enhanced by <b>GPT-5</b></div>', unsafe_allow_html=True)

elif st.session_state.page == "register":
    exec(open("pages/02_Register_User.py").read())
elif st.session_state.page == "recognition":
    exec(open("pages/03_Recognition.py").read())
elif st.session_state.page == "history":
    exec(open("pages/04_Login_History.py").read())
elif st.session_state.page == "about":
    st.markdown('<h1 class="big-title">ℹ️ About This App</h1>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🧠 Technology Stack
    - Python, OpenCV, Streamlit  
    - Haar Cascade Classifier  
    - SQLite / CSV for Data Storage  
    - PIL for Image Processing  

    ### 💡 Key Features
    - Real-time face recognition  
    - Secure login tracking  
    - Simple user registration  
    - Beautiful & futuristic UI  

    ### 🧩 Future Enhancements
    - Deep Learning (CNN-based recognition)  
    - Role-based dashboards  
    - Face mask detection & emotion tracking  

    ---
    👩‍💻 Developed by **Riya**  
    Guided by **[Your Teacher’s Name]**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2025 Face Recognition Project | All Rights Reserved</div>', unsafe_allow_html=True)
