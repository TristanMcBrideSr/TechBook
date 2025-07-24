
from SkillLink import SkillLink

skillLink = SkillLink()

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
    skillLink.calledActions('fooId', locals())
    currentId, newId, section = infoList
    return f"Got list with current userId={currentId}, with new userId={newId}, section={section}"

# def barId(infoDict: dict):
#     """
#     Description: Process a dict containing userId and section.
#     """
#     currentId = infoDict.get("currentId")
#     newId = infoDict.get("newId")
#     section = infoDict.get("section")
#     skillLink.calledActions('barId', locals())
#     return f"Got list with current userId={currentId}, with new userId={newId}, section={section}"