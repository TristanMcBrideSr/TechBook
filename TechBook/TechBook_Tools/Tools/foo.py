
from SkillsManager import ArgumentParser

argParser = ArgumentParser()

LIST_SIG = {
    "fooId": ["currentId", "newId", "section"]
}

# DICT_SIG = {
#     "barId": {"currentId": "Current user ID", "newId": "New user ID", "section": "Section to update"},
# }

def fooId(infoList: list):
    """
    Description: Update user ID in a specific section.
    """
    argParser.printArgs(__name__, locals())
    currentId, newId, section = infoList
    return f"Got list with current userId={currentId}, with new userId={newId}, section={section}"

# def barId(infoDict: dict):
#     """
#     Description: Process a dict containing userId and section.
#     """
#     currentId = infoDict.get("currentId")
#     newId = infoDict.get("newId")
#     section = infoDict.get("section")
#     return f"Got list with current userId={currentId}, with new userId={newId}, section={section}"