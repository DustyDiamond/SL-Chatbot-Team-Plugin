#!/usr/bin/python
# -*- coding: utf-8 -*-
#---------------------------------------------------------
# Import Libraries
#---------------------------------------------------------
import os
import json
import codecs

from datetime import datetime

#---------------------------------------------------------
# Script information
#---------------------------------------------------------
ScriptName = "Team Command"
Website = "https://github.com/DustyDiamond/SL-Chatbot-Team-Plugin/blob/main/README.md"
Description = "Answers with the Current Team you're playing with"
Creator = "DustyDiamond"
Version = "1.0.6"
Command = "!team"

#---------------------------------------------------------
# Globals
#---------------------------------------------------------
settings = {}
languages = {}
users = []
und = ""
team = ""

def Init():
    global settings, languages

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
    global settings, users, languages, team 
    outputMessage = ""
    username = data.User  
    team = settings["users"] 
    if data.IsChatMessage():
        #---------------------------------------------------------
        # !setteam branch
        #---------------------------------------------------------
        if data.GetParam(0).lower() == (left(settings["command"],1) + "set" + right(settings["command"],(len(settings["command"])-1))) and Parent.HasPermission(data.User, settings["permission"], ""):        
            paramCount = int(data.GetParamCount())
            users = []

            #log("paramCount: "+ str(paramCount))

            for i in range(paramCount):
                if i == 0:
                    continue
                else:
                    try:
                        users.insert(i,data.GetParam(i))
                        #log(str(i) + ": " + data.GetParam(i))
                    except:
                        users.append(data.GetParam(i))
                        #log(str(i) + ": " + data.GetParam(i))

                team_msg()
                #team = settings["users"]  

                if (settings["useSetteam"]):
                    outputMessage = settings["setteam"]
                else:
                    outputMessage = settings["bot_response"]

                #log("Team Set!")       

        #---------------------------------------------------------
        # !team branch
        #---------------------------------------------------------
        elif data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, "Everyone", ""):
            
            if settings["users"] == "" or team == "":
                return
            
            username = data.UserName
            #team = settings["users"]  
            outputMessage = settings["bot_response"]

        outputMessage = outputMessage.replace("$team", team) 
        # final send of message
        send_message(outputMessage.format(username))
        return

# Misc Functions
def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log("INFO: ","[" + ScriptName + "] " + dt_string + ": " + message)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #log("Message Sent")
    return

# build team message
def team_msg():
    global settings, users, languages, team
    lang = settings["language"]
    und = languages[lang]
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
        
    
    settings["users"] = team
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