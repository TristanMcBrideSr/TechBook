import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from TechBook_Utils.ToolSchemas import TypedSchemaManager

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genClient = genai.Client(api_key=apiKey)

schemaManager = TypedSchemaManager()
toolFunctions = schemaManager.getToolFunctions()
toolSchemas = schemaManager.getToolSchemas()

def getResponse(contents, tool):
    generateContentConfig = types.GenerateContentConfig(
        tools=tool,
        response_mime_type="text/plain",
    )
    return [genClient.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=contents,
        config=generateContentConfig,
    )]

def buildResponsePayload(funcName, result):
    if isinstance(result, dict):
        return result
    return {funcName: result}

def processInput(ctx: str) -> str:
    msg = schemaManager.handleFormat("user", ctx)
    messages = [msg] if not isinstance(msg, list) else msg
    while True:
        chunk = getResponse(messages, toolSchemas)[0]
        if chunk.function_calls:
            for funcCall in chunk.function_calls:
                funcName = funcCall.name
                funcArgs = funcCall.args or {}
                result = schemaManager.callFunction(funcName, toolFunctions, funcArgs)
                responsePayload = buildResponsePayload(funcName, result)
                functionResponse = types.Content(
                    role="function",
                    parts=[types.Part.from_function_response(
                        name=funcName,
                        response=responsePayload
                    )]
                )
                messages.append(functionResponse)
            continue
        if chunk.text:
            return chunk.text
        break
    return "No response from model."


if __name__ == "__main__":
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")