import os
from dotenv import load_dotenv
from openai import OpenAI
from TechBook_Utils.SkillGraph import SkillGraph

load_dotenv()
graph = SkillGraph()
systemPrompt = "You are a helpful assistant."

gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def getUnstructuedSystemMsg() -> list:
    return systemPrompt

def getUnstructuedExamples() -> str:
    return "\n".join([
        "user:\nhello",
        "assistant:\nHello there! How can I help you today?",
        # Add more example pairs as needed...
    ])

def getStructuedSystemMsg() -> list:
    return [
        graph.handleJsonFormat("system", systemPrompt),
    ]

def getStructuedExamples() -> list:
    return [
        graph.handleJsonFormat("user", "hello"),
        graph.handleJsonFormat("assistant", "Hello there! How can I help you today?"),
        # Add more example pairs as needed...
    ]

def isStructured(*args):
    return graph.isStructured(*args)

def handleJsonExamples(items):
    return graph.handleJsonExamples(items)

def handleExamples(items, formatFunc):
    return graph.handleExamples(items, formatFunc)

def unstructuredInput(client, model, system, user, extra=None):
    print("Using unstructured input processing...")
    logic = system
    if extra:
        logic += extra
    return client.responses.create(model=model, instructions=logic, input=user)

def structureInput(client, model, system, user, extra=None):
    print("Using structured input processing...")
    logic = []
    # Using the add function to process roles
    # def add(role, value):
    #     if isinstance(value, str):
    #         #print(f"Converted {role} string to dict.")
    #         logic.append(graph.handleJsonFormat(role, value))
    #     elif isinstance(value, dict):
    #         #print(f"Added {role} dict as-is.")
    #         logic.append(value)
    #     elif isinstance(value, list) and all(isinstance(i, dict) for i in value):
    #         #print(f"Added {role} list of dicts as-is.")
    #         logic.extend(value)
    #     elif value is not None:
    #         #print(f"ERROR: {role} was not a string, dict, or list of dicts.")
    #         raise ValueError(f"{role.title()} must be a string, dict, or a list of dicts.")

    # add("system",    system)
    # add("assistant", extra)
    # add("user",      user)

    # Using the new handleJsonExamples function to process roles
    logic.extend(handleJsonExamples([
        ("system", system), 
        ("assistant", extra), 
        ("user", user)]
    ))

    # Using the new handleExamples for structured input
    # logic.extend(handleRoles([
    #     ("system", system),
    #     ("assistant", extra),
    #     ("user", user)], 
    #     graph.handleJsonFormat
    # ))

    #print("Final logic list:", logic)
    return client.responses.create(model=model, input=logic)

def processInput(user_input):
    model  = "gpt-4o"  # Specify the model you want to use
    # Using unstructured input
    # system = getUnstructuedSystemMsg()  # Get the system message for unstructured input
    # extra  = getUnstructuedExamples()  # Get the examples for unstructured input
    # Using structured input
    system = getStructuedSystemMsg()  # Get the system message for structured input
    extra  = getStructuedExamples()  # Get the examples for structured input
    try:
        getStructured = isStructured(system, user_input, extra)
        print(f"Context Type: {getStructured}")
        inputMap = {
            True:  lambda: structureInput(gptClient, model, system, user_input, extra),
            False: lambda: unstructuredInput(gptClient, model, system, user_input, extra)
        }
        return inputMap[getStructured]().output_text
    except Exception as e:
        print(f"Error processing input: {e}")
        return f"Neural Context Error Occurred: {e}"


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = processInput(user_input)
        print(f"Assistant: {response}")
