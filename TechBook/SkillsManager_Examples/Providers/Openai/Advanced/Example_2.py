import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from TechBook_Utils.ToolSchemas import JsonSchemaManager

load_dotenv()
showLoadedTools = os.getenv('SHOW_LOADED_TOOLS', 'False') == 'True'
schemaType = "responses"

toolSchemaManager = JsonSchemaManager()
toolFunctions = toolSchemaManager.getToolFunctions()
tools = [toolSchemaManager.buildToolSchema(f, schemaType) for f in toolFunctions.values()]
systemPrompt = "You are a helpful assistant that can call functions to get information."
gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# No longer needed as its handled by the SkillGraph
# if showLoadedTools:
#     print(f"Discovered tools: {list(toolFunctions.keys())}")
#     schemaJson = json.dumps(tools, indent=2)
#     schemaJson = re.sub(
#         r'("description": ")(.*?)(\")',
#         lambda m: m.group(1) + m.group(2).replace('\\n', '\n\t\t') + m.group(3),
#         schemaJson,
#         flags=re.DOTALL
#     )
#     print(f"Tools schema: {schemaJson}")

def formatMessage(role, content):
    return toolSchemaManager.handleFormat(role, content)

def getResponse(inputMessages: list, toolList):
    return gptClient.responses.create(
        model="gpt-4.1",
        input=inputMessages,
        tools=toolList,
    )

def processInput(ctx: str) -> str:
    systemMessage = formatMessage("system", systemPrompt)
    userMessage = formatMessage("user", ctx)
    messages = [systemMessage, userMessage]

    response = getResponse(messages, tools)
    functionCalls = []
    functionOutputs = []

    for toolCall in response.output:
        if toolCall.type != "function_call":
            continue

        functionCalls.append({
            "type": "function_call",
            "call_id": toolCall.call_id,
            "name": toolCall.name,
            "arguments": toolCall.arguments
        })

        name = toolCall.name
        args = json.loads(toolCall.arguments)
        result = toolSchemaManager.callFunction(name, toolFunctions, args)

        functionOutputs.append({
            "type": "function_call_output",
            "call_id": toolCall.call_id,
            "output": str(result)
        })

    messages.extend(functionCalls)
    messages.extend(functionOutputs)
    response2 = getResponse(messages, tools)
    return response2.output_text.strip()


if __name__ == "__main__":
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")g