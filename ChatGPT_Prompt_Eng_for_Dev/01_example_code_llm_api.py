# Example code for calling the openai API
# Set up your API key in the .env file
# To install the OpenAI Python library:
#############################################
# !pip install openai

# The library needs to be configured with your account's secret key, which is available on the website.
# You can either set it as the OPENAI_API_KEY environment variable before using the library:
#############################################
# !export OPENAI_API_KEY='sk-...'

#Or, set openai.api_key to its value:
#############################################
# import openai
# openai.api_key = "sk-..."

import openai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')
print(openai.api_key)

# In order to use the OpenAI library version 1.0.0, here is the code that you would use instead for the get_completion function:

client = openai.OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

