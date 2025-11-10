import streamlit as st
import cv2
import numpy as np
import face_recognition
import json
import os
from datetime import datetime
import sqlite3

st.title(" Face Recognition")

if 'run' not in st.session_state:
    st.session_state['run'] = False

start_stop = st.button("Start Webcam" if not st.session_state['run'] else "Stop Webcam")

if start_stop:
    st.session_state['run'] = not st.session_state['run']

# Load known encodings
db_path = "users/encodings.json"
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        known_db = json.load(f)
    known_names = list(known_db.keys())
    known_encodings = [np.array(known_db[name]) for name in known_names]
else:
    st.warning("No users registered yet.")
    known_names = []
    known_encodings = []

FRAME_WINDOW = st.image([])

# Setup database
conn = sqlite3.connect('login_times.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timestamp TEXT
    )
''')
conn.commit()

def log_login(name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logins (name, timestamp) VALUES (?, ?)", (name, timestamp))
    conn.commit()

if st.session_state['run'] and known_encodings:
    video_capture = cv2.VideoCapture(0)
    while st.session_state['run']:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                confidence = (1 - face_distances[best_match_index]) * 100
                if matches[best_match_index]:
                    name = f"{known_names[best_match_index]} ({confidence:.2f}%)"
                    log_login(known_names[best_match_index])
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            color = (0, 255, 0) if "Unknown" not in name else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    video_capture.release()
else:
    if not st.session_state['run']:
        st.info("Click 'Start Webcam' to begin recognition.")
