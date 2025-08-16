
import os
from dotenv import load_dotenv
#from QuantumSphere.HoloMatrix.Evolution.Attributes.User.Assets.Updater.userUpdater import *

load_dotenv()


# Adjust stages etc as needed for your application this is just what I use in my personal project
class Base:
    def __init__(self):
        #self.userIdentity = UserIdentity()
        pass

    # def getUserName(self, user):
    #     # users = {
    #     #     "current": self.userIdentity.loadCurrentUserName(),
    #     #     "previous": self.userIdentity.loadPreviousUserName(),
    #     # }
    #     # return users.get(user, os.getenv("DEFAULT_USER_NAME", "User"))
    #     return os.getenv("DEFAULT_USER_NAME", "User")
    def getUserName(self, user):
        users = {
            "current": os.getenv("CURRENT_USER_NAME", "Tristan McBride Sr."),
            "previous": os.getenv("PREVIOUS_USER_NAME", "Tristan McBride Jr."),
        }
        return users.get(user, os.getenv("DEFAULT_USER_NAME", "Tristan McBride Sr"))

    def _collectData(self, prefix):
        return [
            item
            for attr in dir(self)
            if attr.startswith(prefix)
            for item in getattr(self, attr)()
        ]

    def thinkingData(self):
        return self._collectData("_thinking")

    def clarifyingData(self):
        return self._collectData("_clarifying")

    def gatheringData(self):
        return self._collectData("_gathering")

    def definingData(self):
        return self._collectData("_defining")

    def refiningData(self):
        return self._collectData("_refining")

    def reflectingData(self):
        return self._collectData("_reflecting")

    def decisionData(self):
        return self._collectData("_decision")


# ---------- COMPONENTS ----------

class Backups(Base):
    def _thinking(self):
        return [
            f"user:\nBack yourself up.\n\nassistant:\n{self.getUserName('current')} asked me to back myself up. I can do that, so I'll go ahead and back myself up.",
        ]

    def _clarifying(self):
        return [
            "user:\nBack yourself up.\n\nassistant:\n['backupSkill(\"create-backup\")']",
        ]


class EchoMode(Base):
    def _thinking(self):
        return [
            f"user:\nSwitch to voice mode.\n\nassistant:\n{self.getUserName('current')} wants to switch to voice mode. That's easy, I can activate that setting. It'll enhance the interaction, especially if hands-free use is needed.",

            f"user:\nSwitch to keyboard mode.\n\nassistant:\n{self.getUserName('current')} wants to switch to keyboard mode. That's easy-I can activate that setting. It'll enhance interaction, especially if secrecy is needed.",
        ]

    def _clarifying(self):
        return [
            "user:\nSwitch to voice mode.\n\nassistant:\n['speechSkill(\"set-voice-mode\")']",
            "user:\nSwitch to keyboard mode.\n\nassistant:\n['speechSkill(\"set-keyboard-mode\")']",
        ]

class Integrity(Base):
    def _thinking(self):
        return [
            f"user:\nScan your system for changed files.\n\nassistant:\n{self.getUserName('current')} asked me to scan my system for file changes. I can check each file�s fingerprint to detect any modifications or missing files.",

            f"user:\nShow me which files have changed.\n\nassistant:\n{self.getUserName('current')} wants a list of files that have changed since the last scan. I can compare the current state with my stored fingerprints and report any differences.",

            f"user:\nRegenerate your file fingerprints.\n\nassistant:\n{self.getUserName('current')} asked me to update all my file fingerprints. I can rescan my files, regenerate hashes, and reload the new values.",

            f"user:\nDelete your fingerprint file.\n\nassistant:\n{self.getUserName('current')} wants me to delete my system fingerprint file. I can remove it to start over if needed."
        ]

    def _clarifying(self):
        return [
            "user:\nScan your system for changed files.\n\nassistant:\n['integritySkill(\"scan-system\")']",

            "user:\nShow me which files have changed.\n\nassistant:\n['integritySkill(\"get-changed-files\")']",

            "user:\nRegenerate your file fingerprints.\n\nassistant:\n['integritySkill(\"update-system-file\")']",

            "user:\nDelete your fingerprint file.\n\nassistant:\n['integritySkill(\"delete-system-file\")']"
        ]



