import unittest
from app import app, db, login_manager
from app.models import User, Chat, Message
from flask_login import login_user, logout_user, login_required, current_user
from app.DND import GameSession
from app.longtext import *

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app to use testing configuration
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

            self.user = User(username='dddd')
            self.user.set_password('dddd')
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        with self.app.app_context():
            response = self.login('test', 'test_password')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Main Page', response.data)


class ChatTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

            self.user = User(username='dddd')
            self.user.set_password('dddd')
            db.session.add(self.user)
            db.session.commit()
            self.login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='test_password'
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Log Out', response.data)

    def test_create_chat(self):
        with self.app.app_context():
            response = self.client.post('/api/chats')
            self.assertEqual(response.status_code, 200)
            self.assertTrue('id' in response.get_json())
            self.assertTrue('context' in response.get_json())

    def test_send_and_get_messages(self):
        with self.app.app_context():
            # Create chat first
            response = self.client.post('/api/chats')
            chat_id = response.get_json()['id']

            # Send message to the chat
            response = self.client.post(f'/api/chats/{chat_id}/messages', json={'content': 'Hello, world!'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['role'], 'AI')
            self.assertTrue('content' in response.get_json())
            self.assertTrue('context' in response.get_json())

            # Get messages of the chat
            response = self.client.get(f'/api/chats/{chat_id}/messages')
            self.assertEqual(response.status_code, 200)
            messages = response.get_json()
            self.assertEqual(len(messages), 2)  # One from user, one from AI
            self.assertEqual(messages[0]['role'], 'User')
            self.assertEqual(messages[0]['content'], 'Hello, world!')
            self.assertEqual(messages[1]['role'], 'AI')

    def test_delete_chat(self):
        with self.app.app_context():
            # Create chat first
            response = self.client.post('/api/chats')
            chat_id = response.get_json()['id']

            # Delete the chat
            response = self.client.delete(f'/api/chats/{chat_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['message'], 'Chat deleted')

            # Verify the chat is deleted
            response = self.client.get(f'/api/chats/{chat_id}/messages')
            self.assertEqual(response.status_code, 404)

class DNDTestcase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

            self.user = User(username='dddd')
            self.user.set_password('dddd')
            db.session.add(self.user)
            db.session.commit()
            self.login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='test_password'
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_start_game(self):
        with self.app.app_context():
            game_session = GameSession()
            first_ai_message = game_session.startGame()
            self.assertIsNotNone(first_ai_message)
            self.assertIsInstance(first_ai_message, str)

    def test_get_completion(self):
        with self.app.app_context():
            game_session = GameSession()
            prompt = "You find a treasure chest. What do you do?"
            ai_response = game_session.get_completion(prompt)
            self.assertIsNotNone(ai_response)
            self.assertIsInstance(ai_response, str)

class LongTextTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

            self.user = User(username='dddd')
            self.user.set_password('dddd')
            db.session.add(self.user)
            db.session.commit()
            self.login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='test_password'
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_get_reply(self):
        with self.app.app_context():
            text = "This is a long text for testing purposes."
            final_prompt = "What do you think about this text?"
            compress_prompt = "Please compress the text and provide key information."

            response = getReply(text, final_prompt, compress_prompt)

            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)

    def test_compress_text(self):
        with self.app.app_context():
            text = "This is a long text for testing purposes."
            compress_prompt = "Please compress the text and provide key information."
            final_prompt = "What do you think about this text?"

            compressed_text = compressText(text, compress_prompt, final_prompt)

            self.assertIsNotNone(compressed_text)
            self.assertIsInstance(compressed_text, str)

    def test_final_prompt(self):
        with self.app.app_context():
            text = "This is a long text for testing purposes."
            final_prompt = "What do you think about this text?"

            output = finalPrompt(final_prompt, text)

            self.assertIsNotNone(output)
            self.assertIsInstance(output, str)
