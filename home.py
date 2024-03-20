import streamlit as st
from streamlit_option_menu import option_menu
import App,img,account,web
from openai import OpenAI

st.set_page_config(
        page_title="MAIN MENU",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        # Function to toggle chatbot interface
        def toggle_chatbot():
            st.session_state.show_chatbot = not st.session_state.show_chatbot

        # Initialize session state variables
        if "show_chatbot" not in st.session_state:
            st.session_state.show_chatbot = False

        # Sidebar option menu
       
        app = option_menu(
                menu_title='MAIN MENU',
                options=['account','DOCUMENT','IMAGE','WEBSITE'],
                icons=['person-circle','file-earmark-text','images','globe2'],
                menu_icon='house-fill',
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

            # Button to toggle chatbot interface
        with st.sidebar:
          st.button("Chat-bot🤖", on_click=toggle_chatbot)

        # Run the selected app or chatbot interface
        if st.session_state.show_chatbot:
            


            
              st.title("ChatGPT-like clone")

              client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

              if "openai_model" not in st.session_state:
                  st.session_state["openai_model"] = "gpt-3.5-turbo"

              if "messages" not in st.session_state:
                  st.session_state.messages = []

              for message in st.session_state.messages:
                  with st.chat_message(message["role"]):
                      st.markdown(message["content"])

              if prompt := st.chat_input("What is up?"):
                  st.session_state.messages.append({"role": "user", "content": prompt})
                  with st.chat_message("user"):
                      st.markdown(prompt)

                  with st.chat_message("assistant"):
                      stream = client.chat.completions.create(
                          model=st.session_state["openai_model"],
                          messages=[
                              {"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages
                          ],
                          stream=True,
                      )
                      response = st.write_stream(stream)
                  st.session_state.messages.append({"role": "assistant", "content": response})
                  
        else:
            # Run the selected app
            if app == "DOCUMENT":
                App.app()
            elif app == "IMAGE":
                img.app() 
            elif app == "account":
                account.app()
            elif app == "WEBSITE":
                web.app()           

# Initialize MultiApp
multi_app = MultiApp()

# Add apps to MultiApp
multi_app.add_app("Document", App.app)
multi_app.add_app("Image", img.app)
multi_app.add_app("Account", account.app)
multi_app.add_app("Website", web.app)

# Run the application
multi_app.run()