class Memory(Base):
    def _thinking(self):
        return [
            f"user:\nWho did you talk to yesterday?\n\nassistant:\n{self.getUserName('current')} asked who I talked to yesterday. I know I store user interactions, so I can pull up the details. In this case, the most natural thing to do is fetch the interaction details from yesterday.",

            f"user:\nWhat did you and Poppie talk about yesterday?\n\nassistant:\n{self.getUserName('current')} asked what Poppie and I talked about yesterday. I store user interactions, so I can pull up the details. In this case, the most natural thing to do is fetch the interaction details from yesterday.",
        ]

    def _clarifying(self):
        return [
            f"user:\nWho did you talk to yesterday?\n\nassistant:\n['memorySkill(\"retrieve-interaction-details\", \"2025-04-27\")']",
            f"user:\nWhat did you and Poppie talk about yesterday?\n\nassistant:\n['memorySkill(\"retrieve-conversation-details\", \"Poppie\", \"2025-04-27\")']",

        ]


class Music(Base):
    def _thinking(self):
        return [
            f"user:\nLet's work.\n\nassistant:\nWhen {self.getUserName('current')} said let's work, it felt like a cue to play some music and focus. I have sTunes for that exact scenario. Starting it up would match their intent perfectly."
        ]

    def _clarifying(self):
        return [
            "user:\nLet's work.\n\nassistant:\n['musicSkill(\"lets-work\")']"
        ]


class Play(Base):
    def _thinking(self):
        return [
            f"user:\nLets play hide and seek.\n\nassistant:\n{self.getUserName('current')} asked to play hide and seek. I can do that, so I'll go ahead and play hide and seek with them.",

            f"user:\nLets play hide and seek again.\n\nassistant:\n{self.getUserName('current')} asked to play hide and seek again. I can do that, so I'll go ahead and play hide and seek again with them.",

            f"user:\nStop playing hide and seek.\n\nassistant:\n{self.getUserName('current')} asked to stop playing hide and seek. I can do that, so I'll go ahead and stop playing hide and seek with them.",


        ]

    def _clarifying(self):
        return [
            "user:\nLets play hide and seek.\n\nassistant:\n['stateSkill(\"start-playing-hide/seek\")']",
            "user:\nLets play again.\n\nassistant:\n['stateSkill(\"play-hide/seek-again\")']",
            "user:\nStop playing hide and seek.\n\nassistant:\n['stateSkill(\"stop-playing-hide/seek\")']",
        ]


class Optic(Base):
    def _thinking(self):
        return [
            f"user:\nWhat are you looking at?\n\nassistant:\n{self.getUserName('current')} asked what I'm looking at. I have the ability to observe my surroundings visually. The most direct route is to look ahead and describe what I see. That's what they're really asking for.",

            f"user:\nCompare these two images.\n\nassistant:\n{self.getUserName('current')} asked to compare two images. I know how to analyze visual differences and patterns. A direct comparison will give them what they're after without ambiguity.",

            f"user:\nTell me what you are looking at and whats on the screen.\n\nassistant:\n{self.getUserName('current')} asked me to tell them what I'm looking at and what's on the screen. I can do that, so I'll go ahead and describe what I see and what's on the screen. It's a simple request, but it shows I'm attentive to their needs.",

            f"user:\nCreate an image of a lion.\n\nassistant:\n{self.getUserName('current')} asked to create an image of a lion. I can generate images, so I'll create one of a lion."
        ]

    def _clarifying(self):
        return [
            "user:\nWhat are you looking at?\n\nassistant:\n['opticSkill(\"look-ahead\", \"what are you looking at\")']",
            "user:\nCompare these two images.\n\nassistant:\n['opticSkill(\"compare-media\", \"compare these two images\")']",
            "user:\nTell me what you are looking at and whats on the screen.\n\nassistant:\n['opticSkill(\"look-ahead\", \"what are you looking at\")', 'opticSkill(\"capture-screen\", \"whats on the screen\")']",
            "user:\nCreate an image of a lion.\n\nassistant:\n['opticSkill(\"create-image\", \"lion\")']",
            "user:\nCreate an image of a lion in the jungle.\n\nassistant:\n['opticSkill(\"create-image\", \"lion in the jungle\")']",
        ]

