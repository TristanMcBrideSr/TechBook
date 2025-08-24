

import os
import threading
import logging
from dotenv import load_dotenv

## Note: HoloLink and HoloSync are the new names for SkillLink and SyncLink respectively.
# from SkillLink import SkillLink, SyncLink
from HoloLink import HoloLink as SkillLink
from HoloSync import HoloSync as SyncLink

load_dotenv()

logger = logging.getLogger(__name__)

# Set These Environment Variables in your .env file or system environment variables
# SHOW_CAPABILITIES=True (optional, to show capabilities at startup)
# SHOW_METADATA=True (optional, to show metadata at startup)
# SHOW_CALLED_ACTIONS=True (optional, to show called actions during execution)


class SkillGraph:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SkillGraph, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.skillLink     = SkillLink() # Can pass in autoReload=True and cycleInterval=60 to automatically reload skills when they change.
        # Set your base directories. Is equivalent to r"C:\path\to\TechBook_Skills" on Windows or "/path/to/TechBook_Skills" on Linux/Mac.
        self.syncLink      = SyncLink(githubRepo="TristanMcBrideSr/SkillForge", repoFolder="SkillForge/Forge", syncDir=self.db.forgedSkillsDir)
        self.baseSkillsDir = self.getDir('TechBook_Skills')
        self.baseToolsDir  = self.getDir('TechBook_Tools')
        self.showSkills    = os.getenv('SHOW_SKILLS', 'False') == 'True'
        self.showTools     = os.getenv('SHOW_TOOLS', 'False') == 'True'
        self.schemaType    = os.getenv('SCHEMA_TYPE', 'chat_completions').lower()  # Default to 'chat_completions' if not set
        self.showMetaData  = os.getenv('SHOW_METADATA', 'False') == 'True'
        self.syncActivated = os.getenv("ACTIVATE_SKILL_SYNC", "False")
        if self.syncActivated:
            # self.skillList=["research"] # List the skills you want to sync from SkillForge
            self.syncLink.startSync() #(syncList=self.skillList, override=False)  # Download the latest skills from SkillForge changing the override parameter to True will overwrite existing skills
        self.skillComponents()
        self.toolComponents()
        self.showSkillsAndTools()  # Load skills and tools at startup if configured to do so.

    def showSkillsAndTools(self):
        if self.showSkills:
            self.getAgentCapabilities()  # Load agent capabilities after skills to ensure they are available for use.
        if self.showMetaData:
            self.getMetaData() # Load metadata after skills to ensure it is available for use.
        if self.showTools and self.schemaType == 'chat_completions':
            self.getTools()
        if self.showTools and self.schemaType == 'responses':
            self.getTools()  # Load tools after skills to ensure they are available for use.
        if self.showTools and self.schemaType == 'typed':
            self.getTools()

    def getDir(self, *paths):
        return self.skillLink.getDir(*paths)

    def setAutoReload(self, autoReload: bool = True, cycleInterval: int = 60) -> None:
        """
        Set whether to automatically reload skills when they change.
        This is useful for development and testing purposes.
        By default SkillLink auto reload is set to False with a cycle interval of 60 seconds you can change this 
        by passing autoReload=True to enable or a different cycleInterval in seconds.
        Only necessary when letting the agent create new skills or when you want to refresh the skills during runtime.
        """
        self.skillLink.setAutoReload(autoReload, cycleInterval)

    # If you rather not separate the skills into dynamic, static and restricted components, you can skip the following methods and make 
    # it simpler by using just using 1 method to load all skills.
    # See below for different options for loading skills and tools.
    def skillComponents(self):
        """
        Load dynamic components for user and self skills.
        Dynamic components are those that can be reloaded or changed during runtime.
        """
        self.userSkills = [] # If not using user setup, you can skip this.
        self.agentSkills = []
        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User')], # If not using user setup, you can skip this. Refer to the Example_3.py for more details on how to use the user skills.
                [self.getDir(self.baseSkillsDir, 'Agent')]
            ],
            components=[
                self.userSkills, # If not using user setup, you can skip this.
                self.agentSkills
            ],
            reloadable=[
                False, # If not using user setup, you can skip this.
                False # This is for dynamic skills, so set to True if you want to reload them.
            ]
        )

    def toolComponents(self):
        """
        Load custom tools for the self agent.
        These tools are not part of the dynamic, static and restricted skills.
        """
        self.agentTools = []
        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseToolsDir, 'Tools')]
            ],
            components=[
                self.agentTools
            ],
            reloadable=[
                False
            ]
        )

    def getUserActions(self, content):
        """
        Get user actions based on the provided content.
        This method combines dynamic, static, and restricted user skills to return the available actions.
        Use only if you want to get user actions based on the content provided.
        """
        # If you are not using user skills, you can skip this method. Refer to the Example_3.py for more details on how to use the user skills.
        skills = (
            self.userSkills
        )
        return self.skillLink.getComponents(skills, content)

    def getAgentActions(self):
        """
        Get self actions based on the available skills.
        This method combines dynamic, static, and restricted self skills to return the available actions.
        """
        skills = (
            self.agentSkills
        )
        return self.skillLink.getComponents(skills)

    def reloadSkills(self):
        """ 
        Reload all skills and print any new skills added.
        Only necessary when letting the agent create new skills or when you want to refresh the skills during runtime.
        """
        original = self.getMetaData()
        self.skillLink.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} That {skill['description']}.\n")

    def getMetaData(self):
        """Get metadata for all skills."""
        metaData = (
                self.userSkills + self.agentSkills + self.agentTools
        )
        return self.skillLink.getMetaData(metaData, self.showMetaData)


    # ----- Skills -----
    def getAgentCapabilities(self):
        """
        Get capabilities of the self agent based on its skills.
        This method combines dynamic, static, and restricted self skills to return the available capabilities.
        """
        description = False
        capabitites = (
            self.agentSkills
        )
        return self.skillLink.getCapabilities(capabitites, self.showSkills, description)

    def checkActions(self, action: str) -> str:
        """
        Check if the given action is available in the self agent's skills.
        If the action is not found, it will return an error message.
        """
        return self.skillLink.checkActions(action)

    def getActions(self, action: str) -> list:
        """
        Get actions available for the self agent based on the given action string.
        If the action is not found, it will return an empty list.
        """
        return self.skillLink.getActions(action)

    def executeAction(self, actions, action):
        """
        Execute a single action from the self agent's skills.
        If the action is not found, it will return an error message.
        You must do your own for loop to iterate through the actions.
        """
        return self.skillLink.executeAction(actions, action)

    def executeActions(self, actions, action):
        """
        Execute multiple actions from the self agent's skills.
        If the action is not found, it will return an error message.

        The for loop is done for you to iterate through the actions.
        """
        return self.skillLink.executeActions(actions, action)

    def skillInstructions(self):
        """
        Get action instructions for the self agent based on its capabilities.
        This method returns a string that describes how the self agent can perform actions.
        """
        # # If you want to provide your own examples, you can uncomment the following line and provide your own examples.
        # return self.skillLink.skillInstructions(self.getAgentCapabilities(), self.skillExamples())

        # # This will automatically generate instructions based on the capabilities and your naming conventions.
        # return self.skillLink.skillInstructions(self.getAvaCapabilities())
        return self.skillLink.skillInstructions(self.getAgentCapabilities())

    def skillExamples(self):
        """
        Get examples of how to use skills from your naming conventions.
        This should be customized to match your skill naming conventions.
        """
        return (
            "Single Action Examples:\n" # Don't change this line
            "- ['getDate()']\n" # Change to match your skill naming conventions
            "- ['getTime()']\n" # Change to match your skill naming conventions
            "- ['getDate()', 'getTime()']\n"
            "Skill With Sub-Action Examples:\n" # Don't change this line
            "- ['appSkill(\"open\", \"Notepad\")']\n" # Change to match your skill naming conventions
            "- ['appSkill(\"open\", \"Notepad\")', 'appSkill(\"open\", \"Word\")']\n"
            "- ['weatherSkill(\"get-weather\", \"47.6588\", \"-117.4260\")']\n" # Change to match your skill naming conventions
        )



    # ----- Tools -----
    def executeTool(self, name, tools, args, threshold=80, retry=True):
        """
        Execute a tool with the given name, tools, and arguments.
        If the tool is not found, it will return an error message.
        If the tool execution fails, it will retry based on the retry parameter.
        """
        return self.skillLink.executeTool(name, tools, args, threshold, retry)

    def getTools(self):
        """
        Get all tools available for the self agent.
        """
        
        tools = (
            self.agentTools
        )
        return self.skillLink.getTools(tools, self.showTools, self.schemaType)

    def extractJson(self, text):
        """
        Extract the first JSON array or object from a string, even if wrapped in markdown or extra commentary.
        """
        return self.skillLink.extractJson(text)

    def getJsonSchema(self, func, schemaType):
        """
        Build a json schema for a function based on its signature and docstring metadata.
        The schemaType can be either 'completions' or 'responses'.
        Compatible with the OpenAI API and similar services that use JSON schemas.
        Returns a dictionary representing the schema.
        """
        return self.skillLink.getJsonSchema(func, schemaType)

    def getTypedSchema(self, func):
        """
        Build a typed schema for a function based on its signature and docstring metadata.
        Compatible with the Google API.
        Returns a dictionary representing the schema.
        """
        return self.skillLink.getTypedSchema(func)

    def getJsonTools(self, schemaType="responses"):
        """
        Get all tools available for the agent in a JSON schema format.
        This method retrieves the tools and converts them to a format compatible with OpenAI APIs.
        The schemaType can be either 'chat_completions' or 'responses'.
        Returns a dictionary representing the tools in JSON schema format.
        """
        toolList = self.getTools()
        return self.holoLink.getJsonTools(toolList, schemaType)

    def getTypedTools(self):
        """
        Get all tools available for the agent in a typed format.
        This method retrieves the tools and converts them to a format compatible with Google GenAI APIs.
        Returns a dictionary representing the tools in typed format.
        """
        toolList = self.getTools()  # {name: function}
        return self.holoLink.getTypedTools(toolList)


    # ----- Can be used with both skills and tools -----
    def isStructured(self, *args):
        """
        Check if any of the arguments is a list of dictionaries.
        This indicates structured input (multi-message format).
        """
        return self.skillLink.isStructured(*args)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        """
        Format content for Google GenAI APIs.
        """
        return self.skillLink.handleTypedFormat(role, content)

    def handleJsonFormat(self, role: str = "user", content: str = ""):
        """
        Format content for OpenAI APIs and similar JSON-based APIs.
        """
        return self.skillLink.handleJsonFormat(role, content)

    def formatTypedExamples(self, items):
        """
        Handle roles for Google GenAI APIs, converting items to Gemini Content/Part types.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleTypedFormat
            - dict: wrapped as Content with role, value as text
            - list of dicts: each dict converted to Content with role, dict as text
        Returns a flat list of Content objects.
        """
        return self.skillLink.formatTypedExamples(items)

    def formatJsonExamples(self, items):
        """
        Handle roles for OpenAI APIs, converting items to JSON message format.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleJsonFormat
            - dict: added as-is
            - list of dicts: each dict is added individually
        Returns a flat list of message dicts.
        """
        return self.skillLink.formatJsonExamples(items)

    def formatExamples(self, items, formatFunc):
        """
        Ultra-robust handler for message formatting.
        Accepts string, dict, list of any mix, any nested depth.
        Silently ignores None. Converts numbers and bools to strings.
        """
        return self.skillLink.formatExamples(items, formatFunc)

    def handleTypedExamples(self, items):
        """
        Handle roles for Google GenAI APIs, converting items to Gemini Content/Part types.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleTypedFormat
            - dict: wrapped as Content with role, value as text
            - list of dicts: each dict converted to Content with role, dict as text
        Returns a flat list of Content objects.
        """
        return self.skillLink.handleTypedExamples(items)

    def handleJsonExamples(self, items):
        """
        Handle roles for OpenAI APIs, converting items to JSON message format.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleJsonFormat
            - dict: added as-is
            - list of dicts: each dict is added individually
        Returns a flat list of message dicts.
        """
        return self.skillLink.handleJsonExamples(items)

    def handleExamples(self, items, formatFunc):
        """
        Ultra-robust handler for message formatting.
        Accepts string, dict, list of any mix, any nested depth.
        Silently ignores None. Converts numbers and bools to strings.
        """
        return self.skillLink.handleExamples(items, formatFunc)

    def buildGoogleSafetySettings(self, harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
        """
        Construct a list of Google GenAI SafetySetting objects.
        """
        return self.skillLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)


    # ----- Loading Skills and Tools -----
    # Below shows multiple options for loading skills and tools from multiple directories.
    # Option 1: Separate methods for loading dynamic, static, and restricted components
    def dynamicComponents(self):
        """
        Load dynamic components for user and self skills.
        Dynamic components are those that can be reloaded or changed during runtime.
        """
        self.dynamicUserSkills = [] # If not using user setup, you can skip this.
        self.dynamicAgentSkills = []
        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User', 'Created'), self.getDir(self.baseSkillsDir, 'User', 'Dynamic')], # If not using user setup, you can skip this.
                [self.getDir(self.baseSkillsDir, 'Agent', 'Created'), self.getDir(self.baseSkillsDir, 'Agent', 'Dynamic')]
            ],
            components=[
                self.dynamicUserSkills, # If not using user setup, you can skip this.
                self.dynamicAgentSkills
            ],
            reloadable=[
                True, # If not using user setup, you can skip this.
                True
            ]
        )

    def staticComponents(self):
        """
        Load static components for user and self skills.
        """
        self.staticUserSkills = [] # If not using user setup, you can skip this.
        self.staticAgentSkills = []
        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User', 'Static')], # If not using user setup, you can skip this.
                [self.getDir(self.baseSkillsDir, 'Agent', 'Static')]
            ],
            components=[
                self.staticUserSkills, # If not using user setup, you can skip this.
                self.staticAgentSkills
            ],
            reloadable=[
                False, # If not using user setup, you can skip this.
                False
            ]
        )

    def restrictedComponents(self):
        """
        Load restricted components for user and self skills.
        """
        self.restrictedUserSkills = [] # If not using user setup, you can skip this.
        self.restrictedAgentSkills = []
        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User', 'Restricted')], # If not using user setup, you can skip this.
                [self.getDir(self.baseSkillsDir, 'Agent', 'Restricted')]
            ],
            components=[
                self.restrictedUserSkills, # If not using user setup, you can skip this.
                self.restrictedAgentSkills
            ],
            reloadable=[
                False, # If not using user setup, you can skip this.
                False
            ]
        )

    # Option 2: Single method for loading all skills
    def loadAllComponents(self):
        """
        Load dynamic, static, and restricted components simplified into a single method,
        and excluding user skills if not needed.
        No advanced logic.
        """
        self.dynamicAgentSkills = []
        self.skillLink.loadComponents(
            paths=[[
                self.getDir(self.baseSkillsDir, 'Agent', 'Created'), 
                self.getDir(self.baseSkillsDir, 'Agent', 'Dynamic')]
            ],
            components=[self.dynamicAgentSkills],
            reloadable=[True]
        )

        self.staticAgentSkills = []
        self.skillLink.loadComponents(
            paths=[[self.getDir(self.baseSkillsDir, 'Agent', 'Static')]],
            components=[self.staticAgentSkills],
            reloadable=[False]
        )

        self.restrictedAgentSkills = []
        self.skillLink.loadComponents(
            paths=[[self.getDir(self.baseSkillsDir, 'Agent', 'Restricted')]],
            components=[self.restrictedAgentSkills],
            reloadable=[False]
        )

        self.agentTools = []
        self.skillLink.loadComponents(
            paths=[[self.getDir(self.baseToolsDir, 'Tools')]],
            components=[self.agentTools],
            reloadable=[False]
        )

    # Option 3: For advanced users, you can customize the loading of skills and tools
    def loadAllomponents(self):
        """
        Load dynamic, static, and restricted Agent components.
        """
        COMPONENTS = {
            'dynamic': {
                'attr': 'dynamicAgentSkills',
                'paths': [self.getDir(self.baseSkillsDir, 'Agent', 'Created'), self.getDir(self.baseSkillsDir, 'Agent', 'Dynamic')],
                'reloadable': True
            },
            'static': {
                'attr': 'staticAgentSkills',
                'paths': [self.getDir(self.baseSkillsDir, 'Agent', 'Static')],
                'reloadable': False
            },
            'restricted': {
                'attr': 'restrictedAgentSkills',
                'paths': [self.getDir(self.baseSkillsDir, 'Agent', 'Restricted')],
                'reloadable': False
            },
            'tools': {
                'attr': 'agentTools',
                'paths': [self.getDir(self.baseToolsDir, 'Tools')],
                'reloadable': False
            }
        }

        for key, opts in COMPONENTS.items():
            setattr(self, opts['attr'], [])
            self.skillLink.loadComponents(
                paths=[opts['paths']],
                components=[getattr(self, opts['attr'])],
                reloadable=[opts['reloadable']]
            )

