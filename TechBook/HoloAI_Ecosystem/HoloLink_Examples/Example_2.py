
import os
import logging
import threading
from dotenv import load_dotenv
from HoloLink import HoloLink

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
        self.holoLink = HoloLink()
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
        return self.holoLink.getDir(*paths)

    # ----- Skills (Actions) -----
    def loadSkills(self):
        self.holoLink.loadComponents(
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
        # return self.holoLink.getComponents(self.fooSkills, content)
        return self.holoLink.getComponents(skills, content)

    def getBarActions(self):
        skills = (
            self.barSkills
        )
        # return self.holoLink.getComponents(self.barSkills)
        return self.holoLink.getComponents(skills)

    def reloadSkills(self):
        original = self.getMetaData()
        self.holoLink.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} that {skill['description']}.\n")

    def getMetaData(self):
        metaData = (
            self.fooSkills + self.barSkills
        )
        return self.holoLink.getMetaData(metaData, self.showMetaData)

    def getCapabilities(self):
        return self.holoLink.getCapabilities(self.barSkills, self.showSkills)

    def checkActions(self, action: str):
        return self.holoLink.checkActions(action)

    def getActions(self, action: str):
        return self.holoLink.getActions(action)

    def executeBarAction(self, actions, action):
        return self.holoLink.executeAction(actions, action)

    def executeBarActions(self, actions, action):
        return self.holoLink.executeActions(actions, action)


    # ----- Tools -----
    def loadTools(self):
        self.holoLink.loadComponents(
            paths=[[self.toolsPath]],
            components=[self.barTools],
            reloadable=[False]
        )

    def getTools(self):
        tools = (
            self.barTools
        )
        # return self.holoLink.getTools(self.barTools)
        return self.holoLink.getTools(tools)

    def executeTool(self, name, tools, args, threshold=80, retry=True):
        return self.holoLink.executeTool(name, tools, args, threshold, retry)

    def extractJson(self, text):
        return self.holoLink.extractJson(text)

    def getJsonSchema(self, func, schemaType):
        return self.holoLink.getJsonSchema(func, schemaType)

    def getTypedSchema(self, func):
        return self.holoLink.getTypedSchema(func)

    def getJsonTools(self, schemaType="responses"):
        toolList = self.getTools()
        return self.holoLink.getJsonTools(toolList, schemaType)

    def getTypedTools(self):
        toolList = self.getTools()
        return self.holoLink.getTypedTools(toolList)


    # ----- Can be used with both skills and tools -----
    def isStructured(self, *args):
        return self.holoLink.isStructured(*args)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        return self.holoLink.handleTypedFormat(role, content)


    def handleJsonFormat(self, role: str = "user", content: str = ""):
        return self.holoLink.handleJsonFormat(role, content)

    def buildGoogleSafetySettings(self, harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
        return self.holoLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)