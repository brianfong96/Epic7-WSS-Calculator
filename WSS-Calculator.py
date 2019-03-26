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
HELP_PROMPT = """
What gear do I upgrade?

Due to the changes on 7 Mar 2019 which exponentially increased the difficulty and costs involved in rolling ideal Heroic gear, the procedure for deciding what gear to upgrade has changed. Under the new system, non-Epic gear will only roll their full complement of substats by the +12 upgrade tier.
The first rule of equipment use/upgrades was not to upgrade anything with a flat substat, but this is now not practicable as the flat substat may appear at the +12 level followed by a +15 roll on the flat substat. Thus, we must now upgrade based on the strength of known stats, rather than attempting to eliminate unknowns early.
The measure we will be using to judge the overall strength of a piece of equipment will be henceforth termed as ‘weighted statistic sum’, or WSS, for short.
To compute the WSS of a piece of gear, add all percentage-based stats together as follows:

Attack, Defense, Health, Effectiveness, Resistance, Critical Hit Damage - x1.0
Critical Hit Rate - x1.5
Speed (this is always flat, but treat it as if it had a %) - x2.0

The sum of the above stats multiplied by their respective weights is the WSS.

The reason for the higher weightage of critrate and speed are due to the lower amounts you can get for each in substat form. As they are easier to get in set or mainstat forms, the recommended builds account for that.

Flat Attack, Defense and Health are worth less than nothing as they ‘suck’ upgrades. Never even begin to upgrade gear with even one flat non-Speed stat.

As the upgrade costs are a fixed ratio to the amount of equipment EXP required to upgrade gear, and higher item level gear requires much more EXP (but gives better stats), the following are the WSS cutoffs for each gear tier, regardless of colour.

Item Level 88 (Tier 7)
+0: Only upgrade if WSS > 22%.
+3: Only upgrade if WSS > 29%.
+6: Only upgrade if WSS > 36%.
+9: Only upgrade if WSS > 42%.
+12: Only upgrade if WSS > 48%.

Item Level 72-85 (Tier 6)
+0: Only upgrade if WSS > 20%.
+3: Only upgrade if WSS > 26%.
+6: Only upgrade if WSS > 32%.
+9: Only upgrade if WSS > 38%.
+12: Only upgrade if WSS > 44%.

Item Level 58-71 (Tier 5)
+0: Only upgrade if WSS > 18%.
+3: Only upgrade if WSS > 24%.
+6: Only upgrade if WSS > 30%.
+9: Only upgrade if WSS > 35%.
+12: Only upgrade if WSS > 40%.

The above upgrade protocol ensures that at whatever point you terminate the upgrading process, the equipment will be above average for its rarity and type. You can use the gear as is as stopgaps, or refodder them into better gear as you wish.
"""

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
