import os
from dotenv import load_dotenv
from openai import OpenAI
from TechBook_Utils.SkillGraph import SkillGraph

load_dotenv()
graph = SkillGraph()
systemPrompt = "You are a helpful assistant."

gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def getSystemMsg() -> list:
    return [
        graph.handleJsonFormat("system", systemPrompt),
    ]

def getExamples() -> list:
    return [
        graph.handleJsonFormat("user", "hello"),
        graph.handleJsonFormat("assistant", "Hello there! How can I help you today?"),
        # Add more example pairs as needed...
    ]

def processInput(ctx: str) -> str:
    systemMsg = getSystemMsg()
    examples = getExamples()
    messages = []
    messages.extend(systemMsg)
    messages.extend(examples)
    messages.append(graph.handleJsonFormat("user", ctx))
    return gptClient.responses.create(
        model="gpt-4o",
        input=messages
    ).output_text

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")
