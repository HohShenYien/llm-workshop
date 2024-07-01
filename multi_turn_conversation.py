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

past_conversations = []

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    past_conversations.append({"role": "user", "parts": [user_input]})
    responses = model.generate_content(
        past_conversations,
        generation_config=generation_config,
        stream=False,
    )
    print(f"AI: {responses.text}")
    past_conversations.append({"role": "model", "parts": [responses.text]})
