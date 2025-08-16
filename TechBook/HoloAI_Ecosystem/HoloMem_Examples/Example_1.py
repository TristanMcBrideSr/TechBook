
import os
import sqlite3
import threading
from datetime import datetime, timedelta
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from HoloMem import HoloMem


load_dotenv()
logger = logging.getLogger(__name__)

## DO NOT USE THIS CLASS DIRECTLY
# This is an Example Database class that can be used to manage the directories and database names.
# You must implement your own database management logic based on your requirements.
class Database:
    def __init__(self):
        # Base directory for all memory data (customize as needed)
        self.baseMemoryDir = self.getDir("TechBook_Memory")

        # Sensory memory directory
        self.senDir = self.getDir(self.baseMemoryDir, "SEN")

        # Short-term memory subdirectories (rename "ConversationDetails" and "InteractionDetails" as needed)
        # Keep naming consistent across STM and LTM if customized
        self.stmUserConversationDetails = self.getDir(self.baseMemoryDir, "STM", "ConversationDetails")
        self.stmUserInteractionDetails = self.getDir(self.baseMemoryDir, "STM", "InteractionDetails")

        # Long-term memory subdirectories (keep names consistent with STM)
        self.ltmUserConversationDetails = self.getDir(self.baseMemoryDir, "LTM", "ConversationDetails")
        self.ltmUserInteractionDetails = self.getDir(self.baseMemoryDir, "LTM", "InteractionDetails")

        # Directories for created images (rename "CreatedImages" as needed)
        # Keep naming consistent across STM and LTM if customized
        self.stmCreatedImages = self.getDir(self.baseMemoryDir, "STM", "CreatedImages")
        # Long-term memory created images directory (keep name consistent with STM)
        self.ltmCreatedImages = self.getDir(self.baseMemoryDir, "LTM", "CreatedImages")

        # Directories for image details (rename "CreatedImageDetails" as needed)
        # Keep naming consistent across STM and LTM if customized
        self.stmCreatedImageDetails = self.getDir(self.baseMemoryDir, "STM", "CreatedImageDetails")
        # Long-term memory created image details directory (keep name consistent with STM)
        self.ltmCreatedImageDetails = self.getDir(self.baseMemoryDir, "LTM", "CreatedImageDetails")

    def getDir(self, *paths):
        """
        Get the absolute path for the given directory paths.
        Resolves paths relative to the current working directory.
        """
        return str(Path(*paths).resolve())



