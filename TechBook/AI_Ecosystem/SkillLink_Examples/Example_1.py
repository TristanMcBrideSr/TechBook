import os
import logging
from dotenv import load_dotenv
from SkillLink import SkillLink

load_dotenv()
logger = logging.getLogger(__name__)

skillLink= SkillLink()
fooPath   = skillLink.getDir('Skills', 'Foo')
barPath   = skillLink.getDir('Skills', 'Bar')
toolsPath = skillLink.getDir('Tools')

fooSkills = []
barSkills = []
barTools  = []

printCapabilities = os.getenv('SHOW_CAPABILITIES', 'False') == 'True'
printMetaData     = os.getenv('SHOW_METADATA', 'False') == 'True'

# ----- Skills (Actions) -----
def loadSkills():
    skillLink.loadComponents(
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
    return skillLink.getComponents(skills, content)
    
def getBarActions():
    Skills = (
        barSkills
    )
    # return skillsmanager.getComponents(barSkills)
    return skillLink.getComponents(Skills)

def reloadSkills():
    original = getMetaData()
    skillLink.reloadSkills()
    new = getMetaData()
    for skill in new:
        if skill not in original:
            print(f"I've added the new skill {skill['className']} that {skill['description']}.\n")

def getMetaData():
    metaData = fooSkills + barSkills
    return skillLink.getMetaData(metaData, printMetaData)

def getCapabilities():
    return skillLink.getCapabilities(barSkills, printCapabilities)

def checkActions(action):
    return skillLink.checkActions(action)

def getActions(action):
    return skillLink.getActions(action)

def executeBarAction(actions, action):
    return skillLink.executeAction(actions, action)

def executeBarActions(actions, action):
    return skillLink.executeActions(actions, action)


# ----- Tools -----
def loadTools():
    skillLink.loadComponents(
        paths=[[toolsPath]],
        components=[barTools],
        reloadable=[False]
    )

def getTools():
    tools = (
        barTools
    )
    # return skillLink.getTools(barTools)
    return skillLink.getTools(tools)

def executeTool(name, tools, args, threshold=80, retry=True):
    return skillLink.executeTool(name, tools, args, threshold, retry)

def extractJson(text):
    return skillLink.extractJson(text)

def getJsonSchema(func, schemaType):
    return skillLink.getJsonSchema(func, schemaType)

def getTypedSchema(func):
    return skillLink.getTypedSchema(func)

def getJsonTools(schemaType="responses"):
        toolList = getTools()
        return skillLink.getJsonTools(toolList, schemaType)

def getTypedTools(self):
    toolList = getTools()
    return skillLink.getTypedTools(toolList)


# ----- Can be used with both skills and tools -----
def isStructured(*args):
    return skillLink.isStructured(*args)

def handleTypedFormat(role="user", content=""):
    return skillLink.handleTypedFormat(role, content)

def handleJsonFormat(role="user", content=""):
    return skillLink.handleJsonFormat(role, content)

def buildGoogleSafetySettings(harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
    return skillLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)
