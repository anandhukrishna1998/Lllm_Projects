

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader, UnstructuredPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv
import PyPDF2
import os

# Load environment variables
load_dotenv()
groq_api_key = os.environ['GROQ_API_KEY']
print(groq_api_key)

# Set up Streamlit UI configuration
st.set_page_config(page_title="RAG ChatBot", layout="wide")

# Initialize session state
if "vectors" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings()
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Ask me anything and I'll uncover your answers based on provided documents."}
    ]

# Sidebar for data input options
with st.sidebar:
    st.title("RAG Chatbot")
    st.write("Upload or input your data to build the knowledge base.")
    data_option = st.radio("Select Input Option:", ["Paste Link", "Upload PDF", "Enter Plain Text"])
    uploaded_data = None

    if data_option == "Paste Link":
        url = st.text_input("Enter the URL:")
        if url and st.button("Load URL"):
            with st.spinner("Fetching content from the URL..."):
                loader = WebBaseLoader(url)
                uploaded_data = loader.load()

    elif data_option == "Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file:
            with st.spinner("Reading PDF..."):
                # Using PyPDF2 to extract text from the PDF
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                uploaded_data = [Document(page_content=text)]

    elif data_option == "Enter Plain Text":
        plain_text = st.text_area("Enter text:")
        if plain_text and st.button("Submit Text"):
            uploaded_data = [Document(page_content=plain_text)]

# Process data and initialize the vector database
if uploaded_data:
    with st.spinner("Processing documents..."):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(uploaded_data)
        vectors = FAISS.from_documents(final_documents, st.session_state.embeddings)
        st.session_state.vectors = vectors
        st.success("Knowledge base updated!")

# Chat functionality
if "vectors" in st.session_state:
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-70b-versatile"
    )

    prompt_template = ChatPromptTemplate.from_template(
        """
        Answer the questions based on the provided context only.
        Please provide the most accurate response based on the question.
        <context>
        {context}
        <context>
        Question: {input}
        """
    )
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided input
    if input_text := st.chat_input("Type your question here..."):
        # Store user input
        st.session_state.messages.append({"role": "user", "content": input_text})
        with st.chat_message("user"):
            st.write(input_text)

        # Generate response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = retrieval_chain.invoke({"input": input_text})["answer"]
                    st.write(response)
            # Store assistant's response
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please upload or input data to enable the chatbot.")