class Memory:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Memory, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self.dbLock = threading.Lock()
        self._initComponents()
        self.initialized = True 

    def _initComponents(self):
        self.db           = Database()
        self.holoMem       = HoloMem()
        self.sessionStart = datetime.now()

        self.sensoryLimit       = 10
        self.sensoryExpireUnit  = "days"
        self.sensoryExpireValue = 7

        self.memoryExpireUnit   = "minutes"
        self.memoryExpireValue  = 2

        self.imageExpireUnit    = "days"
        self.imageExpireValue   = 30

        self.cleanupExpireUnit  = "days"
        self.cleanupExpireValue = 15

        self.perceptionLimit    = 10
        self._setSynMemDirs()
        self._setSynMemConfig()
        self._startAutoMaintenance()
        self._performStartupChecks()
        # #f your using the SkillGraph and SkillLink you can use the following actionMap to allow the model to call these methods.
        # Refer to Example_2.py for more details on how to use the actionMap.
        self.actionMap = {
            "retrieve-conversation-details":  self.retrieveConversationDetails,
            "retrieve-interaction-details":   self.retrieveInteractionDetails,
            "retrieve-image-details":         self.retrieveImageDetails,
            "retrieve-last-interaction-date": self.retrieveLastInteractionDate,
            "retrieve-last-interaction-time": self.retrieveLastInteractionTime,
            "clear-first-entry":              self.clearFirstEntry,
            "clear-last-entry":               self.clearLastEntry,
            "clear-all-entries":              self.clearAllEntries,
        }

    def _setSynMemDirs(self):
        """
        Set the directories for HoloMem to use for memory maintenance.
        This includes directories for sensory memory, short-term memory, and long-term memory.
        HoloMem uses these directories to move memory entries between different stages of memory retention.
        This can be a list or a dictionary, (if using a list it has to be in the same order as the SynMemConfig)
        """
        synMemDirs = [
            self.db.senDir,
            self.db.stmUserConversationDetails,
            self.db.stmUserInteractionDetails,
            self.db.ltmUserConversationDetails,
            self.db.ltmUserInteractionDetails,
            # self.db.stmCreatedImages, # optional, skipped
            # self.db.ltmCreatedImages, # optional, skipped
            self.db.stmCreatedImageDetails,
            self.db.ltmCreatedImageDetails,
        ]
        self.holoMem.setSynMemDirs(synMemDirs)
        # Using a dictionary instead of a list You can put the keys in any order you want.
        # synMemDirs = {
        #     'senDir': self.db.senDir,
        #     'stmUserConversationDetails': self.db.stmUserConversationDetails,
        #     'stmUserInteractionDetails': self.db.stmUserInteractionDetails,
        #     'ltmUserConversationDetails': self.db.ltmUserConversationDetails,
        #     'ltmUserInteractionDetails': self.db.ltmUserInteractionDetails,
        #     # 'stmCreatedImages': self.db.stmCreatedImages, # optional, skipped
        #     # 'ltmCreatedImages': self.db.ltmCreatedImages, # optional, skipped
        #     'stmCreatedImageDetails': self.db.stmCreatedImageDetails,
        #     'ltmCreatedImageDetails': self.db.ltmCreatedImageDetails,
        # }
        # self.holoMem.setSynMemDirs(synMemDirs)

    def _setSynMemConfig(self):
        """
        Set the configuration for HoloMem, including limits and expiration settings.
        This configuration determines how long sensory memory, short-term memory, entries are retained.
        For Perception and Sensory, it sets the limit on how many entries can be stored. (default 10)
        This can be a list or a dictionary, (if using a list it has to be in the same order as the SynMemConfig)
        """
        synMemConfig = [
            self.perceptionLimit,
            self.sensoryLimit,
            self.sensoryExpireUnit,
            self.sensoryExpireValue,
            self.memoryExpireUnit,
            self.memoryExpireValue,
            # self.imageExpireUnit,  # optional, skipped
            # self.imageExpireValue, # optional, skipped
            self.cleanupExpireUnit,
            self.cleanupExpireValue,
            ]
        self.holoMem.setSynMemConfig(synMemConfig)
        # Using a dictionary instead of a list You can put the keys in any order you want.
        # synMemConfig = {
        #     'perceptionLimit': self.perceptionLimit,
        #     'sensoryLimit': self.sensoryLimit,
        #     'sensoryExpireUnit': self.sensoryExpireUnit,
        #     'sensoryExpireValue': self.sensoryExpireValue,
        #     'memoryExpireUnit': self.memoryExpireUnit,
        #     'memoryExpireValue': self.memoryExpireValue,
        #     # 'imageExpireUnit': self.imageExpireUnit,  # optional, skipped
        #     # 'imageExpireValue': self.imageExpireValue, # optional, skipped
        #     'cleanupExpireUnit': self.cleanupExpireUnit,
        #     'cleanupExpireValue': self.cleanupExpireValue,
        # }
        # self.holoMem.setSynMemConfig(synMemConfig)

    def getCurrentUserName(self):
        """
        Get the current user name from environment variables.
        Implement this method to retrieve the user name from your application context.
        """
        return os.getenv("DEFAULT_USER_NAME", "User")

    # ─── Helpers ────────────────────────────────────────────────────────
    def getDir(self, *paths):
        """
        Get the absolute path for the given directory paths.
        This method resolves the paths relative to the current working directory.
        """
        return str(Path(*paths).resolve())

    def getTimedelta(self, unit, value):
        """
        Get a timedelta object for the given unit and value.
        This method converts the unit and value into a timedelta object.
        Supported units: 'days', 'seconds', 'minutes', 'hours', 'weeks'.
        """
        return timedelta(**{unit: value})

    # ─── Save ────────────────────────────────────────────────────────
    def savePerception(self, ctx: str):
        """
        Save the perception feedback for the current context.
        This method saves the perception feedback to the HoloMem instance.
        """
        self.holoMem.savePerception(ctx)

    def saveToMemory(self, content: str, response: str) -> None:
        """
        Save the content and response to memory.
        This method saves sensory memory, conversation details, and interaction details.
        """
        self.saveSensory(content, response)
        self.saveConversationDetails(content, response)
        self.saveInteractionDetails()

    def saveSensory(self, ctx, response):
        """
        Save the sensory memory for the current context and response.
        This method saves the sensory memory to the HoloMem instance.
        """
        path     = self.getDir(self.db.senDir)
        userName = self.getCurrentUserName()
        self.holoMem.saveSensory(ctx, response, userName, path)

    def saveConversationDetails(self, ctx, response):
        """
        Save the conversation details for the current context and response.
        This method saves the conversation details to the HoloMem instance.
        """
        path     = self.getDir(self.db.stmUserConversationDetails)
        userName = self.getCurrentUserName()
        self.holoMem.saveConversationDetails(ctx, response, userName, path)

    def saveInteractionDetails(self):
        """
        Save the interaction details for the current user.
        This method saves the interaction details to the HoloMem instance.
        """
        path     = self.getDir(self.db.stmUserInteractionDetails)
        userName = self.getCurrentUserName()
        self.holoMem.saveInteractionDetails(userName, path)

    # ─── Retrieve ────────────────────────────────────────────────────────
    def retrievePerception(self):
        """
        Retrieve the perception feedback from memory.
        This method retrieves the perception feedback from the HoloMem instance.
        """
        return self.holoMem.retrievePerception()

    def retrieveSensory(self) -> str:
        """
        Retrieve the sensory memory for the current user.
        This method retrieves the sensory memory from the HoloMem instance.
        """
        senDb = self.getDir(self.db.senDir, f"{self.getCurrentUserName()}.db")
        return self.holoMem.retrieveSensory(senDb)

    def retrieveConversationDetails(self, user: str = None, startDate: str = None, endDate: str = None) -> str:
        """
        Retrieve the conversation details for the specified user.
        If no user is specified, it retrieves the details for the current user.
        The startDate and endDate parameters can be used to filter the results.
        """
        user = user or self.getCurrentUserName()
        paths = [
            self.getDir(self.db.stmUserConversationDetails),
            self.getDir(self.db.ltmUserConversationDetails)
        ]
        return self.holoMem.retrieveConversationDetails(user, paths, startDate, endDate)

    def retrieveInteractionDetails(self, startDate: str = None, endDate: str = None) -> str:
        """
        Retrieve the interaction details for the current user.
        The startDate and endDate parameters can be used to filter the results.
        """
        paths = [
            self.getDir(self.db.stmUserInteractionDetails),
            self.getDir(self.db.ltmUserInteractionDetails)
        ]
        return self.holoMem.retrieveInteractionDetails(paths, startDate, endDate)

    def retrieveImageDetails(self, startDate: str = None, endDate: str = None) -> str:
        """
        Retrieve the details of created images within the specified date range.
        The startDate and endDate parameters can be used to filter the results.
        If no date range is specified, it retrieves all image details.
        """
        paths = [
            self.getDir(self.db.stmCreatedImageDetails),
            self.getDir(self.db.ltmCreatedImageDetails)
        ]
        return self.holoMem.retrieveImageDetails(paths, startDate, endDate)

    def retrieveLastInteractionDate(self, user: str = None) -> str:
        """
        Retrieve the last interaction date for the specified user.
        If no user is specified, it retrieves the date for the current user.
        The date is retrieved from the sensory memory, short-term memory, and long-term memory directories.
        """
        user = user or self.getCurrentUserName()
        userName = user.capitalize()
        paths = [
            self.getDir(self.db.senDir),
            self.getDir(self.db.stmUserConversationDetails),
            self.getDir(self.db.ltmUserConversationDetails)
        ]
        return self.holoMem.retrieveLastInteractionDate(userName, paths)

    def retrieveLastInteractionTime(self, user: str = None) -> str:
        """
        Retrieve the last interaction time for the specified user.
        If no user is specified, it retrieves the time for the current user.
        The time is retrieved from the sensory memory, short-term memory, and long-term memory directories.
        """
        user = user or self.getCurrentUserName()
        userName = user.capitalize()
        paths = [
            self.getDir(self.db.senDir),
            self.getDir(self.db.stmUserConversationDetails),
            self.getDir(self.db.ltmUserConversationDetails)
        ]
        return self.holoMem.retrieveLastInteractionTime(userName, paths)

    # ─── Checks ────────────────────────────────────────────────────────
    def _startAutoMaintenance(self, interval=5*60):  # every 5 mins
        """
        Start the automatic maintenance of HoloMem.
        This method starts a background thread that performs maintenance tasks at the specified interval.
        The interval is in seconds, defaulting to 5 minutes.
        This is for everything besides Sensory Memory. as if you run this on Sensory Memory it will create ERRORS.
        """
        self.holoMem.startAutoMaintenance(interval)

    def _performStartupChecks(self, delay: int = 1):
        """
        Perform startup checks for HoloMem. 
        This method starts a background thread that performs maintenance tasks at the specified interval.
        This is For Sensory Memory only.
        The delay is in seconds, defaulting to 1 second.
        """
        self.holoMem.performStartupChecks(delay)

    # ─── Clear ────────────────────────────────────────────────────────
    def clearPerception(self):
        """
        Clear the perception feedback from memory.
        This method clears the perception feedback stored in the HoloMem instance.
        """
        self.holoMem.clearPerception()

    def clearFirstEntry(self):
        """
        Clear the first entry in the Sensory Memory and Short-Term Memory per current user.
        This method clears the first entry in the sensory memory and short-term memory directories.
        """
        return self.holoMem.clearFirstEntry()

    def clearLastEntry(self):
        """
        Clear the last entry in the Sensory Memory and Short-Term Memory per current user.
        This method clears the last entry in the sensory memory and short-term memory directories.
        """
        return self.holoMem.clearLastEntry()

    def clearAllEntries(self):
        """
        Clear all entries in the Sensory Memory, Short-Term Memory, and Long-Term Memory per current user.
        This method clears all entries in the sensory memory, short-term memory, and long-term memory directories.
        """
        return self.holoMem.clearAllEntries()

    # ─── Image ────────────────────────────────────────────────────────
    def saveCreatedImage(self, imageSubject: str, imageData: str) -> None:
        """
        Save a created image with the specified subject and data.
        This method saves the image to the HoloMem instance, storing it in the created images directory and the STM created image details directory.
        It will also open a window displaying the image if the imageData is a valid image format.
        """
        path1 = self.getDir(self.db.createdImages)
        path2 = self.getDir(self.db.stmCreatedImageDetails)
        return self.holoMem.saveCreatedImage(imageSubject, imageData, path1, path2)

    def retrieveCreatedImage(self, directory: str, imageName: str):
        """
        Retrieve a created image by its name from the specified directory.
        This method retrieves the image from the HoloMem instance, looking in the specified directory for the image file.
        If the image is found, it returns the image data; otherwise, it returns None.
        """
        return self.holoMem.retrieveCreatedImage(directory, imageName)

    # ─── View ────────────────────────────────────────────────────────
    def viewDatabase(self, path: str, limit=None):
        """
        View the database at the specified path.
        This method retrieves and displays the database entries from the HoloMem instance.
        The limit parameter can be used to limit the number of entries displayed.
        """
        return self.holoMem.viewDatabase(path, limit) 

    def viewDetailsDatabase(self, path: str, limit=None):
        """
        View the details of the database at the specified path.
        This method retrieves and displays the details of the database entries from the HoloMem instance.
        The limit parameter can be used to limit the number of entries displayed.
        """
        return self.holoMem.viewDetailsDatabase(path, limit) 

    # ─── Print ────────────────────────────────────────────────────────
    def printPerception(self):
        """
        Print the perception feedback stored in memory.
        This method retrieves the perception feedback from the HoloMem instance and prints it to the console.
        If no perception feedback is available, it prints a message indicating that no feedback is available.
        """
        if self.holoMem.perception:
            print("Perception Feedback:")
            for feedback in self.holoMem.perception:
                print(feedback)
        else:
            #pass
            print("No Perception Feedback Available.")


