# app.py
import streamlit as st
from src.preprocessor import parse_whatsapp_chat

# Set up the main app interface
st.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp chat file (.txt format)")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read and decode the uploaded file
    file_data = uploaded_file.getvalue().decode("utf-8")
    
    # Parse the WhatsApp chat data
    df = parse_whatsapp_chat(file_data)
    
    # Display a message and preview the loaded chat data
    st.write("Chat Data Loaded Successfully! Here's a quick preview:")
    st.dataframe(df.head())

    # Extract and prepare the list of unique users for selection
    unique_users = df['User'].unique().tolist()
    
    # Remove system-generated notifications and add an "Overall" option
    if 'group_notification' in unique_users:
        unique_users.remove('group_notification')
    
    # Sort users alphabetically and add "Overall" to the top of the list
    unique_users.sort()
    unique_users.insert(0, "Overall")
    
    # Add a sidebar dropdown for user selection in analysis
    selected_user = st.sidebar.selectbox("Select User for Analysis", unique_users)

    if st.sidebar.button("Show Analysis"):
       pass