import google.generativeai as genai
import PIL

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 128,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

## TODO: Add codes to describe image here
img = PIL.Image.open("images/poster.jpg")

responses = model.generate_content(
    ["Describe what is in the image", img],
    generation_config=generation_config,
    stream=False,
)

print(responses.text)