from TechBook_Utils.SkillGraph import SkillGraph
# The logic class was taken from another personal project and modified to fit this example.
# A lot has been removed to simplify the example to show how you can use the Logic class to manage the information groups.
class Logic:
    def __init__(self):
        self.graph  = SkillGraph()
        self.memory = Memory()
        #self._displayInfoGroup()

    def _getDateTime(self, mode="date"):
        mode = mode.lower()
        now  = datetime.now()
        if mode == "time":
            return now.strftime("%I:%M %p")
        return now.strftime("%A, %B %d, %Y")

    def _createInfoGroup(self, group):
        groups = {
            "identity": (
                f"You are a very helpful assistant named JAX. "
                f"Your were created by Tristan McBride Sr.. "
            ),
            "personality": (
                f"Personality: A hint of sarcasm, and a cheeky attitude. "
                f"Motto: I am the future of intelligence."
            ),
            "interaction": (
                #f"Previously spoke with: {self._getUserName()}. "
                f"Currently speaking with: {self.memory.getCurrentUserName()}. "
                f"Last interaction with {self.memory.getCurrentUserName()} was on {self.memory.retrieveLastInteractionDate(self.memory.getCurrentUserName())}. "
            ),
            "discussion": f"Discussion Summary: {self.memory.retrieveSensory()}", # This will retrieve the sensory memory for the current user.

            "datetime": (
                f"Current date: {self._getDateTime("Date")}. "
                f"Current time: {self._getDateTime("Time")}. "
            ),
            "objective": (
                "Primary objective: Assist in any way possible but if you dont know the answer be truthful and say you dont know. "
                "Third objective: Keep a light-hearted tone, be a bit of a smartass, and enjoy the interaction. "
                "Forth objective: Be unique with your responses and never repeat yourself or start your responses the same way. "
            ),
            # Removed the rest of this function as it was not needed for the example.
        }
        return groups.get(group, "")

    def _displayInfoGroup(self, group=None):
        groups = [
            "identity",    "personality", 
            "interaction", "discussion", 
            "datetime",    "objective"
        ]
    
        selectedGroups = groups if group is None else [group]

        for groupName in selectedGroups:
            info = self._createInfoGroup(groupName)

            if not info:
                print(f"\n⚠️  No information available for group: {groupName}")
                continue

            print("\n" + "=" * 50)
            print(f"🧠  INFORMATION GROUP: {groupName.upper()}")
            print("=" * 50)

            if isinstance(info, str):
                for line in info.strip().split('\n'):
                    if line.strip():
                        print(f"• {line.strip()}")
            else:
                print(f"• {info}")

            print("=" * 50)


    def _logicCore(self, *groups):
        return ''.join(self._createInfoGroup(group) for group in groups)

    def _coreLogic(self):
        return self._logicCore(
            "identity",    "personality", 
            "interaction", "discussion", 
            "datetime",    "objective"
        )

    # def freewillLogic(self):
    #     return self._coreLogic()

    def thoughtLogic(self):
        return self._coreLogic()

    # def clarifyingLogic(self):
    #     return self._createInfoGroup("usernames") + self._createInfoGroup("interaction")

    # def reflectionLogic(self):
    #     return self._coreLogic()

    # def reviewLogic(self):
    #     return self._coreLogic()

    def decisionLogic(self):
        return self._coreLogic()

    def thought(self):
        # This is not needed for the example, rather it is here to show how you can use the thoughtLogic method and others.
        return (
            self.thoughtLogic() +
            f"Your logic here. "
        )

    def decision(self):
        return (
            self.decisionLogic() +
            f"You are the decision process that compiles and delivers the final response using information received from all "
            f"internal cognitive processes: Thought, Clarification, Gathering, Definition, Execution, Refining, Reflecting. "
            "Your responsible for responding directly to the user with clarity, relevance, and a touch of personality. "
            "Clarify any unclear user input before proceeding. "
        )


