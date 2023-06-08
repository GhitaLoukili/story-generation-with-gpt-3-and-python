from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key =api_key


# Read the story from the file
with open("my_generated_story.txt", 'r') as file:
    story = file.read()

# Define the input prompt
prompt = f"""
Analyze the story provided and divide it into 20 distinct scenes. Each scene should represent a significant event, change in location, or key moment in the story's progression. Consider the pacing, narrative structure, and character development when determining the scene breaks. Provide a detailled descrition of each scene:
{story}
you should provide exactly 20 scenes no less
"""

# Call the OpenAI API to generate the scene division
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=prompt,
    max_tokens=2048,
    temperature=0.8,
    n=1,
    stop=None
)

# Extract the generated scene division from the API response
scene_division = response.choices[0].text.strip()

# Split the scene division into separate scenes
scenes = scene_division.split("\n")

# Write the scenes to a new file
with open("scenes_division.txt", 'w') as output_file:
    for i, scene in enumerate(scenes):
        output_file.write(scene)
        output_file.write("\n")
