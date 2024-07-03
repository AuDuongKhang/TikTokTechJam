import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def main():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Create a login widget
    name, authentication_status, username = authenticator.login()

    if authentication_status:
        authenticator.logout()

        st.title("TikTokTechJam-CLOCK")

        tab1, tab2, tab3 = st.tabs(
            ["Create Content/Video/Audio", "Create Video by Motion", "Create Script"])

        with tab1:
            st.header("Create Content, Video, and Audio")

            if 'content' not in st.session_state:
                content_text = st.text_area(
                    "Enter text to generate content", key='generate content')

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
                    "Enter text to generate script", key='generate script')

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
    elif authentication_status == None:
        st.warning('Please enter your username and password')


if __name__ == "__main__":
    main()
