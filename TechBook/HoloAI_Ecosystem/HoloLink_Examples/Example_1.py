import os
import logging
from dotenv import load_dotenv
from HoloLink import HoloLink

load_dotenv()
logger = logging.getLogger(__name__)

holoLink= HoloLink()
fooPath   = holoLink.getDir('Skills', 'Foo')
barPath   = holoLink.getDir('Skills', 'Bar')
toolsPath = holoLink.getDir('Tools')

fooSkills = []
barSkills = []
barTools  = []

printCapabilities = os.getenv('SHOW_CAPABILITIES', 'False') == 'True'
printMetaData     = os.getenv('SHOW_METADATA', 'False') == 'True'

# ----- Skills (Actions) -----
def loadSkills():
    holoLink.loadComponents(
        paths=[
            [fooPath],
            [barPath]
        ],
        components=[
            fooSkills,
            barSkills
        ],
        reloadable=[
            True,
            False
        ]
    )

def getFooActions(content):
    skills = (
            fooSkills
    )
    # return skillsmanager.getComponents(fooSkills, content)
    return holoLink.getComponents(skills, content)
    
def getBarActions():
    Skills = (
        barSkills
    )
    # return skillsmanager.getComponents(barSkills)
    return holoLink.getComponents(Skills)

def reloadSkills():
    original = getMetaData()
    holoLink.reloadSkills()
    new = getMetaData()
    for skill in new:
        if skill not in original:
            print(f"I've added the new skill {skill['className']} that {skill['description']}.\n")

def getMetaData():
    metaData = fooSkills + barSkills
    return holoLink.getMetaData(metaData, printMetaData)

def getCapabilities():
    return holoLink.getCapabilities(barSkills, printCapabilities)

def checkActions(action):
    return holoLink.checkActions(action)

def getActions(action):
    return holoLink.getActions(action)

def executeBarAction(actions, action):
    return holoLink.executeAction(actions, action)

def executeBarActions(actions, action):
    return holoLink.executeActions(actions, action)


# ----- Tools -----
def loadTools():
    holoLink.loadComponents(
        paths=[[toolsPath]],
        components=[barTools],
        reloadable=[False]
    )

def getTools():
    tools = (
        barTools
    )
    # return holoLink.getTools(barTools)
    return holoLink.getTools(tools)

def executeTool(name, tools, args, threshold=80, retry=True):
    return holoLink.executeTool(name, tools, args, threshold, retry)

def extractJson(text):
    return holoLink.extractJson(text)

def getJsonSchema(func, schemaType):
    return holoLink.getJsonSchema(func, schemaType)

def getTypedSchema(func):
    return holoLink.getTypedSchema(func)

def getJsonTools(schemaType="responses"):
        toolList = getTools()
        return holoLink.getJsonTools(toolList, schemaType)

def getTypedTools(self):
    toolList = getTools()
    return holoLink.getTypedTools(toolList)


# ----- Can be used with both skills and tools -----
def isStructured(*args):
    return holoLink.isStructured(*args)

def handleTypedFormat(role="user", content=""):
    return holoLink.handleTypedFormat(role, content)

def handleJsonFormat(role="user", content=""):
    return holoLink.handleJsonFormat(role, content)

def buildGoogleSafetySettings(harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
    return holoLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)
