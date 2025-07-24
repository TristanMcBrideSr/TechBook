import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from TechBook_Utils.SkillGraph import SkillGraph

load_dotenv()
graph = SkillGraph()

systemPrompt = "You are a helpful assistant that can call functions to get information."
gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def getSystemMsg() -> list:
    # System message to set the context for the model
    return [
        graph.handleJsonFormat("system", """You are a helpful assistant."""),
        ]

def getExamples() -> list:
    # Example conversations to help the model understand the context and expected responses
    return [
        graph.handleJsonFormat("user", """hello"""),
        graph.handleJsonFormat("model", """Hello there! How can I help you today?"""),
        # And so on with more examples...
        ]


def processInput(ctx: str) -> str:
    systemMsg = getSystemMsg()  # List of Parts (from graph.handleJsonFormat)
    examples = getExamples()    # List of Parts (from graph.handleJsonFormat)
    messages = []
    messages.extend(systemMsg)
    messages.extend(examples)
    messages.append(graph.handleJsonFormat("user", ctx))  # Append user input as a new Part
    return gptClient.chat.completions.create(
        model="gpt-4o",
        messages=messages
    ).choices[0].message.content # Return the text response from the model


if __name__ == "__main__":
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")