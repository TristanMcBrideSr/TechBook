
from datetime import datetime
from SkillsManager import ArgumentParser

parser = ArgumentParser()

def get_current_date():
    """
    Description: "Get the current date in DD-MM-YYYY format."
    Additional Information: "This function returns the current date formatted as day-month-year."
    """
    #print("Fetching the current date")
    
    parser.printArgs(__name__, locals())
    return datetime.now().strftime('%d-%B-%Y')