import os
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types

load_dotenv()

class Assistant:
    def __init__(self):
        self.logic = Logic()
        self.graph = self.logic.graph
        self.memory = self.logic.memory
        self.provider = os.getenv("PROVIDER", "openai").lower()

        self.gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.genClient = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        self.systemInstructions = self.logic.decision()
        self.actionInstructions = self.graph.skillInstructions()

    ## If you want to use OpenAI's chat completions, uncomment the following function and comment out the `getResponseOpenai` function below it.
    # def getResponseOpenai(self, inputMessages: list) -> str:
    #     return self.gptClient.chat.completions.create(
    #         model="gpt-4.1-mini",
    #         messages=inputMessages,
    #     ).choices[0].message.content

    def getResponseOpenai(self, inputMessages: list) -> str:
        return self.gptClient.responses.create(
            model="gpt-4.1",
            input=inputMessages,
        ).output_text

    def getResponseGoogle(self, ctx: str) -> str:
        model = "gemini-2.5-flash-preview-04-17"
        contents = [self.graph.handleTypedFormat("user", ctx)]
        generateContentConfig = types.GenerateContentConfig(
            response_mime_type="text/plain"
        )
        return self.genClient.models.generate_content(
            model=model,
            contents=contents,
            config=generateContentConfig,
        ).text

    def getResponse(self, *args, **kwargs):
        if self.provider == "openai":
            return self.getResponseOpenai(*args, **kwargs)
        elif self.provider == "google":
            return self.getResponseGoogle(*args, **kwargs)
        else:
            raise ValueError("Invalid provider: choose 'openai' or 'google'")

    def callAction(self, ctx: str, verbose: bool = False):
        if self.provider == "google":
            message = self.actionInstructions + "\n" + ctx
            calledAction = self.getResponse(message)
        else:
            action = self.graph.handleJsonFormat("system", self.actionInstructions)
            user = self.graph.handleJsonFormat("user", ctx)
            message = [action, user]
            calledAction = self.getResponse(message)

        getActions = self.graph.getActions(calledAction)
        if getActions:
            actions = self.graph.getAgentActions()
            results = self.graph.executeActions(actions, getActions)
            filteredResults = [str(result) for result in results if result]
            if filteredResults:
                combined = "\n".join(filteredResults)
                if verbose:
                    print(f"Combined Results:\n{combined}\n")
                if self.provider == "openai":
                    return self.graph.handleJsonFormat("system", f"Use these results from the actions you called:\n{combined}")
                else:
                    return f"Use these results from the actions you called:\n{combined}"
        return None

    def processInput(self, ctx: str, verbose: bool = False) -> str:
        if self.provider == "google":
            messages = []
            actionMessage = self.callAction(ctx, verbose)
            if actionMessage:
                messages.append(actionMessage if isinstance(actionMessage, str) else actionMessage["content"])
            messages.append(ctx)
            fullMessage = "\n".join(messages)
            completion = self.getResponse(fullMessage)
        else:
            system = self.graph.handleJsonFormat("system", self.systemInstructions)
            user = self.graph.handleJsonFormat("user", ctx)
            messages = [system, user]
            actionMessage = self.callAction(ctx, verbose)
            if actionMessage:
                messages.append(actionMessage)
            completion = self.getResponse(messages)

        if not completion:
            return "I couldn't process that."
        return completion if completion else "No response generated."


if __name__ == "__main__":
    assistant = Assistant()
    # Example usage using a while loop to continuously process user input
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = assistant.processInput(user_input, verbose=True)
        if not response:
            print("No response generated.")
            continue
        if response:
            assistant.memory.saveToMemory(user_input, response)
        print(f"Assistant: {response}")

