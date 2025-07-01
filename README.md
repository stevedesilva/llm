# LLM Engineering 


## Set Up the Project in PyCharm

    Open PyCharm

    File > Open your my-python-project/

    Go to Settings > Project > Python Interpreter

        Select your Conda environment (my_project_env)

    Create run configurations if needed (e.g., for main.py)

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyD7foNAaMeP84XOjojGgEagtqVYH8vsal0" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'

