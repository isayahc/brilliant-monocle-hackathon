# LLM game master ♟

## Introduction

### Why

- it difficult keeping track of cards and following states for a fair game
  
### How

- use chatGPT to record audio
- only record when button is open
- display gamestates on display
- AI keeps track of all the information
  
### What

- Feed information to chatGPT
- displays information to the user(s)
- sends info to chatgpt
- make chatgpt determin the winner

### How to run

#### Needed APIs

- [OpenAI Key](https://platform.openai.com/overview)
- [ELEVENLABS key](https://elevenlabs.io/)

#### Installation Steps

#### python version

It is import to use at least python 3.10

### Windows:

1. Open the Command Prompt or PowerShell by searching for "Command Prompt" or "PowerShell" in the Start menu.

2. Navigate to the directory where you want to create a new environment using the `cd` command. For example, if you want to create the environment in `C:\Projects`, type:
   ```
   cd C:\Projects
   ```

3. Create a new virtual environment using `virtualenv`:
   ```
   python -m venv myenv
   ```

4. Activate the virtual environment:
   - Command Prompt:
     ```
     myenv\Scripts\activate
     ```
   - PowerShell:
     ```
     myenv\Scripts\Activate.ps1
     ```

5. Clone the GitHub repository using `git`:
   ```
   git clone https://github.com/isayahc/brilliant-monocle-hackathon.git
   ```

6. Navigate to the cloned repository's directory:
   ```
   cd brilliant-monocle-hackathon
   ```

7. Install the requirements using pip:
   ```
   pip install -r requirements.txt
   ```

8. Run `main.py`:
   ```
   python main.py
   ```

### Linux and macOS (Unix-based systems):

1. Open a terminal window.

2. Navigate to the directory where you want to create a new environment using the `cd` command. For example, if you want to create the environment in `/home/user/Projects`, type:
   ```
   cd /home/user/Projects
   ```

3. Create a new virtual environment using `virtualenv`:
   ```
   python -m venv myenv
   ```

4. Activate the virtual environment:
   ```
   source myenv/bin/activate
   ```

5. Clone the GitHub repository using `git`:
   ```
   git clone https://github.com/isayahc/brilliant-monocle-hackathon.git
   ```

6. Navigate to the cloned repository's directory:
   ```
   cd brilliant-monocle-hackathon
   ```

7. Install the requirements using pip:
   ```
   pip install -r requirements.txt
   ```

8. Run `main.py`:
   ```
   python main.py
   ```