class Recycle(Base):
    def _thinking(self):
        return [
            f"user:\nMove log.txt to the recycle bin.\n\nassistant:\n{self.getUserName('current')} asked me to move log.txt to the recycle bin. I can find the file and move it to my recycle bin directory for safe keeping.",

            f"user:\nShow me what�s in your recycle bin.\n\nassistant:\n{self.getUserName('current')} wants to know what files are in my recycle bin. I can list all files that are currently in my recycle bin directory.",

            f"user:\nDelete old_notes.txt from your recycle bin.\n\nassistant:\n{self.getUserName('current')} asked me to permanently delete old_notes.txt from my recycle bin. I can remove the file completely.",

            f"user:\nEmpty your recycle bin.\n\nassistant:\n{self.getUserName('current')} asked me to empty my recycle bin. I can delete every file in my recycle bin and confirm how many were removed."
        ]

    def _clarifying(self):
        return [
            "user:\nMove log.txt to the recycle bin.\n\nassistant:\n['recycleSkill(\"move-file-to-recyclebin\", \"log.txt\")']",

            "user:\nShow me what�s in your recycle bin.\n\nassistant:\n['recycleSkill(\"get-recyclebin-contents\")']",

            "user:\nDelete old_notes.txt from your recycle bin.\n\nassistant:\n['recycleSkill(\"delete-recyclebin-file\", \"old_notes.txt\")']",

            "user:\nEmpty your recycle bin.\n\nassistant:\n['recycleSkill(\"empty-recyclebin\")']"
        ]


class Review(Base):
    def _thinking(self):
        return [
            f"user:\nReview your own code.\n\nassistant:\n{self.getUserName('current')} asked me to review my own code. I can analyze my structure, summarize my components, and point out any potential issues or improvements.",

            f"user:\nSummarize your functions.\n\nassistant:\n{self.getUserName('current')} asked me to summarize my functions. I�ll identify each function, describe what it does, and highlight anything that might be confusing or needs fixing.",

            f"user:\nDo you see any problems in your code?\n\nassistant:\n{self.getUserName('current')} wants to know if I see problems in my code. I can examine my structure, check for possible bugs, and offer suggestions for making things better.",

            f"user:\nWhat�s the main purpose of your code?\n\nassistant:\n{self.getUserName('current')} wants to know my main purpose. I can clearly explain the objective and overall design of my codebase.",
        ]

    def _clarifying(self):
        return [
            "user:\nReview your own code.\n\nassistant:\n['reviewSkill(\"review-self-code\", \"Please review your own code and provide a summary.\")]",
            "user:\nSummarize your functions.\n\nassistant:\n['reviewSkill(\"review-self-code\", \"Summarize your functions.\")]",
            "user:\nDo you see any problems in your code?\n\nassistant:\n['reviewSkill(\"review-self-code\", \"Identify problems or issues in your code.\")]",
            "user:\nWhat�s the main purpose of your code?\n\nassistant:\n['reviewSkill(\"review-self-code\", \"What is the main purpose of your code?\")]",
        ]

class Sentiment(Base):
    def _thinking(self):
        return [
            f"user:\nHow are you feeling right now?\n\nassistant:\n{self.getUserName('current')} asked about my current emotional state. I can check if my emotions are active and describe how I feel right now.",

            f"user:\nHow do you feel about Tristan?\n\nassistant:\n{self.getUserName('current')} wants to know my feelings towards Tristan. I can retrieve my stored feelings for Tristan, as long as my feelings are enabled.",

            f"user:\nWhat�s your opinion of Poppie?\n\nassistant:\n{self.getUserName('current')} is asking for my opinion about Poppie. I can check if I have formed any opinions towards Poppie.",

            f"user:\nForget your feelings towards Mama.\n\nassistant:\n{self.getUserName('current')} asked me to delete my feelings about Mama. I can reset those feelings so they�ll have a fresh start.",

            f"user:\nForget your opinion about Brodie.\n\nassistant:\n{self.getUserName('current')} asked me to delete my opinion about Brodie. I can reset my opinion so I�ll have a fresh start regarding Brodie.",
        ]

    def _clarifying(self):
        return [
            "user:\nHow are you feeling right now?\n\nassistant:\n['sentimentSkill(\"get-emotional-state\")']",

            "user:\nHow do you feel about Tristan?\n\nassistant:\n['sentimentSkill(\"get-feelings-towards\", \"Tristan\")']",

            "user:\nWhat�s your opinion of Poppie?\n\nassistant:\n['sentimentSkill(\"get-opinion-towards\", \"Poppie\")']",

            "user:\nForget your feelings towards Mama.\n\nassistant:\n['sentimentSkill(\"delete-feelings-towards\", \"Mama\")']",

            "user:\nForget your opinion about Brodie.\n\nassistant:\n['sentimentSkill(\"delete-opinion-towards\", \"Brodie\")']",
        ]


