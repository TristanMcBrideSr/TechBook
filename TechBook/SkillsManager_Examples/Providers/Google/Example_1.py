import os
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types

from TechBook_Utils.SkillGraph import SkillGraph

load_dotenv()
graph = SkillGraph()

genClient = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def getSystemMsg() -> list:
    # System message to set the context for the model
    return [
        graph.handleTypedFormat("system", """You are a helpful assistant."""),
        ]

def getExamples() -> list:
    # Example conversations to help the model understand the context and expected responses
    return [
        graph.handleTypedFormat("user", """hello"""),
        graph.handleTypedFormat("model", """Hello there! How can I help you today?"""),
        # And so on with more examples...
        ]

def getSafetySettings(harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
    return graph.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)

def processInput(userInput: str):
    model = "gemini-2.5-flash-preview-04-17"

    # Build up system message and example conversation
    systemMsg = getSystemMsg()  # List of Parts (from graph.handleTypedFormat)
    examples = getExamples()    # List of Parts (from graph.handleTypedFormat)

    # Compose the prompt (contents)
    contents = []
    contents.extend(examples)
    # Insert the actual user input at the end
    contents.append(graph.handleTypedFormat("user", userInput)), # Append user input as a new Part

    # Safety settings
    safetySettings = getSafetySettings()  # returns a list of SafetySetting

    # Generate content config
    generateContentConfig = types.GenerateContentConfig(
        safety_settings=safetySettings,
        response_mime_type="text/plain",
        system_instruction=systemMsg,  # List of Parts
    )
    return genClient.models.generate_content(
        model=model,
        contents=contents,
        config=generateContentConfig,
    ).text  # Return the text response from the model


if __name__ == "__main__":
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")




