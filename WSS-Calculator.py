#!/usr/bin/env python
# The following calculations are based on this google doc
# https://docs.google.com/document/d/1aKpEZ6g42YMyU4QPsWcrVUT9UNHgbeXlYvYyPeyPz9Y/mobilebasic 
from appJar import gui

CALCULATE = "Calculate"
CANCEL = "Cancel"
HELP = "Help"
ATTACK_PERCENTAGE = "Substat Attack %"
DEFENSE_PERCENTAGE = "Substat Defense %"
HEALTH_PERCENTAGE = "Substat Health %"
EFFECTIVENESS_PERCENTAGE = "Substat Effectiveness %"
RESISTANCE_PERCENTAGE = "Substat Effectiveness Resistance %"
CRIT_DAMAGE_PERCENTAGE = "Substat Crit Damage %"
CRIT_RATE = "Substat Crit Rate %"
SPEED = "Substat Speed"
STATS = [ATTACK_PERCENTAGE, DEFENSE_PERCENTAGE, HEALTH_PERCENTAGE, EFFECTIVENESS_PERCENTAGE, RESISTANCE_PERCENTAGE, CRIT_DAMAGE_PERCENTAGE, CRIT_RATE, SPEED]
LEVEL = "Gear Level (Min lvl 58)"
ENHANCE = "Current Enhancement (Default 0)"
with open('help.txt', 'r') as f:
    HELP_PROMPT = f.read()
f.close()

T7_WSS = {0:22, 3:29, 6:36, 9:42, 12:48}
T6_WSS = {0:20, 3:26, 6:32, 9:38, 12:44}
T5_WSS = {0:18, 3:24, 6:30, 9:35, 12:40}

def press(button):
    if button == CANCEL:
        app.stop()
    elif button == CALCULATE:
        wss = 0
        valid = True
        for stat in STATS:
            s = app.getEntry(stat).strip()
            if s.isnumeric():
                s = int(s)
                if stat == SPEED:
                    s = s * 2
                if stat == CRIT_RATE:
                    s = s * 1.5
            elif s == str():
                s = 0
            else:
                valid = False
                s = 0
            wss += s
        gear_lvl = app.getEntry(LEVEL).strip()
        enhance_lvl = app.getEntry(ENHANCE).strip()
        if gear_lvl.isnumeric() and enhance_lvl.isnumeric():
            gear_lvl = int(gear_lvl)
            enhance_lvl = int(enhance_lvl)
            if gear_lvl < 58:
                app.infoBox("ERROR", "Gear Level too Low")
                return
        else:
            valid = False
        if valid:
            T_WSS = T5_WSS
            if gear_lvl >= 88:
                T_WSS = T7_WSS
            elif gear_lvl >= 72:
                T_WSS = T6_WSS
            
            base = 0
            if enhance_lvl >= 12:
                base = 12
            elif enhance_lvl >= 9:
                base = 9
            elif enhance_lvl >= 6:
                base = 6
            elif enhance_lvl >= 3:
                base = 3
            if wss >= T_WSS[base]:                
                app.infoBox("Result", "You Should upgrade gear till " + str(base+3))
            else:
                app.infoBox("Result", "It's not worth upgrading the gear")
        else:
            app.infoBox("ERROR", "INVALID INPUT")
    elif button == HELP:
        app.infoBox("Help", HELP_PROMPT)
    return

app = gui("WSS Calculator", "800x400")
app.setBg("green")
app.setFont(18)
app.addLabel("title", "WSS Calculator")
app.setLabelBg("title", "blue")
app.addLabelEntry(ATTACK_PERCENTAGE)
app.addLabelEntry(DEFENSE_PERCENTAGE)
app.addLabelEntry(HEALTH_PERCENTAGE)
app.addLabelEntry(EFFECTIVENESS_PERCENTAGE)
app.addLabelEntry(RESISTANCE_PERCENTAGE)
app.addLabelEntry(CRIT_DAMAGE_PERCENTAGE)
app.addLabelEntry(CRIT_RATE)
app.addLabelEntry(SPEED)
app.addLabelEntry(LEVEL)
app.addLabelEntry(ENHANCE)
app.addButtons([CALCULATE, CANCEL, HELP], press)
app.go()
