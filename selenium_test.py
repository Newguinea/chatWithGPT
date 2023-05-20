import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from app import app, db, login_manager
from app.models import User, Chat, Message
from flask_login import login_user, logout_user, login_required, current_user
from app.DND import GameSession
from app.longtext import *


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)  # Use the specified ChromeDriver executable path
        self.driver.get('http://127.0.0.1:5000/login')  # Replace with the URL of your Flask application

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Find the username and password input fields
        username_input = self.driver.find_element_by_id('username')
        password_input = self.driver.find_element_by_id('password')

        # Enter the username and password
        username_input.send_keys('test')
        password_input.send_keys('test_password')

        # Submit the login form
        password_input.send_keys(Keys.RETURN)

        # Check if the page contains the expected text
        main_page_text = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Main Page', main_page_text)

if __name__ == '__main__':
    unittest.main()
