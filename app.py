import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. AI CONFIGURATION
# Note: On Streamlit Cloud, we use st.secrets to keep your key hidden from the public.
# You will set this up in the Streamlit Dashboard later.
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. HELPER FUNCTION: Extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 3. STREAMLIT UI LAYOUT
st.set_page_config(page_title="AI Career Agent", page_icon="🤖", layout="wide")

st.title("AI Career Agent 🤖")
st.markdown("### Optimize your CV for the 'Masses'")

# Create a layout with two columns
left_col, right_col = st.columns(2)

with left_col:
    st.header("Step 1: Job Details")
    job_description = st.text_area(
        "Paste the Job Description (JD) here:", 
        height=300, 
        placeholder="Copy requirements from LinkedIn, Amazon, etc."
    )

with right_col:
    st.header("Step 2: Your Resume")
    uploaded_file = st.file_uploader("Upload your CV in PDF format", type="pdf")

# 4. EXECUTION LOGIC
if st.button("🚀 Analyze Match"):
    if job_description and uploaded_file:
        with st.spinner("Analyzing the gap between your CV and the JD..."):
            # Process the PDF
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # AI Prompt Engineering
            prompt = f"""
            You are a professional recruiter. Compare the following Resume with the Job Description.
            1. Provide a Match Score (0-100%).
            2. Identify 5 missing critical keywords.
            3. Rewrite 3 experience bullet points to better align with the JD using the STAR method.
            
            Job Description: {job_description}
            Resume Content: {resume_text}
            """
            
            # Get response from Gemini
            response = model.generate_content(prompt)
            
            # Display Results
            st.success("Analysis Complete!")
            st.markdown("---")
            st.markdown(response.text)
    else:
        st.warning("Please ensure both the Job Description is pasted and a CV is uploaded.")
