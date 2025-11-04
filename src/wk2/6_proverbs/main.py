import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print("✓ OpenAI API Key is set")
else:
    print("❌ OpenAI API Key not set")

# Initialize OpenAI client
openai = OpenAI()

# Model configuration
MODEL = "gpt-4o-mini"

# System prompts for different proverb functions
GENERATE_SYSTEM_PROMPT = """You are a wise sage who knows proverbs from cultures around the world. 
When given a topic or theme, you generate relevant and meaningful proverbs. 
You can create proverbs in the style of different cultures when requested.
Always provide the proverb and a brief explanation of its meaning."""

EXPLAIN_SYSTEM_PROMPT = """You are a knowledgeable teacher who explains the meaning and wisdom behind proverbs.
When given a proverb, you provide a clear, insightful explanation of its meaning, origin (if known), 
and how it can be applied to modern life."""

CULTURE_SYSTEM_PROMPT = """You are an expert in world cultures and their proverbs.
When asked about proverbs from a specific culture, you provide authentic proverbs from that culture
along with context about their meaning and significance."""


def generate_proverb(topic, culture="general"):
    """Generate a proverb based on a topic and optional culture."""
    if not topic or not topic.strip():
        return "❌ Please enter a topic or theme."
    
    try:
        user_prompt = f"Generate a proverb about '{topic}'"
        if culture and culture.lower() != "general":
            user_prompt += f" in the style of {culture} culture"
        user_prompt += ". Provide the proverb and a brief explanation of its meaning."
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": GENERATE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating proverb: {str(e)}\n\nPlease check your API key and internet connection."


def explain_proverb(proverb):
    """Explain the meaning of a given proverb."""
    if not proverb or not proverb.strip():
        return "❌ Please enter a proverb to explain."
    
    try:
        user_prompt = f"Explain the meaning and wisdom of this proverb: '{proverb}'"
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error explaining proverb: {str(e)}\n\nPlease check your API key and internet connection."


def get_cultural_proverbs(culture, count=3):
    """Get proverbs from a specific culture."""
    if not culture or not culture.strip():
        return "❌ Please enter a culture name."
    
    try:
        user_prompt = f"Provide {count} authentic proverbs from {culture} culture. "
        user_prompt += "For each proverb, include its meaning and cultural significance."
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CULTURE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error fetching cultural proverbs: {str(e)}\n\nPlease check your API key and internet connection."


# Create Gradio interface with tabs for different functions
with gr.Blocks(title="Proverbs App") as app:
    gr.Markdown("# 🌟 Proverbs App")
    gr.Markdown("Explore the wisdom of proverbs from around the world")
    
    with gr.Tab("Generate Proverb"):
        gr.Markdown("### Generate a proverb based on a topic")
        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="Topic or Theme",
                    placeholder="e.g., friendship, patience, wisdom...",
                    lines=2
                )
                culture_input = gr.Textbox(
                    label="Culture (optional)",
                    placeholder="e.g., Chinese, African, Japanese, or leave blank for general",
                    lines=1
                )
                generate_btn = gr.Button("Generate Proverb", variant="primary")
            with gr.Column():
                generate_output = gr.Textbox(
                    label="Generated Proverb",
                    lines=10,
                    show_copy_button=True
                )
        
        generate_btn.click(
            fn=generate_proverb,
            inputs=[topic_input, culture_input],
            outputs=generate_output
        )
    
    with gr.Tab("Explain Proverb"):
        gr.Markdown("### Get an explanation of a proverb")
        with gr.Row():
            with gr.Column():
                proverb_input = gr.Textbox(
                    label="Enter a Proverb",
                    placeholder="e.g., A stitch in time saves nine",
                    lines=3
                )
                explain_btn = gr.Button("Explain", variant="primary")
            with gr.Column():
                explain_output = gr.Textbox(
                    label="Explanation",
                    lines=10,
                    show_copy_button=True
                )
        
        explain_btn.click(
            fn=explain_proverb,
            inputs=proverb_input,
            outputs=explain_output
        )
    
    with gr.Tab("Cultural Proverbs"):
        gr.Markdown("### Explore proverbs from different cultures")
        with gr.Row():
            with gr.Column():
                culture_select = gr.Textbox(
                    label="Culture",
                    placeholder="e.g., Chinese, Japanese, African, Arabic, Native American...",
                    lines=1
                )
                count_slider = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                    label="Number of Proverbs"
                )
                cultural_btn = gr.Button("Get Proverbs", variant="primary")
            with gr.Column():
                cultural_output = gr.Textbox(
                    label="Cultural Proverbs",
                    lines=15,
                    show_copy_button=True
                )
        
        cultural_btn.click(
            fn=get_cultural_proverbs,
            inputs=[culture_select, count_slider],
            outputs=cultural_output
        )
    
    gr.Markdown("---")
    gr.Markdown("*Powered by OpenAI GPT-4o-mini*")

if __name__ == "__main__":
    app.launch()
