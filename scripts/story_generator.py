from dotenv import load_dotenv
import os
import openai
import re

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key =api_key

# This function reads the file line by line, and when it encounters a line starting with <, 
# it sets the current part to be the markup string (with the < and > characters stripped), 
# and initializes an empty string for that part in the parts dictionary.

# As it continues to read lines from the file, it appends each line to the current part's content string, 
# until it encounters a line starting with <\, at which point it sets the current part to None.

# The function then returns the parts dictionary, which contains the content for each part of the file, 
# indexed by the corresponding markup string.

def split_file(filename):
    markup = None
    dictionary = {}
    with open(filename,'r') as file :
        line = file.readline()
        while line != '' :
            if line.startswith('<'):
                markup = line[2:].strip()           # Set the current part as the markup string
                dictionary[markup]=''
            elif line.startswith('>'):
                dictionary[markup] += '\n'          # Handle a line starting with '>'
            else:
                dictionary[markup] += line          # Append the line to the current part's content string
            line = file.readline()
    # close the file
    file.close()
    return dictionary

# Split the file into parts using the split_file function
dictionary_parts = split_file('my_story.txt')

# Extract the parts from the dictionary
title = dictionary_parts['STORY_TITLE']
synopsis = dictionary_parts['STORY_SYNOPSIS']
characters = dictionary_parts['CHARACTERS']
requirements = dictionary_parts['STORY_REQUIREMENTS']
genre = dictionary_parts['STORY_GENRE']
setting = dictionary_parts['STORY_SETTING']
character_details = dictionary_parts['STORY_CHARACTERS']
plot = dictionary_parts['STORY_PLOT']
themes = dictionary_parts['STORY_THEMES']
tone = dictionary_parts['STORY_TONE']

# Define the prompt
prompt = (f"Title: {title}\n"
          f"Synopsis: {synopsis}\n"
          f"Characters:\n"
          f"{characters}\n"
          f"Requirements: {requirements}\n"
          f"Genre: {genre}\n"
          f"Info about story:\n"
          f"The setting: {setting}\n"
          f"The characters: {character_details}\n"
          f"The plot: {plot}\n"
          f"The themes: {themes}\n"
          f"The tone: {tone}\n"
          )

# Define the OpenAI API request parameters
model_engine = "text-davinci-003"
max_tokens = 2048
temperature = 0.5
stop = "\n"

# Define the OpenAI API request
prompt += "Build the story outlines from the factors above, then create the story chapters from the outline, write them in depth and in great details\n"
print('\n',prompt,'\n')
generated_story = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=temperature,
    stop=stop
)

# Extract the generated story from the API response
story = generated_story.choices[0].text.strip()

# Remove the part of the generated story that repeats the prompt
story = re.sub(prompt, "", story)

# Print the generated story
print(story)

# Save the generated story to a text file
with open("my_generated_story.txt", "w") as f:
    f.write(story)