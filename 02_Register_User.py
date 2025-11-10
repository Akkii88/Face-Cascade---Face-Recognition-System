import streamlit as st
import cv2
import face_recognition
import numpy as np
import json
import os

st.title(" Register New User")

# --- Ensure users folder exists ---
os.makedirs("users", exist_ok=True)
ENCODING_FILE = "users/encodings.json"

# --- Load existing encodings ---
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "r") as f:
        known_db = json.load(f)
else:
    known_db = {}

# --- Input field for user name ---
name = st.text_input("Enter your name to register:")

# --- Start webcam ---
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

capture = st.button(" Capture and Register Face")

if capture and name.strip():
    st.info("Capturing face... Please look at the camera.")
    ret, frame = camera.read()
    if not ret:
        st.error("Failed to access camera.")
    else:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            known_db[name] = face_encoding.tolist()

            with open(ENCODING_FILE, "w") as f:
                json.dump(known_db, f)

            st.success(f" Face registered successfully for '{name}'!")
        elif len(face_locations) == 0:
            st.warning("No face detected. Please try again.")
        else:
            st.warning("Multiple faces detected. Please ensure only one face is visible.")
else:
    ret, frame = camera.read()
    if ret:
        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
