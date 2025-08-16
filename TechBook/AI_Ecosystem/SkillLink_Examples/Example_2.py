
import os
import logging
import threading
from dotenv import load_dotenv
from SkillLink import SkillLink

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ClassName: # This is a placeholder for the class name, replace with your actual class name
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ClassName, cls).__new__(cls) # Remember to replace ClassName with your actual class name
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self.skillLink= SkillLink()
        self.fooPath   = self.getDir('Skills', 'Foo')
        self.barPath   = self.getDir('Skills', 'Bar')
        self.toolsPath = self.getDir('Tools')
        self.fooSkills = []
        self.barSkills = []
        self.barTools  = []
        self.showSkills   = os.getenv('SHOW_SKILLS', 'False') == 'True'
        self.showMetaData = os.getenv('SHOW_METADATA', 'False') == 'True'
        self.loadSkills()
        self.loadTools()
        self.initialized = True

    def getDir(self, *paths):
        return self.skillLink.getDir(*paths)

    # ----- Skills (Actions) -----
    def loadSkills(self):
        self.skillLink.loadComponents(
            paths=[
                [self.fooPath],
                [self.barPath]
            ],
            components=[
                self.fooSkills,
                self.barSkills
            ],
            reloadable=[
                True,
                False
            ]
        )

    def getFooActions(self, content):
        skills = (
            self.fooSkills
        )
        # return self.skillLink.getComponents(self.fooSkills, content)
        return self.skillLink.getComponents(skills, content)

    def getBarActions(self):
        skills = (
            self.barSkills
        )
        # return self.skillLink.getComponents(self.barSkills)
        return self.skillLink.getComponents(skills)

    def reloadSkills(self):
        original = self.getMetaData()
        self.skillLink.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} that {skill['description']}.\n")

    def getMetaData(self):
        metaData = (
            self.fooSkills + self.barSkills
        )
        return self.skillLink.getMetaData(metaData, self.showMetaData)

    def getCapabilities(self):
        return self.skillLink.getCapabilities(self.barSkills, self.showSkills)

    def checkActions(self, action: str):
        return self.skillLink.checkActions(action)

    def getActions(self, action: str):
        return self.skillLink.getActions(action)

    def executeBarAction(self, actions, action):
        return self.skillLink.executeAction(actions, action)

    def executeBarActions(self, actions, action):
        return self.skillLink.executeActions(actions, action)


    # ----- Tools -----
    def loadTools(self):
        self.skillLink.loadComponents(
            paths=[[self.toolsPath]],
            components=[self.barTools],
            reloadable=[False]
        )

    def getTools(self):
        tools = (
            self.barTools
        )
        # return self.skillLink.getTools(self.barTools)
        return self.skillLink.getTools(tools)

    def executeTool(self, name, tools, args, threshold=80, retry=True):
        return self.skillLink.executeTool(name, tools, args, threshold, retry)

    def extractJson(self, text):
        return self.skillLink.extractJson(text)

    def getJsonSchema(self, func, schemaType):
        return self.skillLink.getJsonSchema(func, schemaType)

    def getTypedSchema(self, func):
        return self.skillLink.getTypedSchema(func)

    def getJsonTools(self, schemaType="responses"):
        toolList = self.getTools()
        return self.skillLink.getJsonTools(toolList, schemaType)

    def getTypedTools(self):
        toolList = self.getTools()
        return self.skillLink.getTypedTools(toolList)


    # ----- Can be used with both skills and tools -----
    def isStructured(self, *args):
        return self.skillLink.isStructured(*args)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        return self.skillLink.handleTypedFormat(role, content)


    def handleJsonFormat(self, role: str = "user", content: str = ""):
        return self.skillLink.handleJsonFormat(role, content)

    def buildGoogleSafetySettings(self, harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
        return self.skillLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)