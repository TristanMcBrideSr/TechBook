"""
This Example demonstrates how to use the Learning class to evaluate responses
and retrieve examples for different learning stages.
It is from one of my personal projects, where I use the SynLrn module to manage learning stages.
"""

from pathlib import Path
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

from SyncLink import SyncLink
from SynLrn import SynLrn

# from QuantumSphere.EchoMatrix.EchoMatrix import EchoMatrix
# from QuantumSphere.HoloMatrix.Evolution.Attributes.Attributes import Attributes
# from QuantumSphere.HoloMatrix.Evolution.Attributes.User.Assets.Updater.userUpdater import * 
# from QuantumSphere.HoloMatrix.Evolution.Cognition.Memory.Components.Database.Database import Database
# from QuantumSphere.HoloMatrix.Evolution.Cognition.NeuralLink.NeuralLink import NeuralLink


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)


class Learning:
    STAGES = [ 
        # Adjust stages as needed for your application this is just what I use in my personal project
        "thinking", "clarifying", "gathering",
        "defining", "refining",   "reflecting", "decision"
    ]

    def __init__(self):
        # self.attributes      = Attributes()
        # self.userIdentity    = UserIdentity()
        # self.db              = Database()
        # self.learningDir     = self.db.learningDir
        # self.neuralLink      = NeuralLink()
        # self.echoMatrix      = EchoMatrix()
        # self.getLearningLink = self.neuralLink.getLink("learningLink")
        # self.getLearningCore = self.neuralLink.getCore("learningCore")
        self.syncLink    = SyncLink()
        self.attributes  = None  # Placeholder for Attributes instance
        self.learningDir = self.getDir("Learned")
        # Example: Creating KnowledgeBase directory
        self.knowledgeBaseDir = self.getDir("KnowledgeBase")  # Top-level
        # Example: Creating nested KnowledgeBase directory
        # self.knowledgeBaseDir = self.getDir("StartDir", "NextDir", "KnowledgeBase")  # Nested
        self.dbName      = 'Learned.db'
        self.structured  = False
        # This is for demonstration purposes, adjust as needed
        self.syncLink      = SyncLink(githubRepo="TristanMcBrideSr/SkillForge", repoFolder="SkillForge/KnowledgeBase", syncDir=self.knowledgeBaseDir)
        self.syncActivated = os.getenv("ACTIVATE_KNOWLEDGE_SYNC", "False")
        if self.syncActivated:
            self.syncLink.startSync(override=False)  # Download the latest KnowledgeBase the from SkillForge if True it will override the local KnowledgeBase directory file
        import TechBook_Utils.KnowledgeBase as KnowledgeBase # Reference to the KnowledgeBase module for setting up the KnowledgeBase
        self.synLearn = SynLrn(stages=Learning.STAGES, learningDir=self.learningDir, dbName=self.dbName, fallbacks=self.fallbacks, knowledgeBase=KnowledgeBase)

        self.viewDatabase()

    def getDir(self, *paths):
        """
        Returns the absolute path to the learning directory.
        If the directory does not exist, it creates it.
        """
        return str(Path(*paths).resolve())

    def viewDatabase(self, stage: str = None):
        """
        Displays the contents of the learning database for a specific stage.
        If no stage is provided, it shows the entire database.
        """
        self.synLearn.viewDatabase(stage)

    def retrieveStage(self, ctx: str, stage: str, minScore: int = 60, fallbackCount: int = 5, structured: bool = False):
        """
        Retrieves examples from the learning database for a specific stage.
        If structured is True, it returns the results in a structured format.
        If structured is False, it returns a plain text format.
        """
        results = self.synLearn.retrieveStage(ctx, stage, minScore, fallbackCount)
        if structured:
            out = []
            for entry in results:
                ctxText, resText = self.synLearn.splitEntry(entry)
                # Handle the structured format for OpenAI and other compatible APIs or change for Google Gemini
                out.append(self._handleJsonFormat("user", ctxText))
                out.append(self._handleJsonFormat("assistant", resText))
                # out.append(self._handleTypedFormat("model", resText))
            return out
        else:
            return "\n\n".join([f"Example {i + 1}:\n{entry}" for i, entry in enumerate(results)])

    # Adjust these methods to match your learning stages
    def thinking(self, ctx: str, structured: bool = False):   return self.retrieveStage(ctx, "thinking", structured=structured)
    def clarifying(self, ctx: str, structured: bool = False): return self.retrieveStage(ctx, "clarifying", structured=structured)
    def gathering(self, ctx: str, structured: bool = False):  return self.retrieveStage(ctx, "gathering", structured=structured)
    def defining(self, ctx: str, structured: bool = False):   return self.retrieveStage(ctx, "defining", structured=structured)
    def refining(self, ctx: str, structured: bool = False):   return self.retrieveStage(ctx, "refining", structured=structured)
    def reflecting(self, ctx: str, structured: bool = False): return self.retrieveStage(ctx, "reflecting", structured=structured)
    def decision(self, ctx: str, structured: bool = False):   return self.retrieveStage(ctx, "decision", structured=structured)

    def _getShowProcess(self):
        """
        Checks if the learning process should be shown based on an environment variable.
        If the environment variable is not set, it defaults to 'False'.
        """
        load_dotenv(override=True)
        return os.getenv('SHOW_LEARNING_PROCESS', 'False') == 'True'

    def _getActivation(self, key, envVar=None):
        """
        Checks if learning is activated based on an environment variable.
        If the environment variable is not set, it defaults to checking a specific format.
        """
        load_dotenv(override=True)
        envVar = envVar or f"ACTIVATE_{key.upper()}"
        #attrActive = self.attributes.getCurrentAttribute("Self", f"{key}-Activated", "False") == "True"
        envActive = os.getenv(envVar, "False") == "True"
        return envActive #or attrActive

    def evaluate(self, ctx: str, response: str, stage: str) -> str:
        """
        Evaluates the response based on the context and stage.
        If the response is None or "None", it does not add it to the learned responses.
        If the stage is not recognized, it does nothing.
        If the response is valid, it checks if learning is activated and either prompts for human evaluation or performs self-evaluation.
        If the response is correct, it adds it to the learned responses.
        If the response is incorrect, it informs the user that it will not be added to the learned responses.
        """
        isLearningActivated = self._getActivation("Learning")
        if not response or response == "None" or response == ["None"]:
            if isLearningActivated:
                print(f"[LEARNED NOT ADDED] Stage: '{stage}' | Context: '{ctx}' | Response: '{response}'")
            return
        stage = stage.strip().lower()
        if stage not in self.STAGES:
            return
        correct = self._humanEvaluation(ctx, response, stage) if isLearningActivated else self._selfEvaluation(ctx, response, stage)
        if correct == "yes":
            self.synLearn.addToLearned(stage, ctx, response)
            if isLearningActivated:
                #self.echoMatrix.synthesize(f"I'm glad to hear my {stage} was correct, I'll add it to what I've learned.")
                print(f"I'm glad to hear my {stage} was correct, I'll add it to what I've learned.")
            return f"I'm glad to hear my {stage} was correct, I'll add it to what I've learned."
        else:
            if isLearningActivated:
                #self.echoMatrix.synthesize(f"I'm sorry my {stage} was incorrect, I will not add it to what I've learned.")
                print(f"I'm sorry my {stage} was incorrect, I will not add it to what I've learned.")
            return f"I'm sorry my {stage} was incorrect, I will not add it to what I've learned."

    def _humanEvaluation(self, ctx: str, response: str, stage: str) -> str:
        """
        Prompts the user for human evaluation of the response.
        It asks if the logic for the given stage is correct and returns the user's response.
        """
        print(f"\n[HUMAN EVALUATION] Stage: {stage.capitalize()}")
        print(f"Context:\n{ctx}\n")
        print(f"Response:\n{response}\n")
        while True:
            self.echoMatrix.synthesize(f"Was my {stage} logic correct.")
            #userInput = self.echoMatrix.recognize().strip().lower()
            userInput = input(f"Was my {stage} logic correct (Yes/No): ").strip().lower()
            if userInput in ("yes", "no"):
                return userInput
            self.echoMatrix.synthesize("Please respond with 'yes' or 'no'.")
            #print("Please respond with 'yes' or 'no'.")

    def _selfEvaluation(self, ctx: str, response, stage: str) -> str:
        """
        Performs self-evaluation of the response using a neural process (In this case, a simple OpenAI API call).
        It checks if the response is appropriate and accurate for the given context and stage.
        If the response is a list, it joins the elements into a single string.
        If the response is not a string, it converts it to a string.
        It then processes the response and returns 'yes' or 'no' based on the evaluation.
        """
        if isinstance(response, list):
            response = " ".join(str(r) for r in response if isinstance(r, str))
        # decision = self.neuralLink.runNeuralProcess("learning", self.getLearningLink, self.getLearningCore, ctx, response, stage)
        decision = self._process(ctx, response, stage)
        if self._getShowProcess():
            print(f"\n[SELF EVALUATION] Stage: {stage.capitalize()}, Decision: {decision}\n")
        return "yes" if "yes" in decision.lower() else "no"

    def _process(self, ctx: str, response, stage: str) -> str:
        """
        Processes the context and response using a neural process (OpenAI API call).
        It constructs a system message and a user message for the OpenAI API.
        The system message provides instructions for the AI assistant, and the user message contains the context and response to evaluate.
        It returns the AI's response, which is either 'yes' or 'no'.
        """
        # You can change this to any provider or model you prefer
        system = (
            "You are an AI assistant that evaluates responses based on the context provided. "
            "Your task is to determine if the response is appropriate and accurate for the given context. "
            "Answer with 'yes' or 'no'."
        )
        user = (
            f"Evaluate this response in the context of '{stage}' logic:\n\n"
            f"Context: {ctx}\n\nResponse: {response}\n\n"
            "Is the response appropriate and accurate with no errors? Answer with 'yes' or 'no'."
        )
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                self._handleJsonFormat("system", system),
                self._handleJsonFormat("user", user)
            ],
            max_tokens=10,
            temperature=0.0
        ).choices[0].message.content.strip()

    def _handleJsonFormat(self, role="user", content=""):
        """
        Handles the JSON format style for OpenAI and other compatible APIs.
        """
        return self.synLearn.handleJsonFormat(role, content)

    def _handleTypedFormat(self, role="user", content=""):
        """
        Handles the typed format style for Google Gemini and other compatible APIs.
        """
        return self.synLearn.handleTypedFormat(role, content)

    def getUserName(self, user):
        users = {
            "current": os.getenv("CURRENT_USER_NAME", "Tristan McBride Sr."),
            "previous": os.getenv("PREVIOUS_USER_NAME", "Tristan McBride Jr."),
        }
        return users.get(user, os.getenv("DEFAULT_USER_NAME", "Tristan McBride Sr"))

    def fallbacks(self, fallbackType: str) -> list:
        """
        Returns a list of fallback examples based on the specified fallback type.
        The fallbackType can be one of the learning stages like 'thinking', 'clarifying', etc.
        If the fallbackType is not recognized, it returns an empty list.
        """
        # Adjust the stages and information as needed for your application
        currentUser = self.getUserName("current")
        fallbackMap = {
            "thinking": [
                f"user:\nWhat can you do?\n\nassistant:\n{currentUser} is asking what I can do. I've got a lot of functionality, so it makes sense to just lay it out. That way they know their options and I come across as capable.",
                f"user:\nHello\n\nassistant:\n{currentUser} greeted me with hello. I could just acknowledge it or pivot to ask what they need. But honestly, a simple greeting back feels most natural. It shows I'm present without being pushy.",
                f"user:\nCan you generate digital sounds?\n\nassistant:\n{currentUser} asked if I can generate digital sounds. I don't currently have that ability, but I can create a skill to do it.",
                f"user:\nCan you create a relaxing ambient loop?\n\nassistant:\n{currentUser} asked for a relaxing ambient loop. I can't do that yet, but I could create a skill to generate ambient sound patterns.",
            ],
            "clarifying": [
                "user:\nCan you generate digital sounds?\n\nassistant:\n['creationSkill(\"create-self-skill\", \"create a skill to generate digital sounds\")']",
                "user:\nCan you create a relaxing ambient loop?\n\nassistant:\n['creationSkill(\"create-self-skill\", \"create a skill to generate relaxing ambient sound loops\")']",
                "user:\nWhat can you do?\n\nassistant:\nNone",
                "user:\nHello\n\nassistant:\nNone",
            ],
            "gathering": [],
            "defining": [],
            "refining": [],
            "reflecting": [],
            "decision": []
        }
        return fallbackMap.get(fallbackType.lower(), [])


if __name__ == "__main__":
    learning = Learning()
    # Example usage
    ctx = "Hello there how are you?"
    response = "Hello! I'm here to assist you with your queries. How can I help you today?"
    stage = "thinking"
    
    print(learning.evaluate(ctx, response, stage))
    
    
    # Retrieve examples for a specific stage
    examples = learning.thinking(ctx, structured=False)
    print(examples)   # NOT for x in examples: print(x)
