# chatWithGPT

## a project develop based on chatGPT api

1. Normal chat
2. Summary a book(longtext processing)
3. DND game(Dungeons and Dragons

##

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

### Usage

After installing all the dependencies, you can start the server by running the following command:

flask run

Then, you can access the project by entering http://localhost:5000 in your browser.


## Authors and Contact Information：
Zehua Zhu 23424251@student.uwa.edu.au

Wenjie Song 22470722@student.uwa.edu.au

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