# TikTokTechJam-CLOCK

The TikTokTechJam-CLOCK directory will contain the following files:

- **config.yaml**: This file stores some configuration about the authentication. Some simple information includes the expiration date for each user, username, password, email, etc.
- **generate_hashpassword.py**: This Python script initializes the config.yaml file, with 2 default users when initializing the project.
- **text_to_sound.py**: This Python script takes prompts from the users and can be modified to best fit their requirements. It then generates the sound and exports it as a wav file.
- **text2text.py**: This Python script allows users to generate a script and an overview video by providing a prompt.
- **video_pose_prompt.py**: Supports Streamlit to facilitate user interaction for creating videos where a character's motions are based on user prompts, aiming to resemble provided motion reference videos.
- **set_up_environment.ipynb**: Aids in loading the model and setting up necessary libraries.
- **scaler.pt**: Automatically placed in the `./FollowYourPose/checkpoints/followyourpose` directory to support the execution of the "Create Video by Motion" function.
- **trending_app.py**: Main script for the web application. This Python script creates a login page, register page, the main page which has 3 features above, and some logic about authentication.
- **text2video.py**: This Python script uses PyTorch and the Diffusers library to generate and display videos from text prompts. It initializes a video generation pipeline with a pre-trained model and sets up a custom scheduler.

## How to Run the Code

### Step 1: Set up the Environment
1. Open and execute each cell in the `set_up_environment.ipynb` file to load the model and necessary libraries.

### Step 2: Running with Anaconda
1. Open Anaconda Prompt.
2. Run the command: `conda activate streamlit_env`.
3. Navigate to the directory containing the `trending_app.py` file: `cd <path_to_directory>`.
4. Run the command: `streamlit run trending_app.py`.
5. Wait for the website to appear on the screen.
6. Choose and use the desired function.

### Step 3: Running with Terminal
1. Open VS Code.
2. Open the terminal in VS Code.
3. Navigate to the directory containing the `trending_app.py` file: `cd <path_to_directory>`.
4. Run the command: `streamlit run trending_app.py`.
5. Wait for the website to appear on the screen.
6. Choose and use the desired function.
