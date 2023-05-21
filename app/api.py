import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Function to get completion from OpenAI API, used for conversational AI responses
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    # The model takes a prompt and generates a response
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Function to get a summary from OpenAI API, used for summarizing text in 6 words or less
def summarize(prompt, model="gpt-3.5-turbo"):
    prompt = "Summarize the following paragraph in six words or less: " + prompt
    messages = [{"role": "user", "content": prompt}]
    # The model takes a prompt and generates a summary
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]