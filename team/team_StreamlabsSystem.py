import os
import json
import codecs

from datetime import datetime

ScriptName = "Team Command"
Website = "https://github.com/DustyDiamond/SL-Chatbot-Team-Plugin/blob/main/README.md"
Description = "Answers with the Current Team you're playing with"
Creator = "DustyDiamond"
Version = "1.0.2"
Command = "!team"

settings = {}
languages = {}
users = []
und = ""

def Init():
    global settings, users, languages

    work_dir = os.path.dirname(__file__)

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    
    except:
        Parent.Log("ERROR: ", "[" + ScriptName + "]:  Unable to load settings during execution! (Init)")

    try:
        with codecs.open(os.path.join(work_dir, "languages.json"), encoding='utf-8-sig') as json_file:
            languages = json.load(json_file, encoding='utf-8-sig')
    except:
        Parent.Log("ERROR: ", "[" + ScriptName + "]:  Unable to load languages during execution! (Init)")

    return


def Execute(data):
    global settings, users, languages
    outputMessage = ""
    lang = settings["language"]
    und = languages[lang]
    username = data.User

    # !team branch
    if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, "Everyone", ""):
        
        if settings["users"] == "":
            return
        
        userId = data.User
        username = data.UserName
        if (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
            if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
                cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
                cd = str(cdi)
                outputMessage = settings["onCooldown"]
            else:
                cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
                cd = str(cdi)
                outputMessage = settings["onUserCooldown"]
            outputMessage = outputMessage.replace("$cd", cd)

        else:
            team = ""
            if len(users) == 1:
                team = users[0]
            else:
                for i in users[:-1]:
                    if i == "": 
                        continue

                    team = team + i + ", "
                else:
                    team = left(team,(len(team) -2)) + " " + und + " " + users[-1]
                
            outputMessage = settings["bot_response"]
            outputMessage = outputMessage.replace("$team", team)
            #outputMessage = "!team was triggered"

    # !setteam branch
    elif data.IsChatMessage() and data.GetParam(0).lower() == (left(settings["command"],1) + "set" + right(settings["command"],(len(settings["command"])-1))) and Parent.HasPermission(data.User, settings["permission"], ""):        
        paramCount = int(data.GetParamCount())
        users = []

        log("paramCount: "+ str(paramCount))

        for i in range(paramCount):
            if i == 0:
                continue
            else:
                try:
                    users.insert(i,data.GetParam(i))
                    log(str(i) + ": " + data.GetParam(i))
                except:
                    users.append(data.GetParam(i))
                    log(str(i) + ": " + data.GetParam(i))


        if settings["useSetteam"] == True:
            # Extra message for !setteam
            userlist = ""
            team = ""
            if len(users) == 1:
                userlist = users[0]
                team = team + users[0]
            else:
                for x in users[:-1]:
                    if x == "":
                        continue

                    userlist = userlist + x + ","
                    team = team + x + ", "
                else:
                    userlist = userlist + users[-1]
                    team = left(team,(len(team) -2)) + " " + und + " " + users[-1]

            settings["users"] = userlist
            outputMessage = settings["setteam"]
            outputMessage = outputMessage.replace("$team", team)

        else:
            # Same Message for Both
            team = ""
            if len(users) == 1:
                team = users[0]
            else:
                for i in users[:-1]:
                    if i == "": 
                        continue

                    team = team + i + ", "
                else:
                    team = left(team,(len(team) -2)) + " " + und + " " + users[-1]
                
            outputMessage = settings["bot_response"]
            outputMessage = outputMessage.replace("$team", team)

    # final send of message
    send_message(outputMessage.format(username))
    return

# Misc Functions
def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log("INFO:", ScriptName + ": " + dt_string + ": " + message)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    log("Message Sent")
    return

def OpenWebSite():
	os.startfile(Website)

def ReloadSettings(jsonData):
    Init()
    return

def Tick():
    return

def Unload():
    return

# Define Helper Functions
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]