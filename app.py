# pylint: disable=line-too-long,invalid-name
"""
This module demonstrates the usage of the Vertex AI Gemini 1.5 API within a Streamlit application.
"""

from typing import List, Union

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(
    contents: Union[str, List],
    generation_config: GenerationConfig = GenerationConfig(
        temperature=0.1, max_output_tokens=2048
    ),
    stream: bool = True,
) -> str:
    """Generate a response from the Gemini model."""
    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        stream=stream,
    )

    if not stream:
        return responses.text

    final_response = []
    for r in responses:
        try:
            final_response.append(r.text)
        except IndexError:
            final_response.append("")
            continue
    return " ".join(final_response)


st.header("Gemini 1.5 API", divider="rainbow")

(tab1, tab2) = st.tabs(["Generate story", "Marketing campaign"])

with tab1:
    st.subheader("Generate a story")

    # Story premise
    character_name = st.text_input(
        "Enter character name: \n\n", key="character_name", value="Mittens"
    )
    character_age = st.number_input(
        "Enter character age: \n\n", key="character_age", value=20
    )
    character_type = st.text_input(
        "What type of character is it? \n\n", key="character_type", value="Cat"
    )
    character_persona = st.text_input(
        "What personality does the character have? \n\n",
        key="character_persona",
        value="Mittens is a very friendly cat.",
    )
    character_location = st.text_input(
        "Where does the character live? \n\n",
        key="character_location",
        value="Andromeda Galaxy",
    )
    story_premise = st.multiselect(
        "What is the story premise? (can select multiple) \n\n",
        [
            "Love",
            "Adventure",
            "Mystery",
            "Horror",
            "Comedy",
            "Sci-Fi",
            "Fantasy",
            "Thriller",
        ],
        key="story_premise",
        default=["Love", "Adventure"],
    )
    creative_control = st.radio(
        "Select the creativity level: \n\n",
        ["Low", "High"],
        key="creative_control",
        horizontal=True,
    )
    length_of_story = st.radio(
        "Select the length of the story: \n\n",
        ["Short", "Long"],
        key="length_of_story",
        horizontal=True,
    )

    if creative_control == "Low":
        temperature = 0.30
    else:
        temperature = 0.95

    if length_of_story == "Short":
        max_output_tokens = 2048
    else:
        max_output_tokens = 8192

    prompt = f"""Write a {length_of_story} story based on the following premise: \n
    character_name: {character_name} \n
    character_type: {character_type} \n
    character_persona: {character_persona} \n
    character_location: {character_location} \n
    character_age: {character_age} \n
    story_premise: {",".join(story_premise)} \n
    If the story is "short", then make sure to have 5 chapters or else if it is "long" then 10 chapters.
    Important point is that each chapters should be generated based on the premise given above.
    First start by giving the book introduction, chapter introductions and then each chapter. It should also have a proper ending.
    The book should have prologue and epilogue.
    """
    config = GenerationConfig(
        temperature=temperature, max_output_tokens=max_output_tokens
    )

    generate_t2t = st.button("Generate my story", key="generate_t2t")
    if generate_t2t and prompt:
        # st.write(prompt)
        with st.spinner("Generating your story..."):
            first_tab1, first_tab2 = st.tabs(["Story", "Prompt"])
            with first_tab1:
                response = get_gemini_response(
                    prompt,
                    generation_config=config,
                )
                if response:
                    st.write("Your story:")
                    st.write(response)
            with first_tab2:
                st.text(
                    f"""Parameters:\n- Temperature: {temperature}\n- Max Output Tokens: {max_output_tokens}\n"""
                )
                st.text(prompt)

