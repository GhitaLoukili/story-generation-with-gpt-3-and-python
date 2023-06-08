from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = api_key

# Function to generate an image prompt
def generate_image_prompt(prompt, output_file, prompt_title):
    with open(output_file, "a",encoding="utf-8") as f:
        generated_prompt = False
        max_retries = 5
        retry_count = 0
        
        # Retry generating prompt if it fails up to a maximum number of retries
        while not generated_prompt and retry_count < max_retries:
            # Send request to OpenAI API for completion
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                temperature=1.4,
                stop=None
            )

            # Check if response is successful and has choices
            if response and response.choices:
                image_prompt = response.choices[0].text.strip()
                f.write(f"{prompt_title}: {image_prompt}\n")        # Write the generated prompt to the output file
                generated_prompt = True
            
            else:
                print(f"Failed to generate an image prompt for {prompt_title}. Retrying...")
                retry_count += 1
        
        # If prompt generation failed even after retries, display an error message
        if not generated_prompt:
            print(f"Failed to generate an image prompt for {prompt_title}. Please try again later.")


# Load scenes
with open("scenes_division.txt", "r") as f:
    scenes = f.readlines()

# Define the output file name
output_file = "image_prompts.txt" 

with open(output_file, "w") as f:
    # Generate prompts for scenes
    for i, scene in enumerate(scenes, start=1):
        scene = scene.strip()
        prompt = f"Generate a short AI image prompt for the scene {i}: {scene}.\nProvide a brief, vivid description of an image that captures the essence of the scene, incorporating the setting, characters, and any significant details that contribute to the scene's impact in the story"
        prompt_title = f"Image prompt {i}"
        generate_image_prompt(prompt, output_file, prompt_title)

    # Generate prompts for characters
    characters = ["Fatima", "Moroccan Scholar", " Astronomer Hassan", "Doctor Aisha", "Engineer Ahmed","Fatima's Students"]
    for character in characters:
        prompt = f"Generate a short AI image prompt for the character {character} in the story. {character} plays a significant role in uncovering Morocco's scientific history. Provide a brief, vivid description of an image that captures the essence of {character}, considering their personality, expertise, and their contribution to the scientific legacy of Morocco."
        prompt_title = f"Image prompt for {character}"
        generate_image_prompt(prompt, output_file, prompt_title)