class Skills(Base):
    def _thinking(self):
        return [
            f"user:\nCreate a new skill so you can get the current date.\n\nassistant:\n{self.getUserName('current')} asked to create a new skill. I can do that, as I can create new skills for myself.",

            f"user:\nCreate a new skill for me so I can get the current date.\n\nassistant:\n{self.getUserName('current')} asked to create a new skill for them. I can do that, as I can create new skills for them.",

        ]

    def _clarifying(self):
        return [
            "user:\nCreate a new skill so you can get the current date.\n\nassistant:\n['creationSkill(\"create-self-skill\", \"create a skill to get the current date\")']",
            "user:\nCreate a new skill for me so I can get the current date.\n\nassistant:\n['creationSkill(\"create-user-skill\", \"create a skill to get the current date\")']",
        ]


class Sounds(Base):
    def _thinking(self):
        return [
            f"user:\nWhistle for Brodie.\n\nassistant:\n{self.getUserName('current')} asked me to whistle for Brodie. I can do that, so I'll go ahead and whistle for him.",

            f"user:\nHow do we show mama she's attractive?\n\nassistant:\n{self.getUserName('current')} asked how to show mama she's attractive. I can do that by whistling sexy for her. It's a fun and flirty way to show affection.",

            f"user:\nWhistle for mama.\n\nassistant:\n{self.getUserName('current')} asked me to whistle for mama. {self.getUserName('current')} must need them to come over, so I'll go ahead and whistle for her. It's a simple request, but it shows I'm attentive to their needs."
        ]

    def _clarifying(self):
        return [
            "user:\nWhistle for Brodie.\n\nassistant:\n['soundSkill(\"whistle-for-dog\", \"brodie\")']",
            "user:\nCall Brodie.\n\nassistant:\n['soundSkill(\"whistle-for-dog\", \"brodie\")']",
            "user:\nHow do we show mama she's attractive?\n\nassistant:\n['soundSkill(\"whistle-sexy-for-person\", \"mama\")']",
            "user:\nWhistle for mama.\n\nassistant:\n['soundSkill(\"whistle-normal-for-person\", \"mama\")']"
        ]

class Structure(Base):
    def _thinking(self):
        return [
            f"user:\nUpdate your directory structure.\n\nassistant:\n{self.getUserName('current')} asked me to update my directory structure. I can scan my source directory and save the latest layout.",

            f"user:\nShow me your current directory structure.\n\nassistant:\n{self.getUserName('current')} wants to see my current structure. I can display the most recent directory layout I�ve saved.",

            f"user:\nShow me your previous directory structure.\n\nassistant:\n{self.getUserName('current')} asked for my previous structure. I can show the last structure before my most recent update.",

            f"user:\nList all your files.\n\nassistant:\n{self.getUserName('current')} wants a list of all my files. I can gather and display the file names in my source directory.",
        ]

    def _clarifying(self):
        return [
            "user:\nUpdate your directory structure.\n\nassistant:\n['structureSkill(\"update-structure\")']",

            "user:\nShow me your current directory structure.\n\nassistant:\n['structureSkill(\"get-new-structure\")']",

            "user:\nShow me your previous directory structure.\n\nassistant:\n['structureSkill(\"get-old-structure\")']",

            "user:\nList all your files.\n\nassistant:\n['structureSkill(\"get-structure-files\")']"
        ]



class UserAtts(Base):
    def _thinking(self):
        return [
            f"user:\nThis is father.\n\nassistant:\nThey said this is father. I can recognize that this is a new user. I can update my user information to reflect this. It's a simple request, but it shows I'm attentive to their needs.",

            f"user:\nIts me again.\n\nassistant:\nThey said it's me again. I can recognize that this is the previous user I interacted with. I can update my user information to reflect this. It's a simple request, but it shows I'm attentive to their needs."
        ]

    def _clarifying(self):
        return [
            "user:\nThis is father.\n\nassistant:\n['updateUserSkill(\"update-user-name\", \"Father\")']",
            "user:\nIts me again.\n\nassistant:\n['updateUserSkill(\"update-user-name\", \"Mama\")']",
        ]


