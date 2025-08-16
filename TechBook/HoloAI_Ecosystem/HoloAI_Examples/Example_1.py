# # Test prompts
# What is in this image? C:\Users\TechU\OneDrive\Pictures\Screenshot 2024-06-09 022121.png
# Compare these two images. Describe what is in each and highlight differences and similarities, C:\Users\TechU\OneDrive\Pictures\Screenshot 2024-06-09 022121.png, C:\Users\TechU\OneDrive\Pictures\Screenshot 2024-06-19 144830.png

from HoloAI import HoloAI
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if it exists

# DONT FIRGET TO SET YOUR API KEYS IN .env FILE FOR EACH PROVIDER YOU WANT TO USE

OPENAI    = "gpt-4.1"               # your OpenAI vision-capable model
GROG      = "meta-llama/llama-4-scout-17b-16e-instruct"  # groq vision-capable model
GOOGLE    = "gemini-2.5-flash"      # google vision-capable model
ANTHROPIC = "claude-sonnet-4-20250514"  # anthropic vision-capable model

MODEL = GROG  # Default model, can be changed to OPENAI, GOOGLE, or ANTHROPIC

class HoloEngine:
    def __init__(self):
        self.client   = HoloAI()
        self.model    = MODEL
        self.memories = []

    def currentTime(self):
        return datetime.now().strftime("%I:%M %p")

    def currentDate(self):
        return datetime.now().strftime("%B %d, %Y")

    def addMemory(self, user, response, maxTurns=10):
        self.memories.append(f"user:{user}")
        self.memories.append(f"assistant:{response}")
        if len(self.memories) > maxTurns * 2:
            self.memories = self.memories[-maxTurns*2:]

    # when you want to setup high-level instructions for the AI
    # - System: High-level description of the AI's role and capabilities
    # - Instructions: Subset of information that the AI should use to respond to the user
    def config1(self) -> str:
        currentUser = "Tristan McBride Sr."
        system = f"You are a helpful AI assistant. You are designed to assist with various tasks and provide information based on user queries. Your responses should be clear, concise, and informative. You can also analyze images and provide insights based on their content."
        instructions =  f"The current user is {currentUser} and the current date and time is {self.currentDate()} {self.currentTime()}."
        return system, instructions

    # when you want to setup basic instructions for the AI
    # - System: Description of the AI's role and capabilities and other information
    def config2(self) -> str:
        currentUser = "Tristan McBride Sr."
        system = f"You are a helpful AI assistant. The current user is {currentUser} and the current date and time is {self.currentDate()} {self.currentTime()}."
        return system

    # Complete Capabilities e.g. text, image all in one function great for chat bots, voice assistants, etc.
    def HoloCompletion(self, user: str) -> str:
        system, instructions = self.config1()
        #system = self.config2()
        msgs = self.client.formatConversation(self.memories, user)
        #msgs = user # if you want to use the user input directly without conversation history
        resp = self.client.HoloCompletion(
            model=self.model,
            system=system,
            instructions=instructions, # optional, use if you want to provide additional instructions
            input=msgs,
            #verbose=True # uncomment to see the full response structure
        )
        if resp:
            self.addMemory(user, resp)
        return resp

    # Just text completion, great for chat bots, voice assistants, etc. but no image capabilities
    def Response(self, user: str) -> str:
        system, instructions = self.config1()
        #system = self.config2()
        msgs = self.client.formatConversation(self.memories, user)
        #msgs = user # if you want to use the user input directly without conversation history
        resp = self.client.Response(
            model=self.model,
            system=system,
            instructions=instructions, # optional, use if you want to provide additional instructions
            input=msgs,
            #verbose=True # uncomment to see the full response structure
        )
        if resp:
            self.addMemory(user, resp)
        return resp

    # Just image completion, great for image analysis, comparisons, etc.
    # paths: List of image paths to analyze, e.g. ["C:/path/to/image1.png"] or ["C:/path/to/image1.png", "C:/path/to/image2.png"]
    # collect arg: Sets the number of frames to collect for video analysis, default is 5 e.g. 
    # the first frame, then every 5th frame is collected including the last frame
    def Vision(self, user: str, paths: list, collect=5) -> str:
        system, instructions = self.config1()
        #system = self.config2()
        # msgs = self.client.formatConversation(self.memories, user) # if you want to use conversation history 
        msgs = user
        
        resp = self.client.Vision(
            model=self.model,
            system=system,
            instructions=instructions, # optional, use if you want to provide additional instructions
            input=msgs,
            paths=paths,
            collect=collect 
            #verbose=True # uncomment to see the full response structure
        )
        if resp:
            self.addMemory(user, resp)
        return resp

    # def runChatSession(self):
    #     while True:
    #         prompt = input("You: ")
    #         reply = self.HoloCompletion(prompt)
    #         print(f"\nHoloAI:\n{reply}\n")

# if __name__ == "__main__":
#     HoloEngine().runChatSession()



RUN_OPTION= "HoloCompletion"  # Change to "HoloCompletion", "Response" or "Vision" as needed
IMAGE_1= r"C:\Users\TechU\OneDrive\Pictures\Screenshot 2024-06-09 022121.png" # Replace with your image path r"C:/path/to/image1.png"
IMAGE_2= r"C:\Users\TechU\OneDrive\Pictures\Screenshot 2024-06-19 144830.png" # Replace with your image path r"C:/path/to/image2.png"
IMAGE_PATHS = IMAGE_1 # or [IMAGE_1, IMAGE_2]  # List of image paths for Vision functionality



if __name__ == "__main__":
    engine = HoloEngine()
    if RUN_OPTION == "HoloCompletion":
        print("Welcome to HoloAI Chat Session!")
        try:
            while True:
                prompt = input("You: ")
                reply = engine.HoloCompletion(prompt)
                print(f"\nHoloAI:\n{reply}\n")
        except KeyboardInterrupt:
            print("\nSession ended. Goodbye!")
    elif RUN_OPTION == "Response":
        print("Welcome to HoloAI Text Response Session!")
        try:
            while True:
                prompt = input("You: ")
                reply = engine.Response(prompt)
                print(f"\nHoloAI:\n{reply}\n")
        except KeyboardInterrupt:
            print("\nSession ended. Goodbye!")

    elif RUN_OPTION == "Vision":
        print("Welcome to HoloAI Vision Session!")
        try:
            while True:
                prompt = input("You: ")
                reply = engine.Vision(prompt, IMAGE_PATHS)
                print(f"\nHoloAI:\n{reply}\n")
        except KeyboardInterrupt:
            print("\nSession ended. Goodbye!")
