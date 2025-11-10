import streamlit as st

st.title("🏠 Home")

st.markdown(
    """
This application allows you to:

✅ Register new users with their face data  
✅ Recognize faces in real-time via webcam  
✅ Log and view access history  

Use the sidebar to get started.
"""
)

st.image(
    "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg",
    caption="Face Recognition System",
    use_column_width=True
)
