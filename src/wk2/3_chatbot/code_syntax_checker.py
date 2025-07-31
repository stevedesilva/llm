# import os
# import string
#
# from dotenv import load_dotenv
# from openai import OpenAI
# import anthropic
#
# import gradio as gr
#
# load_dotenv(override=True)
#
# openai_api_key = os.getenv('OPENAI_API_KEY')
# if openai_api_key:
#     print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
# else:
#     print("OpenAI API Key not set")
#
# # anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
# # if anthropic_api_key:
# #     print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
# # else:
# #     print("Anthropic API Key not set")
# #
# # google_api_key = os.getenv('GOOGLE_API_KEY')
# # if google_api_key:
# #     print(f"Google API Key exists and begins {google_api_key[:8]}")
# # else:
# #     print("Google API Key not set")
#
#
# # Initialize clients
#
# openai = OpenAI()
# # claude = anthropic.Anthropic()
# # gemini_via_openai_client = OpenAI(
# #     api_key=google_api_key,
# #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # )
#
# # Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# # We're using cheap versions of models so the costs will be minimal
#
#
# gpt_model = "gpt-4o-mini"
# # claude_model = "claude-3-haiku-20240307"
# # gemini_model = "gemini-2.0-flash-lite"
#
# system_message = ("You are a helpful coding instructor. You help students learn python, java and golang. \
# You ask syntax questions for a selected language and then review the result\
# You give the student a score and some helpful advice to improve")
#
# # get syntax question to ask student for a given language
# def get_question(language):
#     return ""
#
# def ask_question(language):
#     question = get_question(language)
#     return question
#
# def check_answer():
#     # This function will check the answer given by the student
#     # It will return a score and some advice
#     return 0, "Good job, but you could improve by..."
#
#
# # normal launch
# # gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch()
#
# # launch in browser
# # gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)
#
# # share public link
# gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)

# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

openai = OpenAI()
MODEL = 'gpt-4o-mini'


# system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
# the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
# For example, if the customer says 'I'm looking to buy a hat', \
# you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'\
# Encourage the customer to buy hats if they are unsure what to get."
#
#
#
# system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, \
# but remind the customer to look at hats!"

system_message = ("You are a helpful coding instructor. You help students learn to code. \
You ask syntax questions for a selected language and then review the result\
You give the student a score and some helpful advice to improve")

def chat(message, history):
    relevant_system_message = system_message

    if 'java' in message:
        relevant_system_message += "Ask a question on the java language, and then check the answer."
    elif 'python' in message:
        relevant_system_message += "Ask a question on the python language, and then check the answer."
    elif 'golang' in message:
        relevant_system_message += "Ask a question on the go language, and then check the answer."
    else:
        relevant_system_message += "Ask a question on a language, and then check the answer."

    messages = [{"role": "system", "content": relevant_system_message}] + history + [
        {"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


gr.ChatInterface(fn=chat,type="messages").launch()
