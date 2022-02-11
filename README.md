# SL Chatbot Team Plugin

A simple Plugin for Streamlabs Chatbot.  
You can set your own command in Script Settings in Chatbot. Standard is `!team` and `!setteam`.  
If you set your command to anything new, the set-command is `!set<command>`.  

## Installation

Download the .zip file from Release-Section, then click import button in SL Chatbot und Scripts and import the .zip-file. There's no need to unpack the .zip-file.  

## Usage

With `!setteam <user1> <user2>` you can add as many users as you whish.  
With `!team` the bot answers with the text you can set in settings and replaces the `$team` with the userlist.  
*It's important that you have `$team` in your bot response*  
*If you leave the `@{0}` in your bot response, it will @ the user who triggered the command*  

You can set the language of the filler `and` between the last and second last name in list, that will automatically be set when you have more than one user in your team command. Currently there is only English and German supported.  
*Note that you have to set your bot responses for yourself. They get NOT translatet. It's just for the `and`*
