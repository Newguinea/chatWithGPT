# chatWithGPT

## Purpose and design of the project

This web application is designed to provide interactive experiences and services powered by OpenAI's GPT-3.5 model through the ChatGPT API. It features three main components, each serving a unique purpose, to provide users with versatile ways of leveraging the capabilities of the AI model.
1. AIOracle

2. Purify

3. AdventureCraft

### AIOracle
The first component is the "AIOracle". Here, users can engage in a conversation with the AI model, similar to a chatbot. This component allows users to ask questions, request information, or just have a friendly chat, showcasing the conversational ability of the GPT-4 model.

### Purify
The second component is the "Purify" feature. This feature allows users to upload a text file containing a long story, and the AI model will generate a concise summary of the content. It's a powerful tool for quickly understanding the main points of a lengthy text, ideal for students, researchers, or anyone dealing with extensive reading materials.

### AdventureCraft
The third component is the "AdventureCraft", an interactive game built around the classic Dungeons & Dragons theme. In this game, the AI model takes on the role of the game master, guiding users through the game by asking them to make decisions at key points. This showcases the imaginative storytelling and interactive capabilities of the AI model, providing a unique gaming experience for users.

Each of these components is designed with an easy-to-use interface and leverages the powerful capabilities of the GPT-4 model to provide useful and entertaining experiences for users.


## Application Architecture
Our web application adopts a 3-tier architecture: the Presentation Layer, the Business Logic Layer, and the Data Access Layer. 

### Presentation Layer
The user interface is built with HTML and CSS, enhanced with Bootstrap for responsive and modern design and jQuery for interactive elements. These technologies provide users with an interactive and intuitive environment to interact with our application across different devices.

### Business Logic Layer
The server-side of our application is powered by Flask, a lightweight and flexible Python web framework. Flask takes care of routing, handling HTTP requests and responses, and serves as a bridge between the user interface and our database.

### Data Access Layer
The data access layer interacts with our SQLite database, where all user information and other data are stored and managed. It is responsible for performing all CRUD (Create, Read, Update, Delete) operations on the data, as required by the Business Logic Layer.

### Flow of Control
1. Users interact with the Presentation Layer (the HTML/CSS interface, enhanced with Bootstrap and jQuery).

2. User actions trigger HTTP requests, which are sent from the Presentation Layer to the Business Logic Layer (Flask).

3. Flask processes the requests and interacts with the Data Access Layer if necessary (e.g., reading from or writing to the SQLite database).

4. The results (data or status messages) are sent back from Flask to the Presentation Layer.
5. The Presentation Layer updates the user interface based on the results, showing the most up-to-date data or status messages to the user.

## Installation and Usage Guide: 

### Installation

First, make sure that Python and pip are installed on your system. If they are not installed, you can download and install Python from here. Pip is usually installed automatically during the Python installation process.

All the dependencies for this project are listed in the requirements.txt file. You can install these dependencies by running the following command:

pip install -r requirements.txt (we expected this program to be run in the venv with python version 3.10)

And do create a .env in app directory, and add this line.

openai.api_key = "your openai api key"

### Usage

After installing all the dependencies, you can start the server by running the following command:

flask run

Then, you can access the project by entering http://localhost:5000 in your browser.

## Testing Guide:

The web application includes several unit tests written using Selenium WebDriver in conjunction with Python's unittest framework. These tests validate the functionality of the web application.
### Test Environment Setup
First of all check this link, https://chromedriver.chromium.org/downloads to download the chromedriver.

If you are using other browsers, you can download the corresponding driver similarly.

Then add this line to your .env file.

CHROMEDRIVER_PATH="your chromedriver path"

### Test cases
1. LoginTestCase: Checks the login functionality of the web application. The test navigates to the login page, enters valid credentials, submits the login form, and verifies the redirection to the home page.

2. ChatSeleniumTestCase: Tests the chat functionality. It logs in, navigates to the chat page, creates a new chat, sends a message, and verifies the sent message.

3. DNDTestCase: Checks the game session functionality. It logs in, navigates to the game page, starts a game session, sends a chat message, and verifies if the message appears in the chat history.

4. longTextTestCase: Tests the text processing functionality. It logs in, navigates to the processing page, inputs a file and required parameters, starts the processing, and verifies if the result is displayed.

### How to run
To run the tests, first of all make sure the venv is activated, then simply run the following command:

python -m unittest test_app or python -m unittest selenium_test

## Commit History



## Authors and Contact Information：
@newguinea[https://github.com/Newguinea] 23424251@student.uwa.edu.au

wenjie 22470722@student.uwa.edu.au

## Acknowledgments: 

Thanks to the professor and tutor for your guidance. Your courses have helped us a lot

for this project, we refer to some tutorials and other people's projects, which inspired us a lot

tutorial of my units
https://teaching.csse.uwa.edu.au/units/CITS3403/

flask backend and database:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

ChatGPT Prompt Engineering for Developers:
https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/

flask test(this materia is in Chinese): (Very good tutorial, love comes from porcelain)
https://tutorial.helloflask.com/test/

I'd like to extend my gratitude to a number of fellow students with whom we've battled day and night in the library, exchanging ideas and discussing concepts. Unfortunately, most of them do not wish their names to be written here. Regardless, I want to say sincerely, thank you all.
