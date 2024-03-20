import streamlit as st
from PIL import Image
import os
import platform
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.llms import Replicate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
import tempfile
import time
import requests
from streamlit_lottie import st_lottie

load_dotenv()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coder = load_lottieurl("https://lottie.host/aa0dce15-5563-48ea-a2cf-b1a30ad06468/2BxQ964aYV.json")

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your Documents", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

def create_conversational_chain(vector_store):
    load_dotenv()

    llm = Replicate(
        streaming=True,
        model="replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781",
        callbacks=[StreamingStdOutCallbackHandler()],
        input={"temperature": 0.01, "max_length": 500, "top_p": 1})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                  retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                  memory=memory)
    return chain

def convert_images_to_pdf(selected_files, pdf_file):
    images_list = []
    for f in selected_files:
        try:
            images_list.append(Image.open(f).convert('RGB'))
        except IOError:
            pass
    if images_list:
        pdf_file_path = pdf_file.name + ".pdf"
        images_list[0].save(pdf_file_path, save_all=True, append_images=images_list[1:])
        return pdf_file_path
    return None

def app():
    try:
        if st.session_state.username == '':
            st.warning('Please login to access this page.')
        else:
            initialize_session_state()
            st.title("Chat With Any Documents 🤖🛸")
            st.sidebar.title("Document Processing")
            uploaded_files = st.sidebar.file_uploader("Choose a document...", accept_multiple_files=True)

            st_lottie(lottie_coder)

            with st.spinner("Operation in progress. Please wait..."):
                if uploaded_files:
                    # Convert images to PDF
                    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                        pdf_file_path = convert_images_to_pdf(uploaded_files, temp_pdf_file)
                        if pdf_file_path:
                            # Load PDF and process
                            loader = PyPDFLoader(pdf_file_path)
                            text_chunks = loader.load()

                            # Create embeddings
                            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                                                model_kwargs={'device': 'cpu'})

                            # Create vector store
                            vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

                            # Create the chain object
                            chain = create_conversational_chain(vector_store)

                            # Display chat history
                            display_chat_history(chain)

    except Exception as e:
        st.error(f"An error occurred: {e}")


