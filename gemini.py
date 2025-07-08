import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Fetch API Key securely
api_key = os.getenv("API_KEY") #API_KEY

# Check for API Key and configure Gemini
if not api_key:
    st.error("❌ API Key not found! Please make sure your .env file contains API_KEY=your_key.")
    st.stop()  # Stops execution if API key is missing
else:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Gemini: {e}")
        st.stop()

# Create Gemini model
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Failed to create Gemini model: {e}")
    st.stop()

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chat", layout="centered")
st.title("💬 Ask Gemini")
st.write("Powered by Google Generative AI")

prompt = st.text_input("Enter your question:", "")

if st.button("Generate"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                result = response.text
                st.success("Response:")
                st.write(result)

                # Generate PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Prompt: {prompt}\n\nResponse:\n{result}")

                # Save PDF file
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"gemini_response_{timestamp}.pdf"
                pdf.output(filename)

                # Streamlit download button
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📄 Download Response as PDF",
                        data=file,
                        file_name=filename,
                        mime="application/pdf"
                    )

                # Remove file after serving
                os.remove(filename)

            except Exception as e:
                st.error(f"Error generating response: {e}")
