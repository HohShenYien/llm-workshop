import google.generativeai as genai

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 128,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

## TODO: Add codes for multi-turn conversation here
