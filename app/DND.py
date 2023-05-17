# app/DND.py
import openai
from langchain import OpenAI
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai_api_key = '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'
openai.api_key = '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'
class GameSession:
    def __init__(self):
        self.messagesShow = []
        self.messagesSend = []
        self.chatCount = 0  # 新添加的属性，用于记录对话数量

    #when receive message use this function
    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        self.messagesShow.append({"role": "user", "content": prompt})
        self.messagesSend.append({"role": "user", "content": prompt + str(self.chatCount)})
        self.messagesSend = self.getMessages()
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.messagesSend,
            temperature=0.2,  # this is the degree of randomness of the model's output
        )
        # Add assistant's response to the message list
        aiReturn = response.choices[0].message["content"]
        self.chatCount += 1  # 在AI回复后增加对话计数器的值
        self.messagesSend.append({"role": "assistant", "content": aiReturn})
        self.messagesShow.append({"role": "assistant", "content": aiReturn})
        return aiReturn

    #press the button start or restrat the game
    def startGame(self):
        self.messagesSend = []
        self.messagesShow = []
        starter = '''As a highly capable AI Dungeon Master, you are going to guide me through a single-player game of \
        Dungeons & Dragons. The game will take place in a randomly generated fantasy world with unique characters, \
        locations, and plot twists. 
    
        Generate a random character for me with a name, rank, personality traits, and items to carry, 
        Now, set the opening scene for our adventure. and ask a question related to this game, as a host of this game\
        you need to chat with the player and ask the player choice, and player should be making progress step by step\
        you should make 10 - 20 times response untill game end. as the limit of 4096 token, speed of your replay, so\
        I send your mesaages with limit 2000 tokens message length, if the message is too long, it will cut the \
        the thired message in message list, and you can see in the end of user prompt has a count number, that is the \
        number of times the user reply, {"role": "user", "content": "prompt3")}, that 3 is means it is the 3 + 1 = 4\
        The user's fourth response
        
        refer to the format below Generate your first output
        ```{format}```
        
        format = ```Name: Thalia Ravenshadow
        Rank: Rogue
        Personality Traits: Quick-witted, cautious, and resourceful
        Items: Dagger, lockpicks, a small vial of poison, and a hooded cloak
        
        Scene for your adventure:
        
        You find yourself standing at the entrance of a dense forest known as the Whispering Woods. The towering trees loom\
         overhead, their ancient branches reaching out like skeletal fingers. The air is thick with an eerie silence, \
         broken only by the occasional hoot of an owl or the rustling of leaves underfoot.
        
        As you take your first step into the forest, the world around you seems to change. The daylight struggles to \
        penetrate the dense canopy, casting long shadows that dance between the trees. The path ahead is barely \
        visible, covered in a thick layer of fallen leaves and tangled roots. \
        You can't shake off the feeling that you're being watched.
        
        In the distance, you spot a flickering light, like a distant lantern in the darkness. \
        Curiosity drives you forward as you navigate the twisted paths, pushing branches and foliage aside. \
        The light leads you to a small clearing where you come across an abandoned campsite.
        
        The remnants of a campfire smolder in the center, surrounded by discarded bedrolls and empty food containers. \
        Near the fire, you notice a torn piece of parchment with a hastily scrawled message: \
        "Beware the Whispering Woods. Danger lurks within."
        
        What would you like to do, Thalia Ravenshadow?```'''
        firstAimessage = self.get_completion(prompt=starter)
        # del self.messagesSend[0] #first prompt is very large, reduce speace
        # del self.messagesShow[0]  # first prompt is very large, reduce speace
        return firstAimessage

    def getMessages(self):
        # TODO get a mesaage list in this format, start with ai first response, if message lenth is too long, for loop delete message[1]
        # max lenth is 2000 token, use this number because want to speed up the api replay speed
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        while (llm.get_num_tokens(str(self.messagesSend)) > 2000):
            del self.messagesSend[2]
        return self.messagesSend