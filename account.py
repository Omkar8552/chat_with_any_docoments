import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import requests
from streamlit_lottie import st_lottie


cred = credentials.Certificate("e-cycling-413207-6920c029f43e.json")
firebase_admin.initialize_app(cred)
def app():
# Usernm = []
    st.title('Welcome to Chat with multiple documents :')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''



    def f(): 
        try:
            user = auth.get_user_by_email(email)
            print(user.uid)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            global Usernm
            Usernm=(user.uid)
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
            
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''


        
    
        
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        

        
    
    if  not st.session_state["signedout"]: 
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')
        

        
        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")
            
            if st.button('Create my account'):
                user = auth.create_user(email = email, password = password,uid=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
                     
            st.button('Login', on_click=f)
            
            
    if st.session_state.signout:
        st.text('Name '+st.session_state.username)
        st.text('Email id: '+st.session_state.useremail)
        st.button('Sign out', on_click=t) 
            
        def load_lottieurl(url):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()

        lottie_coder = load_lottieurl("https://lottie.host/00a407ec-9de3-42b5-a9c8-b31dfa8d99d1/3MeGAoQy6q.json")

            # Custom CSS for styling
        st.markdown(
                """
                <style>
                    body {
                        background-color: #f8f9fa;
                        font-family: 'Arial', sans-serif;
                    }
                    .container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        flex-direction: column;
                    }
                    .animation-container {
                        text-align: center;
                        margin-bottom: 20px;
                    }

                    .lottie-animation {
                    width: 800px; /* Adjust the width as needed */
                    height: 500px; /* Adjust the height as needed */
                    marginLeft: '-47%',
                    }
                    .animate-text {
                        text-align:center;
                        font-size: 48px;
                        font-weight: bold;
                        color: #3498db; /* Blue color for the text */
                        animation: slide-in 1.5s ease-out;
                        justify-content: center;
                        align-items: center;

                    }
                    .sub-text {
                        text-align:center;
                        font-size: 24px;
                        color: #555;
                        margin-top: 20px;
                    }
                    @keyframes slide-in {
                        0% {
                            transform: translateY(-50px);
                            opacity: 0;
                        }
                        100% {
                            transform: translateY(0);
                            opacity: 1;
                        }
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

           
        st.markdown("<h1 class='animate-text'>👋🤖 Welcome to Your Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text'>Let's make your conversation more engaging and dynamic!</p>", unsafe_allow_html=True)
            

        if lottie_coder:
                
                st.write(f'<div class="lottie-animation">{st_lottie(lottie_coder, width=800, height=500)}</div>', unsafe_allow_html=True)

        else:
            st.error("Failed to load Lottie animation.")

            
            st.markdown("<div class='container'>", unsafe_allow_html=True)
            st.markdown("<div class='animation-container'>", unsafe_allow_html=True)

            
            st.markdown("<p class='sub-text'>Feel free to customize and enhance this page!</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)        
    

                            
    def ap():
        st.write('Posts')

    

    

                    