import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from TechBook_Utils.ToolSchemas import JsonSchemaManager

load_dotenv()
showLoadedTools = os.getenv('SHOW_LOADED_TOOLS', 'False') == 'True'
schemaType = "chat_completions"

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

def getResponse(inputMessages, toolList):
    return gptClient.chat.completions.create(
        model="gpt-4o",
        messages=inputMessages,
        tools=toolList,
        tool_choice="auto"
    )

def processInput(ctx: str) -> str:
    systemMessage = formatMessage("system", systemPrompt)
    userMessage = formatMessage("user", ctx)
    messages = [systemMessage, userMessage]

    response = getResponse(messages, tools)
    assistantMessage = response.choices[0].message

    if getattr(assistantMessage, "tool_calls", None):
        for toolCall in assistantMessage.tool_calls:
            args = json.loads(toolCall.function.arguments)
            result = toolSchemaManager.callFunction(toolCall.function.name, toolFunctions, args)

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [toolCall]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": toolCall.id,
                "content": str(result)
            })

        response2 = getResponse(messages, tools)
        return response2.choices[0].message.content
    return assistantMessage.content if assistantMessage.content else "No response generated."


if __name__ == "__main__":
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")