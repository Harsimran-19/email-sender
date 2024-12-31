import streamlit as st
import pandas as pd
from src.email_sender import send_bulk_emails

def main():
    st.title("Email Automation System")
    
    subject = st.text_input("Subject")
    from_name = st.text_input("From Name")
    body = st.text_area("Email Body")
    
    # File uploads
    uploaded_file = st.file_uploader("Upload CSV/Excel file", type=['csv', 'xlsx'])
    attachments = st.file_uploader("Upload Attachments", type=['pdf', 'docx', 'xlsx', 'jpg', 'png'], accept_multiple_files=True)
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        email_column = st.selectbox("Select Email Column", df.columns)
        
        if st.button("Send Emails"):
            with st.spinner("Sending emails..."):
                successful_sends, unsuccessful_sends = send_bulk_emails(
                    df[email_column].tolist(),
                    subject,
                    from_name,
                    body,
                    attachments
                )
                st.success(f"Sent {successful_sends} emails successfully and {unsuccessful_sends} emails successfully!")

if __name__ == "__main__":
    main()