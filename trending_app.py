import streamlit as st


def main():
    st.title("Multi-functional Application")

    tab1, tab2 = st.tabs(
        ["Create Script/Video/Audio", "Create Video by Motion"])

    with tab1:
        st.header("Create Script, Video, and Audio")

        if 'script' not in st.session_state:
            script_text = st.text_area("Enter text to generate script", "")
            if st.button("Generate Script"):
                st.session_state['script'] = "Generated script from: " + script_text
                st.experimental_rerun()

        if 'script' in st.session_state:
            st.write(st.session_state['script'])

            if 'video' not in st.session_state:
                if st.button("Convert Script to Video"):
                    st.session_state['video'] = "Generated video from script"
                    st.experimental_rerun()
                if st.button("Back to Script Generation"):
                    del st.session_state['script']
                    st.experimental_rerun()

            if 'video' in st.session_state:
                st.write(st.session_state['video'])

                if 'audio' not in st.session_state:
                    if st.button("Convert Video to Audio"):
                        st.session_state['audio'] = "Generated audio from video"
                        st.experimental_rerun()
                    if st.button("Back to Video Generation"):
                        del st.session_state['video']
                        st.experimental_rerun()

                if 'audio' in st.session_state:
                    st.write(st.session_state['audio'])
                    if st.button("Back to Video Generation"):
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


if __name__ == "__main__":
    main()
