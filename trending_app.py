import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import bcrypt

config_default_link = './config.yaml'


def hash_passwords(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_passwords = hashed.decode()

    return hashed_passwords


def save_users(users, filename=config_default_link):
    with open(filename, 'w') as file:
        yaml.dump(users, file)


def validate_register_info(name, email, username, config):
    if name == '' or email == '' or username == '':
        return False

    users = config['credentials']['usernames']
    user_emails = []

    for item in users.items():
        user_emails.append(item[1]['email'])

    for user in users:
        if username == user:
            st.error('Username already taken')
            return False

    return True


def register_new_user(config):
    st.title("Register User")

    name = st.text_input("Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    repeat_password = st.text_input("Repeat Password", type="password")

    if password != repeat_password:
        st.warning('Passwords do not match')

    if st.button("Register"):
        if validate_register_info(name, email, username, config):
            hashed_password = hash_passwords(password)

            config['credentials']['usernames'][username] = {
                'name': name,
                'password': hashed_password,
                'email': email,
            }

            with open(config_default_link, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            st.success('User registered successfully!')
        else:
            st.error("An error occurred during registration.")


def main():
    with open(config_default_link) as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    if 'register' not in st.session_state:
        st.session_state['register'] = False

    if st.session_state['register']:
        st.sidebar.title("Register User")
        register_new_user(config)

        if st.sidebar.button("Back to Login"):
            st.session_state['register'] = False
            st.experimental_rerun()
    else:
        # Create a login widget
        name, authentication_status, username = authenticator.login()

        if authentication_status:
            st.sidebar.success("You are logged in")
            authenticator.logout("Logout", "sidebar")

            st.title("TikTokTechJam-CLOCK")

            tab1, tab2, tab3 = st.tabs(
                ["Create Content/Video/Audio", "Create Video by Motion", "Create Script"])

            with tab1:
                st.header("Create Content, Video, and Audio")

                if 'content' not in st.session_state:
                    content_text = st.text_area(
                        "Enter text to generate content", key='generate_content')

                    if st.button("Generate Content"):
                        st.session_state['content'] = "Generated content from: " + content_text
                        st.experimental_rerun()

                if 'content' in st.session_state:
                    st.write(st.session_state['content'])

                    if 'video' not in st.session_state and 'audio' not in st.session_state:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Back to Content Generation"):
                                del st.session_state['content']
                                st.experimental_rerun()

                        with col2:
                            if st.button("Convert Content to Video"):
                                st.session_state['video'] = "Generated video from content:"
                                st.experimental_rerun()

                        with col3:
                            if st.button("Convert Content to Audio"):
                                st.session_state['audio'] = "Generated audio from content: "
                                st.experimental_rerun()

                    if 'video' in st.session_state:
                        st.write(st.session_state['video'])
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("Back to Content Generation"):
                                del st.session_state['content']
                                del st.session_state['video']
                                st.experimental_rerun()

                        with col2:
                            if st.button("Back to Video or Audio Generation"):
                                del st.session_state['video']
                                st.experimental_rerun()

                    if 'audio' in st.session_state:
                        st.write(st.session_state['audio'])
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("Back to Content Generation"):
                                del st.session_state['content']
                                del st.session_state['audio']
                                st.experimental_rerun()

                        with col2:
                            if st.button("Back to Video or Audio Generation"):
                                del st.session_state['audio']
                                st.experimental_rerun()

            with tab2:
                st.header("Create Video by Motion")

                if 'motion_video' not in st.session_state:
                    motion_text = st.text_area(
                        "Enter text to generate motion video", "")
                    motion_video = st.file_uploader(
                        "Upload video for motion", type=["mp4", "mov", "avi"])
                    if st.button("Generate Motion Video"):
                        st.session_state['motion_video'] = "Generated motion video from: " + motion_text
                        st.experimental_rerun()

                if 'motion_video' in st.session_state:
                    st.write(st.session_state['motion_video'])

                    if 'motion_audio_video' not in st.session_state:
                        if st.button("Add Audio to Motion Video"):
                            st.session_state['motion_audio_video'] = "Generated motion video with audio"
                            st.experimental_rerun()
                        if st.button("Back to Motion Video Generation"):
                            del st.session_state['motion_video']
                            st.experimental_rerun()

                    if 'motion_audio_video' in st.session_state:
                        st.write(st.session_state['motion_audio_video'])
                        if st.button("Back to Motion Video Generation"):
                            del st.session_state['motion_audio_video']
                            st.experimental_rerun()

            with tab3:
                st.header("Generate Script")

                if 'script' not in st.session_state:
                    script_text_2 = st.text_area(
                        "Enter text to generate script", key='generate_script')

                    if st.button("Generate Script"):
                        st.session_state['script'] = "Generated script from: " + \
                            script_text_2
                        st.experimental_rerun()

                if 'script' in st.session_state:
                    st.write(st.session_state['script'])
                    if st.button("Back to Script Generation"):
                        del st.session_state['script']
                        st.experimental_rerun()

        elif authentication_status == False:
            st.error('Username/password is incorrect')
            st.session_state['register'] = False
        elif authentication_status == None:
            st.warning('Please enter your username and password')
            st.session_state['register'] = False

        if st.sidebar.button("Register", key='register_new_user'):
            st.session_state['register'] = True
            st.experimental_rerun()


if __name__ == "__main__":
    main()
