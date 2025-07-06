import streamlit as st
import google.generativeai as genai
import json
import os


# --- Configuration ---
# Your Google API Key should be set as an environment variable or provided here.
# For Canvas environment, leave it as an empty string. The environment will inject it.
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Leave this empty for Canvas to inject the key

# with open("/content/credentials.json",) as f:
#   data = json.load(f)
#   print(len(data))


# Configure the Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    # This block is primarily for local development if the key isn't in env vars.
    # In Canvas, the key is handled automatically.
    try:
        # Attempt to get API key from Streamlit secrets if running locally
        # and not in Canvas with __initial_auth_token.
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        else:
            st.error("Google API Key not found. Please set it as an environment variable or in Streamlit secrets.")
            st.stop()
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}. Please ensure your API key is set.")
        st.stop()

# Initialize the Gemini model
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}. Please check your API key and network connection.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="Gemini AI Study Assistant", layout="wide")

st.title("📚 Gemini AI Study Assistant")
st.markdown("""
This application leverages Google's Gemini LLM to help students with:
- **Debugging Code:** Get explanations for errors and suggestions for fixes.
- **Explaining Complex Topics:** Understand difficult concepts with simple examples.
- **Explaining Data Analysis Concepts:** Grasp the nuances of various data analysis techniques.
""")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["🐛 Code Debugger", "💡 Topic Explainer", "📊 Data Analysis Concepts"])

# --- Tab 1: Code Debugger ---
with tab1:
    st.header("Code Debugger")
    st.markdown("Paste your code below and let Gemini help you debug it.")

    code_input = st.text_area("Enter your code here:", height=300, key="code_debugger_input",
                              placeholder="""
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

data = [1, 2, 3, 4, 5]
print(calculate_average(data))
                              """)

    if st.button("Debug Code", key="debug_button"):
        if code_input:
            with st.spinner("Debugging your code..."):
                try:
                    prompt = f"Debug the following code. Explain any errors, suggest fixes, and provide a corrected version if necessary:\n\n```\n{code_input}\n```"
                    response = model.generate_content(prompt)
                    st.subheader("Debugging Report:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred while debugging: {e}")
        else:
            st.warning("Please enter some code to debug.")

# --- Tab 2: Topic Explainer ---
with tab2:
    st.header("Topic Explainer")
    st.markdown("Enter any complex topic you want to understand better.")

    topic_input = st.text_input("Enter the topic:", key="topic_explainer_input",
                                 placeholder="Quantum Entanglement")

    if st.button("Explain Topic", key="explain_topic_button"):
        if topic_input:
            with st.spinner(f"Explaining '{topic_input}'..."):
                try:
                    prompt = f"Explain the following topic in simple terms, using analogies and a clear, relatable example:\n\nTopic: {topic_input}"
                    response = model.generate_content(prompt)
                    st.subheader(f"Explanation for '{topic_input}':")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred while explaining the topic: {e}")
        else:
            st.warning("Please enter a topic to explain.")

# --- Tab 3: Data Analysis Concepts ---
with tab3:
    st.header("Data Analysis Concepts")
    st.markdown("Get clear explanations for various data analysis concepts.")

    concept_input = st.text_input("Enter a data analysis concept:", key="data_concept_input",
                                   placeholder="P-value in Hypothesis Testing")

    if st.button("Explain Concept", key="explain_concept_button"):
        if concept_input:
            with st.spinner(f"Explaining '{concept_input}'..."):
                try:
                    prompt = f"Explain the data analysis concept '{concept_input}' in detail, including its purpose, how it's used, and a simple example if applicable."
                    response = model.generate_content(prompt)
                    st.subheader(f"Explanation for '{concept_input}':")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred while explaining the concept: {e}")
        else:
            st.warning("Please enter a data analysis concept.")

st.markdown("---")
st.info("Powered by Google Gemini LLM")
