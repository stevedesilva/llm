import json
import os
import sys

import gradio as gr
import anthropic
from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv
from jupyter_client.consoleapp import flags
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

from website import Website

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith("sk-proj-"):
    print("API key found and looks good so far!")
else:
    print("❌ Invalid API key. Please check your .env file or the troubleshooting notebook.")

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

# Initialize client
claude = anthropic.Anthropic()

# Define the model and API endpoint
MODEL = 'gpt-4o-mini'
openai = OpenAI()

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

system_prompt = ("You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown. \
Include details of company culture, customers and careers/jobs if you have the information.")

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(website):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)

def get_all_details(url):
    website = Website(url)
    result = "Landing page:\n"
    result += website.get_contents()
    links = get_links(website)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link['url']).get_contents()
    return result

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more that 5,000 characters
    return user_prompt


def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    result = response.choices[0].message.content
    if 'ipykernel' in sys.modules:
        # We're in a Jupyter environment
        print("Running in Jupyter Notebook or IPython environment.\n\n")
        display(Markdown(result))
    else:
        # We're in a script or terminal
        print("Running in a script or terminal environment.\n\n")
        console = Console()
        console.print(Markdown(result))



def stream_brochure_gpt(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_brochure_claude(company_name, url):
    result = claude.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.7,
        system=system_prompt,
        messages=[
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    response = ""
    with result as stream:
        for text in stream.text_stream:
            response += text or ""
            yield response

# stream_brochure("Hugging Face", "https://huggingface.co")
# create_brochure("Hugging Face", "https://huggingface.co")

def stream_model(company_name, url, model):
    if model == 'GPT':
        result = stream_brochure_gpt(company_name, url)
    elif model == "Claude":
        result = stream_brochure_claude(company_name, url)
    else:
        raise ValueError("unknown model")
    yield from result

view = gr.Interface(fn=stream_model,
                    inputs=[gr.Textbox(label="Company name", placeholder="Hugging Face"),
                            gr.Textbox(label="Add website for brochure", placeholder="https://huggingface.co"),
                            gr.Dropdown(['GPT', 'Claude'], label="Select model", value='GPT')],
                    outputs=[gr.Markdown(label="Brochure:")],
                    flagging_mode="never")
view.launch(share=True)

