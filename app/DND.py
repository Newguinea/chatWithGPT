import openai
from langchain import OpenAI
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai_api_key = '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'
openai.api_key = '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'
messages = []

#when receive message use this funtion
def get_completion(prompt, model="gpt-3.5-turbo"):
    global messages
    messages.append({"role": "user", "content": prompt})
    messages = getMessages()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,  # this is the degree of randomness of the model's output
    )
    # Add assistant's response to the message list
    aiReturn = response.choices[0].message["content"]
    messages.append({"role": "assistant", "content": aiReturn})
    return aiReturn

#press the button start or restrat the game
def startGame():
    global messages
    messages = []
    starter = '''As a highly capable AI Dungeon Master, you are going to guide me through a single-player game of \
    Dungeons & Dragons. The game will take place in a randomly generated fantasy world with unique characters, \
    locations, and plot twists. 

    Generate a random character for me with a name, rank, personality traits, and items to carry, 
    
    Now, set the opening scene for our adventure. and ask a question to player
    
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
    penetrate the dense canopy, casting long shadows that dance between the trees. The path ahead is barely visible, \
    covered in a thick layer of fallen leaves and tangled roots. \
    You can't shake off the feeling that you're being watched.
    
    In the distance, you spot a flickering light, like a distant lantern in the darkness. \
    Curiosity drives you forward as you navigate the twisted paths, pushing branches and foliage aside. \
    The light leads you to a small clearing where you come across an abandoned campsite.
    
    The remnants of a campfire smolder in the center, surrounded by discarded bedrolls and empty food containers. \
    Near the fire, you notice a torn piece of parchment with a hastily scrawled message: \
    "Beware the Whispering Woods. Danger lurks within."
    
    What would you like to do, Thalia Ravenshadow?```'''
    firstAimessage = get_completion(prompt=starter)
    del messages[0] #first prompt is very large, reduce speace
    return firstAimessage

def getMessages():
    global messages
    # TODO get a mesaage list in this format, start with ai first response, if message lenth is too long, for loop delete message[1]
    # max lenth is 2000 token, use this number because want to speed up the api replay speed
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    while (llm.get_num_tokens(str(messages)) > 2000):
        del messages[1]
    return messages