with tab2:
    st.subheader("Generate your marketing campaign")

    product_name = st.text_input(
        "What is the name of the product? \n\n",
        key="campaign_product_name",
        value="ZomZoo",
    )
    product_category = st.radio(
        "Select your product category: \n\n",
        ["Clothing", "Electronics", "Food", "Health & Beauty", "Home & Garden"],
        key="product_category",
        horizontal=True,
    )
    st.write("Select your target audience: ")
    target_audience_age = st.radio(
        "Target age: \n\n",
        ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        key="target_audience_age",
        horizontal=True,
    )
    # target_audience_gender = st.radio("Target gender: \n\n",["male","female","trans","non-binary","others"],key="target_audience_gender",horizontal=True)
    target_audience_location = st.radio(
        "Target location: \n\n",
        ["Urban", "Suburban", "Rural"],
        key="target_audience_location",
        horizontal=True,
    )
    st.write("Select your marketing campaign goal: ")
    campaign_goal = st.multiselect(
        "Select your marketing campaign goal: \n\n",
        [
            "Increase brand awareness",
            "Generate leads",
            "Drive sales",
            "Improve brand sentiment",
        ],
        key="campaign_goal",
        default=["Increase brand awareness", "Generate leads"],
    )
    if campaign_goal is None:
        campaign_goal = ["Increase brand awareness", "Generate leads"]
    brand_voice = st.radio(
        "Select your brand voice: \n\n",
        ["Formal", "Informal", "Serious", "Humorous"],
        key="brand_voice",
        horizontal=True,
    )
    estimated_budget = st.radio(
        "Select your estimated budget ($): \n\n",
        ["1,000-5,000", "5,000-10,000", "10,000-20,000", "20,000+"],
        key="estimated_budget",
        horizontal=True,
    )

    prompt = f"""Generate a marketing campaign for {product_name}, a {product_category} designed for the age group: {target_audience_age}.
    The target location is this: {target_audience_location}.
    Aim to primarily achieve {campaign_goal}.
    Emphasize the product's unique selling proposition while using a {brand_voice} tone of voice.
    Allocate the total budget of {estimated_budget}.
    With these inputs, make sure to follow following guidelines and generate the marketing campaign with proper headlines: \n
    - Briefly describe company, its values, mission, and target audience.
    - Highlight any relevant brand guidelines or messaging frameworks.
    - Provide a concise overview of the campaign's objectives and goals.
    - Briefly explain the product or service being promoted.
    - Define your ideal customer with clear demographics, psychographics, and behavioral insights.
    - Understand their needs, wants, motivations, and pain points.
    - Clearly articulate the desired outcomes for the campaign.
    - Use SMART goals (Specific, Measurable, Achievable, Relevant, and Time-bound) for clarity.
    - Define key performance indicators (KPIs) to track progress and success.
    - Specify the primary and secondary goals of the campaign.
    - Examples include brand awareness, lead generation, sales growth, or website traffic.
    - Clearly define what differentiates your product or service from competitors.
    - Emphasize the value proposition and unique benefits offered to the target audience.
    - Define the desired tone and personality of the campaign messaging.
    - Identify the specific channels you will use to reach your target audience.
    - Clearly state the desired action you want the audience to take.
    - Make it specific, compelling, and easy to understand.
    - Identify and analyze your key competitors in the market.
    - Understand their strengths and weaknesses, target audience, and marketing strategies.
    - Develop a differentiation strategy to stand out from the competition.
    - Define how you will track the success of the campaign.
   -  Utilize relevant KPIs to measure performance and return on investment (ROI).
   Give proper bullet points and headlines for the marketing campaign. Do not produce any empty lines.
   Be very succinct and to the point.
    """
    config = GenerationConfig(temperature=0.8, max_output_tokens=2048)

    generate_t2t = st.button("Generate my campaign", key="generate_campaign")
    if generate_t2t and prompt:
        second_tab1, second_tab2 = st.tabs(["Campaign", "Prompt"])
        with st.spinner("Generating your marketing campaign ..."):
            with second_tab1:
                response = get_gemini_response(
                    prompt,
                    generation_config=config,
                )
                if response:
                    st.write("Your marketing campaign:")
                    st.write(response)
            with second_tab2:
                st.text(prompt)
