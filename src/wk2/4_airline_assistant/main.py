import os
import json
from http.client import responses

from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"

# Initialize clients
openai = OpenAI()

system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


ticket_prices = {"london" : "£100", "paris" : "£150", "new york" : "£500", "tokyo" : "£800"}

def get_ticket_price(destination):
    print(f"Tool get_ticket_price called for {destination}")
    destination = destination.lower()
    return ticket_prices.get(destination, "Unknown")



price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type" : "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city to which the customer wants to buy a ticket. For example, 'London', 'Paris', 'New York', or 'Tokyo'."
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False,
    },
}

tools=[{"type":"function","function": price_function}]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id,
    }
    return response, city

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content




gr.ChatInterface(fn=chat,type="messages").launch()






