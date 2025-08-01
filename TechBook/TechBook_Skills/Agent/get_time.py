
from datetime import datetime
from SkillLink import SkillLink

skillLink = SkillLink()

def get_current_time():
    """
    Description: "Get the current time in HH:MM format."
    Additional Information: "This function returns the current time formatted as hour:minute."
    """
    skillLink.calledActions(__name__, locals())
    return datetime.now().strftime('%H:%M')
