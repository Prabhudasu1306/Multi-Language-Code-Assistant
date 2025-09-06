import streamlit as st
from ollama_helper import generate_text, DEFAULT_MODEL

st.set_page_config(page_title=" Multi-Language Code Assistant", layout="wide")

st.title(" Multi-Language Code Assistant")
st.write("Powered by **Ollama (Mistral)** running locally ")

with st.sidebar:
    st.header(" Settings")
    model = st.text_input("Model name", value=DEFAULT_MODEL)
    task = st.radio(
        "Task",
        ["Generate Code", "Explain Code", "Fix Code", "Generate Tests"],
        index=0,
    )
    
    languages = ["Python", "Java", "JavaScript", "TypeScript", "C", "C++", "Go", "Rust", 
                "Ruby", "PHP", "Swift", "Kotlin", "Scala", "HTML", "CSS", "SQL", "Bash"]
    language = st.selectbox("Programming Language", languages, index=0)

st.subheader(" Prompt or Code")
user_input = st.text_area("Enter prompt, description, or paste code:", height=200)

if st.button("Run Task"):
    if not user_input.strip():
        st.warning(" Please enter a prompt or code")
    else:
        st.info(f" Running `{task}` with model `{model}` for {language}...")
        output, detected_lang = generate_text(model, user_input, task, language)

        st.subheader(" Output")
        
        display_lang = detected_lang.lower() if detected_lang else language.lower()
        
        if task == "Explain Code":
            st.write(output)
        else:
            st.code(output, language=display_lang)