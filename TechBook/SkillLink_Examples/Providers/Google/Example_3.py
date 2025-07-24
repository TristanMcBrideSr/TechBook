
import os
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types

from TechBook_Utils.SkillGraph import SkillGraph

load_dotenv()
graph = SkillGraph()

genClient = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

systemPrompt = "You are a helpful assistant."

def getSystemMsg() -> list:
    # System message to set the context for the model
    return [
        graph.handleTypedFormat("system", systemPrompt),
        ]

def getUnstructuedExamples() -> str:
    return "\n".join([
        "user:\nhello",
        "model:\nHello there! How can I help you today?",
        # Add more example pairs as needed...
    ])

def getSturcturedExamples() -> list:
    # Example conversations to help the model understand the context and expected responses
    return [
        graph.handleTypedFormat("user", """hello"""),
        graph.handleTypedFormat("model", """Hello there! How can I help you today?"""),
        # And so on with more examples...
        ]

def getSafetySettings(harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
    return graph.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)

def handleTypedRoles(items):
    return graph.handleTypedRoles(items)

def handleRoles(items, formatFunc):
    return graph.handleRoles(items, formatFunc)

def processInput(userInput: str):
    model = "gemini-2.5-flash-preview-04-17"

    # Build up system message and example conversation
    systemMsg = getSystemMsg()  # List of Parts (from graph.handleTypedFormat)
    # examples = getSturcturedExamples()    # List of Parts (from graph.handleTypedFormat)
    examples = getUnstructuedExamples()

    # Compose the prompt (contents) normally
    contents = []
    # contents.extend(examples)
    # # Insert the actual user input at the end
    # contents.append(graph.handleTypedFormat("user", userInput)), # Append user input as a new Part

    # Using the new handleTypedRoles function to process roles
    contents.extend(handleTypedRoles([
        ("model", examples),
        ("user", userInput)]
    ))

    # Using the new handleRoles for structured input
    # contents.extend(handleRoles([
    #     ("model", examples),
    #     ("user", userInput)], 
    #     graph.handleTypedFormat
    # ))

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