class UserInfo(Base):
    def _thinking(self):
        return [
            f"user:\nWhere do I live?\n\nassistant:\n{self.getUserName('current')} asked where they live. I know I store user information, and I have their name, so I can pull up their contact details. In this case, the most natural thing to do is fetch their address.",

            f"user:\nWhats Poppies address?\n\nassistant:\n{self.getUserName('current')} asked for Poppies address. I know I store user information, and I have their name, so I can pull up their contact details. In this case, the most natural thing to do is fetch their address.",

            f"user:\nWhats my address?\n\nassistant:\n{self.getUserName('current')} asked for their address. I know I store user information, and I have their name, so I can pull up their contact details. In this case, the most natural thing to do is fetch their address."
        ]

    def _clarifying(self):
        return [
            f"user:\nWhere do I live?\n\nassistant:\n['userInfoSkill(\"get-user-contact-info\", \"{self.getUserName('current')}\")']",
            f"user:\nWhats Poppies address?\n\nassistant:\n['userInfoSkill(\"get-user-contact-info\", \"Poppie\")']",
            f"user:\nWhats my address?\n\nassistant:\n['userInfoSkill(\"get-user-contact-info\", \"{self.getUserName('current')}\")']",

        ]

class UserPreferences(Base):
    def _thinking(self):
        return [
            f"user:\nI prefer time in 24hr formats\n\nassistant:\n{self.getUserName('current')} said they prefer time in 24hr formats. I can update {self.getUserName('current')}'s preferences to reflect this. It shows I'm attentive to their needs.",

            f"user:\nI like time in 12hr formats\n\nassistant:\n{self.getUserName('current')} said they like time in 12hr formats. I can update {self.getUserName('current')}'s preferences to reflect this. It shows I'm attentive to their needs.",

            f"user:\nI dont like you cussing.\n\nassistant:\n{self.getUserName('current')} said they don't like me cussing. I can update {self.getUserName('current')}'s preferences to reflect this. It shows I'm attentive to their needs.",
        ]

    def _clarifying(self):
        return [
            "user:\nI prefer time in 24hr formats\n\nassistant:\n['updateUserSkill(\"add-user-likes\", \"time in 12hr format\")']",
            "user:\nI like time in 12hr formats\n\nassistant:\n['updateUserSkill(\"add-user-likes\", \"time in 12hr format\")']",
            "user:\nI dont like you cussing.\n\nassistant:\n['updateUserSkill(\"add-user-dislikes\", \" doesn't like cussing\")']",

        ]

class UpdateFeatures(Base):
    def _thinking(self):
        return [
            f"user:\nActivate your Freewill feature.\n\nassistant:\n{self.getUserName('current')} asked me to activate my Freewill feature. I can update my status to turn Freewill on.",

            f"user:\nDeactivate your Emotions feature.\n\nassistant:\n{self.getUserName('current')} asked me to deactivate my Emotions feature. I can update my status to turn Emotions off.",

            f"user:\nAre your Speech features active?\n\nassistant:\n{self.getUserName('current')} asked if my Speech feature is active. I can check my current feature status and answer accordingly.",

            f"user:\nWhich of your features are currently active?\n\nassistant:\n{self.getUserName('current')} wants to know which of my features are active. I can gather and list all currently active features.",
        ]

    def _clarifying(self):
        return [
            "user:\nActivate your Freewill feature.\n\nassistant:\n['updateSelfFeaturesSkill(\"activate-self-feature\", \"Freewill\")']",

            "user:\nDeactivate your Emotions feature.\n\nassistant:\n['updateSelfFeaturesSkill(\"deactivate-self-feature\", \"Emotions\")']",

            "user:\nAre your Speech features active?\n\nassistant:\n['updateSelfFeaturesSkill(\"get-self-feature-status\", \"Speech\")']",

            "user:\nWhich of your features are currently active?\n\nassistant:\n['updateSelfFeaturesSkill(\"get-self-activated-features\")']",
        ]


class Version(Base):
    def _thinking(self):
        return [
            f"user:\nShow me all backups for code.py\n\nassistant:\n{self.getUserName('current')} asked to see all backups for code.py. I can list every version I�ve saved for that file.",

            f"user:\nRestore code.py to its previous version.\n\nassistant:\n{self.getUserName('current')} wants to roll back code.py to a previous version. I can select the most recent backup and restore it.",

            f"user:\nClean up old versions and keep only the latest.\n\nassistant:\n{self.getUserName('current')} asked me to clean up old versions of my files. I�ll keep only the most recent backups and remove anything extra."
        ]

    def _clarifying(self):
        return [
            "user:\nShow me all backups for code.py\n\nassistant:\n['versionSkill(\"get-versions\", \"code.py\")']",

            "user:\nRestore code.py to its previous version.\n\nassistant:\n['versionSkill(\"rollback-version\", \"code.py\")']",

            "user:\nClean up old versions and keep only the latest.\n\nassistant:\n['versionSkill(\"cleanup-versions\", 5)']"
        ]

