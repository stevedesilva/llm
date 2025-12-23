# Proverbs App

A Gradio-based web application that lets you explore the wisdom of proverbs from around the world using AI.

## Features

### 1. Generate Proverb
- Generate proverbs based on any topic or theme
- Optional: Specify a culture (Chinese, African, Japanese, etc.) for culturally-specific proverbs
- Receive both the proverb and an explanation of its meaning

### 2. Explain Proverb
- Enter any proverb and get a detailed explanation
- Learn about the wisdom, meaning, and modern applications of proverbs
- Understand the context and origin of traditional sayings

### 3. Cultural Proverbs
- Explore authentic proverbs from specific cultures
- Choose the number of proverbs (1-5) to receive
- Learn about cultural significance and meanings

## How to Use

1. Make sure you have your OpenAI API key set in a `.env` file:
   ```
   OPENAI_API_KEY=your_key_here
   ```

2. Run the app:
   ```bash
   python main.py
   ```

3. The Gradio interface will launch in your browser

4. Choose a tab based on what you want to do:
   - **Generate Proverb**: Enter a topic and optionally a culture
   - **Explain Proverb**: Enter a proverb to understand its meaning
   - **Cultural Proverbs**: Enter a culture name to see authentic proverbs

## Examples

### Generate Proverb
- Topic: "patience"
- Culture: "Chinese" (or leave blank)

### Explain Proverb
- Proverb: "A stitch in time saves nine"

### Cultural Proverbs
- Culture: "Japanese"
- Count: 3

## Requirements

- Python 3.10+
- OpenAI API key
- Dependencies: Install from the root-level `environment_v2.yml` file in the repository
  ```bash
  # From the repository root
  conda env create -f environment_v2.yml
  conda activate llms
  ```
  Key dependencies used by this app: gradio, openai, python-dotenv

## Technology

- **Gradio**: Interactive web interface
- **OpenAI GPT-4o-mini**: AI model for generating and explaining proverbs
- **Python-dotenv**: Environment variable management
