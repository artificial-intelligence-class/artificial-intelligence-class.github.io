from pymagnitude import *
from graph import *
from a_star import *
import random
import time
import csv
import re
import copy
from queue import Queue
from r2d2_hw4 import *

from client import DroidClient

import contextlib
import sys

# The following structure is useful for supressing print statements
class PrintsToOuterSpace(object):
    def write(self, x): pass

@contextlib.contextmanager
def noStdOut():
    save_stdout = sys.stdout
    sys.stdout = PrintsToOuterSpace()
    yield
    sys.stdout = save_stdout

class Robot:
    def __init__(self, droidID, wordSimCutoff, voice):
        self.embeddings = WordEmbeddings("Your Path Here: ") # Change the path
        self.createSentenceEmbeddings()
        self.droid = DroidClient()
        self.name = "R2"
        self.wordSimCutoff = wordSimCutoff
        self.voice = voice

        self.numDict = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twenty": 20, "fifty": 50, "hundred": 100}

        self.holoProjectorIntensity = 0
        self.logicDisplayIntensity = 0
        self.frontRGB = (0, 0, 0)
        self.backRGB = (0, 0, 0)

        self.heading = 0
        self.speed = 0.5
        self.oneFootConstant = 0.65

        self.grid = [[]]
        self.gridSize = 1
        self.pos = (-1, -1)
        self.objCoord = dict()
        self.G = Graph(self.grid)

        self.waddling = False

        self.happiness = 0 # from -1 to 1

        self.colorToRGB = {}
        with open('data/colors.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.colorToRGB[row[0]] = (int(row[2]), int(row[3]), int(row[4]))

        connected = False
        i = 0
        if len(droidID) != 7: i = 3
        while not connected and i < 3:
            with noStdOut():
                connected = self.droid.connect_to_droid(droidID)
            i += 1
        if i == 3: self.prettyPrint("We could not connect to the droid. We are starting in non-connected mode. Please connect through commands.")

    def createSentenceEmbeddings(self):
        trainingSentences = loadTrainingSentences("data/r2d2TrainingSentences.txt")

        self.categories = [x for x in trainingSentences]

    def inputCommand(self, command):
        commandType = self.embeddings.getCategory(command, "data/r2d2TrainingSentences.txt")

        if not self.droid.connected_to_droid and commandType != "connection":
            print("You are not connected to a droid right now! Please connect to a droid before issuing any non-connection commands")
            return

        if "i like you" in command.lower():
            # max happiness
            self.happiness = 1
            with noStdOut(): self.happyAnimation()
            if commandType == "no":
                print(self.name + ": Awwww, thank you <3")
                return
        elif "i hate you" in command.lower():
            # min happiness
            self.happiness = -1
            with noStdOut():
                choice = random.choice([0, 1, 2])
                if choice == 0: self.droid.animate(23)
                if choice == 1: self.droid.play_sound(4)
                if choice == 1: self.droid.play_sound(12)
            if commandType == "no":
                print(self.name + ": >:(")
                return

        if commandType == "no" and not self.voice:
            subcommand = input(self.name + ": I could not understand your command. Do you want to add this command to the training set? (yes/no): ")
            if "yes" in subcommand.lower():
                subcommand = input("What category do you want to add it to? Choices are driving, light, head, state, connection, stance, animation, or grid: ")
                subcommand = subcommand.strip().lower()
                if subcommand in self.categories:
                    with open("data/r2d2TrainingSentences.txt", 'a') as the_file:
                        the_file.write(subcommand + 'Sentences :: ' + command + '\n')
                    print("Command added. Changes are now present.")
                else:
                    print(subcommand + " not a valid category.")
            else:
                self.happiness = max(-1, self.happiness - 0.1) # happiness update
            return
        elif commandType == "no":
            self.happiness = max(-1, self.happiness - 0.1) # happiness update
            print(self.name + ": I could not understand your command.")
            with noStdOut(): self.commandNotUnderstood()
            return

        # If the droid is not happy, with a certain random chance related to happiness levels, do not execute the command
        if self.happiness < 0:
            if random.random() < abs(self.happiness):
                print(self.name + ": I'm angry at you! I will not execute your "  + commandType + " command. (Say I like you to make me happy.)")
                if self.droid.connected_to_droid:
                    with noStdOut(): self.droid.play_sound(random.choice([4, 12]))
                return

        if not self.voice:
            subcommand = input(self.name + ": I parsed this as a " + commandType + " command. Is this correct? (yes/no): ")
            if "no" in subcommand.lower():
                subcommand = input("What category does this command belong to? Choices are driving, light, head, state, connection, stance, animation, or grid (if you do not want to add this to the training set, type anything else): ")
                subcommand = subcommand.strip().lower()
                if subcommand == commandType:
                    print("This is what we parsed it as! We are not adding this sentence, continuing execution...")
                elif subcommand in self.categories:
                    with open("data/r2d2TrainingSentences.txt", 'a') as the_file:
                        the_file.write(subcommand + 'Sentences :: ' + command + '\n')
                    print("Command added. Changes are now present.")
                    return
                else:
                    print(subcommand + " not a valid category. Resuming execution ...")

        result = getattr(self, commandType + "Parser")(command.lower())
        if result:
            print(self.name + ": Done executing "  + commandType + " command.")
            if hasattr(self.droid, "is_continuous_roll"):
                if self.droid.is_continuous_roll:
                    return
            if self.droid.connected_to_droid and commandType != "animation":
                with noStdOut(): self.droid.play_sound(random.choice([20, 29])) # play a sound after executing a successful command
        else:
            print(self.name + ": I could not understand your " + commandType + " command.")
            self.happiness = max(-1, self.happiness - 0.1) # happiness update
            if self.droid.connected_to_droid:
                with noStdOut(): self.commandNotUnderstood()

    def happyAnimation(self):
        choice = random.choice([0, 1, 2, 3])
        if choice == 0: self.droid.play_sound(30)
        elif choice == 1: self.droid.animate(5)
        elif choice == 2: self.droid.play_sound(34)
        else: self.droid.animate(24)
        time.sleep(0.5)

    def commandNotUnderstood(self):
        if self.happiness <= -0.8:
            self.droid.play_sound(7)
        elif self.happiness <= -0.6:
            self.droid.play_sound(2)
            time.sleep(0.5)
        elif self.happiness <= -0.3:
            self.droid.play_sound(random.choice([4, 12]))
        elif self.happiness <= 0:
            choice = random.choice([0, 1])
            if choice == 0: self.droid.animate(0)
            if choice == 1: self.droid.play_sound(1)

    def reset(self):
        self.droid.roll(0, 0, 0)

    def disconnect(self):
        self.droid.disconnect()

    def flash_colors(self, colors, seconds = 1, front = True):
        if front:
            for color in colors:
                self.droid.set_front_LED_color(*color)
                time.sleep(seconds)
        else:
            for color in colors:
                self.droid.set_back_LED_color(*color)
                time.sleep(seconds)

    def askForColor(self, lightPosition = "both"):
        if lightPosition != "both":
            print("We detect that you want to change your " + lightPosition + " light, but could not find a color.")
        else:
            print("We parsed this as a light command, but could not find a color.")
        if self.voice: return False
        command = input("Do you want to input a color? (yes/no): ")
        color = False
        if "yes" in command.lower():
            print("You may have inputted a color, but it is not in our database or is mispelled. Please input a color or rgb tuple.")
            command = input("If you want to add the color to the database, input color_name (one string) :: rgb tuple: ")

            words = re.split('\W+', command)
            words = [x for x in words if x != ""]
            for word in words:
                if word in self.colorToRGB: color = self.colorToRGB[word]
            if len(words) == 4:
                try:
                    color = (int(words[1]), int(words[2]), int(words[3]))
                    colorName = words[0]
                    with open('data/colors.csv', 'a') as csvStorer:
                        csvStorer.write('\n' + colorName + ',R2D2 ' + colorName + ',' + words[1] + ',' + words[2] + ',' + words[3])
                    print(colorName + " added to database. It will be available on the next restart.")
                except ValueError:
                    pass
            elif len(words) == 3:
                try:
                    color = (int(words[0]), int(words[1]), int(words[2]))
                except ValueError:
                    pass

        return color

    def lightParser(self, command):
        # slot filler for lights
        ################################################

        # lights - keeps track of which lights to turn on, combination of holoEmit, logDisp, front, and back
        # intensities - keeps track of what intensity to change those lights to, combination of blink, dim, off, on
        # percent - boolean if percent change
        # valueChange - keeps track if we want to increase or decrease value, either "add" or "sub"
        # numValue - keeps track of numerical value
        # colors - rgb values of colors in sentence, also detects rgb tuples
        slots = {"lights": [], "intensities": set(), "percent": False, "valueChange": False, "numValue": False, "colors": []}

        ################################################

        solutionSlots = self.embeddings.lightParser(command)

        if not solutionSlots["lights"]: solutionSlots["lights"] == ["front", "back"]
        slots["lights"] = solutionSlots["lights"]
        if solutionSlots["add"]: slots["valueChange"] = "add"
        if solutionSlots["sub"]: slots["valueChange"] = "sub"
        if solutionSlots["off"]: slots["intensities"].add("off")
        if solutionSlots["on"]: slots["intensities"].add("on")

        if "%" in command:
            slots["percent"] = True

        if "dim" in command:
            slots["intensities"].add("dim")
        if "blink" in command:
            slots["intensities"].add("blink")

        words = re.split('\W+', command)
        words = [x for x in words if x != ""]

        i = 0
        for word in words:
            if word in self.numDict: word = self.numDict[word]
            if i < len(words) - 2:
                try:
                    rgb = (int(word), int(words[i+1]), int(words[i+2]))
                    slots["colors"].append(rgb)
                except ValueError:
                    pass
            if self.embeddings.vectors.similarity("percent", word) > self.wordSimCutoff:
                slots["percent"] = True

            if word in self.colorToRGB:
                slots["colors"].append(self.colorToRGB[word])
            i += 1
            try:
                increment = int(word)
                slots["numValue"] = increment
            except ValueError:
                continue

        return self.lightSlotsToActions(slots)

    def lightSlotsToActions(self, slots):
        if "holoEmit" in slots["lights"]:
            if "blink" in slots["intensities"]:
                self.droid.set_holo_projector_intensity((self.holoProjectorIntensity + 1)%2)
                time.sleep(0.3)
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "dim" in slots["intensities"]:
                self.holoProjectorIntensity = self.holoProjectorIntensity / 2
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "off" in slots["intensities"]:
                self.holoProjectorIntensity = 0
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "on" in slots["intensities"]:
                self.holoProjectorIntensity = 1
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            else:
                return False
            return True

        if "logDisp" in slots["lights"]:
            if "blink" in slots["intensities"]:
                self.droid.set_logic_display_intensity((self.logicDisplayIntensity + 1)%2)
                time.sleep(0.3)
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "dim" in slots["intensities"]:
                self.logicDisplayIntensity = self.logicDisplayIntensity / 2
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "off" in slots["intensities"]:
                self.logicDisplayIntensity = 0
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "on" in slots["intensities"]:
                self.logicDisplayIntensity = 1
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            else:
                return False
            return True

        if slots["valueChange"]:
            lights = slots["lights"]

            if not slots["numValue"]:
                if self.voice: return False
                if slots["percent"]: command = input("Percent not found in command, please input percent to change by here: ")
                else: command = input("Increment not found in command, please input amount to change by here: ")
                try:
                    command = command.replace("%", "")
                    slots["numValue"] = int(command)
                except ValueError:
                    return False

            if slots["valueChange"] == "sub": slots["numValue"] = -slots["numValue"]

            red = self.colorToRGB["red"]
            green = self.colorToRGB["green"]
            blue = self.colorToRGB["blue"]

            if set(slots["colors"]).isdisjoint({red, green, blue}):
                command = input("Did not find what values (red/blue/green) to change, input what values to change: ")
                if "red" in command: slots["colors"].append(red)
                if "green" in command: slots["colors"].append(green)
                if "blue" in command: slots["colors"].append(blue)

            if set(slots["colors"]).isdisjoint({red, green, blue}): return False

            perc = slots["percent"]
            value = slots["numValue"]

            if red in slots["colors"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (max(0, min(rgb[0] + ((1-perc)*100 + perc*rgb[0])*value/100, 255)), rgb[1], rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if green in slots["colors"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], max(0, min(rgb[1] + ((1-perc)*100 + perc*rgb[1])*value/100, 255)), rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if blue in slots["colors"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], rgb[1], max(0, min(rgb[2] + ((1-perc)*100 + perc*rgb[2])*value/100, 255))))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))

            return True

        if "back" in slots["lights"] and len(slots["lights"]) == 1:
            if len(slots["colors"]) > 1:
                seconds = slots["numValue"]
                if not seconds: seconds = 1
                self.flash_colors(slots["colors"], seconds, False)
            elif len(slots["colors"]) == 1:
                self.backRGB = slots["colors"][0]
            else:
                color = self.askForColor("back")
                if not color: return False
                self.backRGB = color

            self.droid.set_back_LED_color(*self.backRGB)
            return True

        if ("front" in slots["lights"] and len(slots["lights"]) == 1) or len(slots["colors"]) > 1:
            if len(slots["colors"]) > 1:
                seconds = slots["numValue"]
                if not seconds: seconds = 1
                self.flash_colors(slots["colors"], seconds)
            elif len(slots["colors"]) == 1:
                self.frontRGB = slots["colors"][0]
            else:
                color = self.askForColor("front")
                if not color: return False
                self.frontRGB = color

            self.droid.set_front_LED_color(*self.frontRGB)
            return True

        if len(slots["colors"]) == 1:
            self.backRGB = slots["colors"][0]
            self.frontRGB = slots["colors"][0]
            self.droid.set_back_LED_color(*self.backRGB)
            self.droid.set_front_LED_color(*self.frontRGB)
            return True

        if "blink" in slots["intensities"]:
            self.droid.set_holo_projector_intensity((self.holoProjectorIntensity + 1)%2)
            self.droid.set_logic_display_intensity((self.holoProjectorIntensity + 1)%2)
            time.sleep(0.3)
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)  
            return True
        elif "dim" in slots["intensities"]:
            self.holoProjectorIntensity = 0
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.logicDisplayIntensity = 0
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            self.backRGB = tuple(x/2 for x in self.backRGB)
            self.frontRGB = tuple(x/2 for x in self.frontRGB)
            self.droid.set_back_LED_color(*self.backRGB)
            self.droid.set_front_LED_color(*self.frontRGB)
            return True
        elif "off" in slots["intensities"]:
            self.holoProjectorIntensity = 0
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.logicDisplayIntensity = 0
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            self.backRGB = (0, 0, 0)
            self.frontRGB = (0, 0, 0)
            self.droid.set_back_LED_color(*self.backRGB)
            self.droid.set_front_LED_color(*self.frontRGB)
            return True
        elif "on" in slots["intensities"]:
            self.holoProjectorIntensity = 1
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.logicDisplayIntensity = 1
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            return True

        if len(slots["colors"]) == 0:
            color = self.askForColor()
            if color:
                self.backRGB = color
                self.frontRGB = color
                self.droid.set_back_LED_color(*self.backRGB)
                self.droid.set_front_LED_color(*self.frontRGB)
                return True

        return False

    def angleParser(self, index, directions):
        if index >= len(directions): return (0, -1)

        cDir = directions[index]

        if cDir == "go" or cDir == "turn" or cDir == "by": return (0, -1)

        angle = 0
        if cDir == "north": angle = self.heading
        elif cDir == "south": angle = (self.heading + 180) % 360
        elif cDir == "east": angle = (self.heading + 90) % 360
        elif cDir == "west": angle = (self.heading + 270) % 360
        elif cDir == "northeast": angle = (self.heading + 45) % 360
        elif cDir == "northwest": angle = (self.heading + 315) % 360
        elif cDir == "southeast": angle = (self.heading + 135) % 360
        elif cDir == "southwest": angle = (self.heading + 225) % 360
        elif cDir == "forward": angle = self.droid.angle
        elif cDir == "backward": angle = (self.droid.angle + 180) % 360
        elif cDir == "right": angle = (self.droid.angle + 90) % 360
        elif cDir == "left": angle = (self.droid.angle + 270) % 360

        if index + 1 == len(directions): return (angle, index + 1) 
        elif directions[index + 1] != "by": return (angle, index + 1) 
        elif directions[index + 1] == "by" and index + 2 == len(directions): return (0, -1)
        else:
            nDir = directions[index + 2]
            angle2 = None
            if nDir == "north": angle2 = self.heading
            elif nDir == "south": angle2 = (self.heading + 180) % 360
            elif nDir == "east": angle2 = (self.heading + 90) % 360
            elif nDir == "west": angle2 = (self.heading + 270) % 360
            elif nDir == "northeast": angle2 = (self.heading + 45) % 360
            elif nDir == "northwest": angle2 = (self.heading + 315) % 360
            elif nDir == "southeast": angle2 = (self.heading + 135) % 360
            elif nDir == "southwest": angle2 = (self.heading + 225) % 360
            else: return (0, -1)

            return ((angle + angle2) // 2, index + 3)

    def drivingParser(self, command):
        # slot filler for lights
        ################################################

        # directions - keeps track of directions, ordered combination of go, turn, by, cardinal directions (north), and directions (right)
        # percent - boolean if percent change
        # speedChange - keeps track if we want to change speed, either "add", "sub", or "set"
        # numValues - keeps track of numerical values
        # continuous - "stop" or "start" continuous roll
        # threat - designates if there is a threat (run away!)
        # shape - determines what shape to drive in
        # driveModifiers - modifier words for driving (non-continuous), "half" and "twice" for speed (temporary), "feet" and "seconds" for determining length
        # heading - determines if the sentence talks about a heading
        slots = {"directions": [], "percent": False, "speedChange": False, "numValues": Queue(),
        "continuous": None, "threat": False, "shape": [], "driveModifiers": [], "heading": False}

        ################################################

        solutionSlots = self.embeddings.drivingParser(command)

        if solutionSlots["add"]: slots["speedChange"] = "add"
        if solutionSlots["sub"]: slots["speedChange"] = "sub"
        if "set" in command: slots["speedChange"] = "set"

        slots["directions"] = solutionSlots["directions"]
        if "u-turn" in command: slots["directions"].append("backward")

        if re.search(r"\b(circle|donut)\b", command, re.I):
            slots["shape"].append("circle")
        if re.search(r"\b(square)\b", command, re.I):
            slots["shape"].append("square")

        if "half" in command: slots["driveModifiers"].append("half")
        if "twice" in command: slots["driveModifiers"].append("twice")
        if "feet" in command or "foot" in command: slots["driveModifiers"].append("feet")
        if "seconds" in command or "second" in command: slots["driveModifiers"].append("seconds")

        if "start" in command or "continuous" in command:
            slots["continuous"] = "start"
        if "stop" in command or "halt" in command or "freeze" in command:
            slots["continuous"] = "stop"

        if "run away" in command:
            slots["continuous"] = "start"
            slots["threat"] = True

        if "%" in command:
            slots["percent"] = True

        if "heading" in command:
            slots["heading"] = True

        command = command.strip()
        if command[-1] == ".": command = command[:-1]
        words = re.split('[^\w.]+', command)
        words = [x for x in words if x != ""]

        for word in words:
            if self.embeddings.vectors.similarity("percent", word) > self.wordSimCutoff:
                slots["percent"] = True
            if word in self.numDict: word = self.numDict[word]

            try:
                value = float(word)
                slots["numValues"].put(value)
            except ValueError:
                continue

        return self.drivingSlotsToActions(slots)

    def drivingSlotsToActions(self, slots):
        if "circle" in slots["shape"]:
            for heading in range(0, 360, 30):
                self.droid.roll(self.speed, heading, 1)
            self.droid.roll(0, 0, 0)
            return True
        if "square" in slots["shape"]:
            for heading in range(0, 360, 90):
                self.droid.roll(0, heading, 0)
                time.sleep(0.35)
                self.droid.roll(self.speed, heading, 1)
            self.droid.roll(0, 0, 0)
            return True

        if slots["continuous"] == "start":
            angle = None
            if len(slots["directions"]) == 0:
                angle = self.droid.angle
            else:
                tup = self.angleParser(0 + (slots["directions"][0] == "go" and len(slots["directions"]) > 1), slots["directions"])
                if tup[1] == -1: angle = self.droid.angle
                else: angle = tup[0]
            if slots["threat"]: angle = (angle + 180) % 360

            self.droid.roll_continuous(self.speed, angle)
            return True
        if slots["continuous"] == "stop":
            self.waddling = False
            self.droid.stop_roll()
            return True

        if slots["heading"]:
            if slots["numValues"].empty():
                print("Heading requires a numerical value")
                return False
            if len(slots["directions"]) == 0:
                self.heading = slots["numValues"].get()
            elif slots["directions"][0] == "turn":
                self.droid.roll(0.5, (self.heading + slots["numValues"].get()) % 360, 0)
            else:
                tup = self.angleParser(0, slots["directions"])
                if tup[1] == -1: return False
                self.heading = (self.heading + slots["numValues"].get() + (self.heading - tup[0])) % 360
            return True

        if slots["speedChange"]:
            perc = slots["percent"]
            mult = 1
            if slots["speedChange"] == "sub": mult = -1

            if slots["speedChange"] == "set":
                if slots["numValues"].empty():
                    print("Setting speed requires a numerical value")
                    return False
                self.speed = ((1-perc)*100 + perc*self.speed)*slots["numValues"].get()/100
            elif not slots["numValues"].empty():
                self.speed = self.speed + mult*((1-perc)*100 + perc*self.speed)*slots["numValues"].get()/100
            else:
                self.speed += mult*0.25

            if self.speed == 0: print("Speed can't be 0, setting it to 0.1.")
            self.speed = max(min(self.speed, 1), 0.1)

            if hasattr(self.droid, "is_continuous_roll"):
                if self.droid.is_continuous_roll:
                    self.droid.roll_continuous(self.speed, self.droid.angle)
            return True

        if len(slots["directions"]) > 0:
            if hasattr(self.droid, "is_continuous_roll"):
                if self.droid.is_continuous_roll:
                    if slots["directions"][0] == "turn":
                        if len(slots["directions"]) < 2: return False
                        tup = self.angleParser(1, slots["directions"])
                        if tup[1] == -1: return False
                        self.droid.roll_continuous(self.speed, tup[0])
                        return True
                    self.droid.stop_roll()

            speed = self.speed
            if "half" in slots["driveModifiers"]: speed = min(0.1, speed * 1/2)
            elif "twice" in slots["driveModifiers"]: speed = max(1, speed * 2)

            error = "There is some error in your driving instruction. Either you did not provide directions or you gave a combo cardinal direction (north-by-northeast) that did not make sense."

            i = 0
            while i < len(slots["directions"]):
                if slots["directions"][i] == "turn":
                    tup = self.angleParser(i+1, slots["directions"])
                    if tup[1] == -1:
                        print(error)
                        return False
                    i = tup[1]

                    self.droid.roll(speed, tup[0], 0)
                else:
                    if slots["directions"][i] == "go": i = i+1

                    tup = self.angleParser(i, slots["directions"])
                    if tup[1] == -1:
                        print(error)
                        return False
                    i = tup[1]

                    if slots["numValues"].empty() or ("seconds" not in slots["driveModifiers"] and "feet" not in slots["driveModifiers"]):
                        self.droid.roll(speed, tup[0], 1)
                    elif "seconds" in slots["driveModifiers"]:
                        self.droid.roll(speed, tup[0], slots["numValues"].get())
                    else:
                        self.droid.roll(speed, tup[0], slots["numValues"].get()*self.oneFootConstant/speed)
            return True
            
        return False

    def connectionParser(self, command):
        # slot filler for connections
        ################################################

        # connect - determines if this is a connection request, values = connect, disconnect
        # id - stores possible id of droid
        # percent - boolean to determine if we want to scan for nearby droids
        slots = {"connect": None, "id": None, "scan": False}

        ################################################

        if "disconnect" in command: slots["connect"] = "disconnect"
        elif "connect" in command: slots["connect"] = "connect"

        # maybe check if something like the word droid/robots is in play
        if "nearby" in command or ("are" in command and "other" in command): slots["scan"] = True

        index = command.find("-")
        if 2 <= index <= len(command) - 4:
            slots["id"] = command[index - 2: index + 5].upper()

        return self.connectionSlotsToActions(slots)

    def connectionSlotsToActions(self, slots):
        if slots["connect"] == "disconnect":
            if self.droid.connected_to_droid: self.disconnect()
            else: print("You are already disconnected from the server.")
            return True
        if slots["connect"] == "connect":
            rid = slots["id"]
            if not rid:
                print("You must enter a valid Droid id to connect.")
                return False
            success = self.droid.connect_to_droid(rid)
            if not success:
                print("You must enter a valid Droid id to connect.")
                return False
            return True
        if slots["scan"]:
            self.droid.scan()
            return True
        return False

    def stanceParser(self, command):
        # slot filler for stance
        ################################################

        # connect - determines if this command issues a stance change, values = bi, tri
        # waddle - boolean for waddle
        slots = {"stance": None, "waddle": False}

        ################################################

        if "biped" in command: slots["stance"] = "bi"
        elif "triped" in command: slots["stance"] = "tri"
        elif "third" in command and ("up" in command or ("on" in command and "stop" in command)): slots["stance"] = "bi"
        elif "third" in command and ("down" in command or "on" in command): slots["stance"] = "tri"

        if "stop" in command or "off" in command: slots["waddle"] = False
        elif "tiptoe" in command or "start" in command or "on" in command: slots["waddle"] = True

        return self.stanceSlotsToActions(slots)

    def stanceSlotsToActions(self, slots):
        if slots["stance"] == "bi":
            if self.droid.stance == 2: print("You are already in biped mode.")
            else:
                self.droid.set_stance(2)
                self.waddling = False
            return True
        elif slots["stance"] == "tri":
            if self.droid.stance == 1: print("You are already in triped mode.")
            else:
                self.droid.set_stance(1)
                self.waddling = False
            return True
        elif slots["waddle"]:
            if self.waddling: print("You are already waddling.")
            else:
                self.droid.set_waddle(True)
                self.droid.stance = 2
                self.waddling = True
            return True
        else: # assume bert understands correctly this is a stance command, must be a command to stop waddling
            if not self.waddling: print("You are not waddling currently.")
            else:
                self.droid.set_waddle(False)
                self.droid.stance = 2
                self.waddling = False
            return True


    # Parser for a animation command
    def animationParser(self, command):
        if re.search("fall", command):
            self.droid.animate(14)
            return True
        if re.search("(dance|move)", command):
            self.droid.animate(20)
            return True

        if re.search("(sing|sound|noise)", command):
            self.droid.play_sound(3)
            return True
        if re.search("laugh", command):
            self.droid.play_sound(random.choice([34, 37]))
            return True
        if re.search("scream", command):
            self.droid.play_sound(7)
            return True
        if re.search("alarm", command):
            self.droid.play_sound(random.choice([18, 19, 20, 21]))
            return True

        return False

    # Parser for a head command
    def headParser(self, command):
        if re.search("(forward|ahead|straight|front)", command):
            self.droid.rotate_head(0)
            return True
        if re.search("left", command):
            self.droid.rotate_head(-90)
            return True
        if re.search("right", command):
            self.droid.rotate_head(90)
            return True
        if re.search("(behind|back)", command):
            self.droid.rotate_head(180)
            return True
        if re.search("around", command):
            self.droid.animate(22)
            return True
        return False

    def prettyPrint(self, content, returnValue = True):
        print("****************************************")
        print(self.name + ": " + str(content))
        print("****************************************")
        return returnValue

    # Parser for a state command
    def stateParser(self, command):
        if re.search("color", command):
            if re.search("(front|forward)", command): self.prettyPrint("My front light rgb is: " + str(self.frontRGB))
            elif re.search("(back|rear)", command): self.prettyPrint("My back light rgb is: " + str(self.backRGB))
            else: self.prettyPrint("My front light rgb is:" + str(self.frontRGB) + "\nMy back light rgb is: " + str(self.backRGB))
            return True
        if re.search("(name|call)", command):
            if re.search("(want|wanna).*you", command) or re.search("is now", command):
                if self.extractName(command) == "":
                    self.prettyPrint("You didn't give me a name!")
                    self.droid.play_sound(7)
                    return False
                else: self.name = self.extractName(command)
            else: self.prettyPrint("My name is: " + self.name)
            return True
        if re.search("(stance|standing)", command):
            if self.droid.stance == 2: self.prettyPrint("I am in biped mode right now, standing on two feet.")
            else: self.prettyPrint("I am in triped mode right now, standing on three feet.")
            return True
        if re.search("awake", command):
            if self.droid.awake: self.prettyPrint("I'm alive!!!!!")
            else: self.prettyPrint("Shush, I'm sleeping.")
            return True
        if re.search("waddling", command):
            if self.waddling: self.prettyPrint("Yes, I am waddling right now, can you dance as well as me?")
            else: self.prettyPrint("No, I am not waddling right now.")
            return True
        if re.search("logic display", command):
            if re.search("off", command):
                if self.logicDisplayIntensity == 0: self.prettyPrint("Yes, my logic display is off.")
                else: self.prettyPrint("No, my logic display is on.")
            else:
                if self.logicDisplayIntensity > 0: self.prettyPrint("Yes, my logic display is on.")
                else: self.prettyPrint("No, my logic display is off.")
            return True
        if re.search("(holoemitter|holo emitter)", command):
            if re.search("off", command):
                if self.holoProjectorIntensity == 0: self.prettyPrint("Yes, my holoemitter is off.")
                else: self.prettyPrint("No, my holoemitter is on.")
            else:
                if self.holoProjectorIntensity > 0: self.prettyPrint("Yes, my holoemitter is on.")
                else: self.prettyPrint("No, my holoemitter is off.")
            return True
        if re.search("(power|battery)", command):
            print("****************************************")
            self.droid.battery()
            print("****************************************")
            return True
        if re.search("(fast|speed)", command): return self.prettyPrint("My current speed is: " + str(self.speed))
        if re.search("back", command):
            words = re.split('\W+', command)
            words = [x for x in words if x != ""]

            for word in words:
                if word in self.colorToRGB:
                    if self.backRGB == self.colorToRGB[word]: return self.prettyPrint("Yes, my back light is " + word + ".")
                    else: return self.prettyPrint("No, my back light is not " + word + ".")
            return False
        if re.search("front", command):
            words = re.split('\W+', command)
            words = [x for x in words if x != ""]

            for word in words:
                if word in self.colorToRGB:
                    if self.frontRGB == self.colorToRGB[word]: return self.prettyPrint("Yes, my front light is " + word + ".")
                    else: return self.prettyPrint("No, my front light is not " + word + ".")
            return False
        if re.search("(orientation|angle)", command): return self.prettyPrint("My angle is " + str(self.droid.angle) + ".")
        if re.search("(heading|direction)", command): return self.prettyPrint("My heading is " + str(self.droid.angle - self.heading) + ".")
        if re.search("driving", command):
            if self.droid.drive_mode: return self.prettyPrint("Yes, I am driving.")
            else: return self.prettyPrint("No, I am not driving.")
        return False

    def extractName(self, command):
        words = re.split("[^a-zA-Z]", command)
        ret = ""
        activated = False
        activated2 = False
        for word in words:
            if activated:
                ret += word + " "
            if word == "you":
                activated = True
            if activated2:
                if word == "now": activated = True
                else: activated2 = False
            if word == "is": activated2 = True
        if len(ret) > 0 and ret[-1] == " ":
            return ret.strip().capitalize()
        else:
            return ret

    # Parser for a grid command
    def gridParser(self, command):
        # Convert the words to lowercase
        # Convert numbers as words to ints
        # Remove duplicate spaces
        words = re.split("(x|[^a-zA-Z0-9])", command.lower())
        command = ""
        for word in words:
            try:
                command += str(w2n.word_to_num(word)) + " "
            except:
                command += word + " "
        command = re.sub(" +", " ", command)
        # print("****************************************")
        # print(command)
        # print("****************************************")

        if re.search("(\d+|to).*(x|by).*(\d+|to) grid", command):
            words = re.split("(x|[^a-zA-Z0-9])", command)
            coords = self.extractCoord(words)
            if len(coords) < 2: return self.prettyPrint("Not enough coordinates!", returnValue = False)

            x, y = coords
            self.grid = [["" for _ in range(y)] for _ in range(x)]
            self.G = Graph(self.grid)
            self.prettyPrintGrid(self.grid)
            return True
        elif re.search("(foot|feet)", command):
            if len(self.grid) == 0 or len(self.grid[0]) == 0: return self.prettyPrint("Grid is not initialized yet!", returnValue = False)

            words = re.split('[^\w.]+', command)
            words = [x for x in words if x != ""]

            value = None
            for word in words:
                if word in self.numDict: word = self.numDict[word]
                try:
                    value = float(word)
                except ValueError:
                    continue
            if not value: return self.prettyPrint("No grid size in feet stated!", returnValue = False)
            self.gridSize = value
            return True
        elif re.search("(not possible|impossible|cannot)", command):
            if len(self.grid) == 0 or len(self.grid[0]) == 0: return self.prettyPrint("Grid is not initialized yet!", returnValue = False)

            words = re.split("(x|[^a-zA-Z0-9])", command)
            coords = self.extractCoord(words, limit = 4)
            if len(coords) < 4: self.prettyPrint("Not enough coordinates!", returnValue = False)

            x, y, x2, y2 = coords
            self.G.neighborhood[(x, y)].discard((x2, y2))
            self.G.neighborhood[(x2, y2)].discard((x, y))
            return True
        elif re.search("you.*re.*(a|on).*(\d+|to).*(\d+|to)", command):
            if self.pos != (-1, -1):
                self.grid[self.pos[0]][self.pos[1]] = ""
            arr = re.split("[^a-zA-Z0-9]", command)
            coords = self.extractCoord(arr)
            if len(coords) < 2: self.prettyPrint("Not enough coordinates!", returnValue = False)

            x, y = coords

            # errors
            if len(self.grid) == 0 or len(self.grid[0]) == 0: return self.prettyPrint("Grid is not initialized yet!", returnValue = False)
            if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]): return self.prettyPrint("Coordinate is out of grid!", returnValue = False)

            self.pos = (x, y)
            self.objCoord["you"] = (x, y)
            self.prettyPrintGrid(self.grid)
            return True
        elif re.search("(s|re) .+ (at|to|on|above|below)", command):
            # Replace obj with its coordinates
            for obj in self.objCoord:
                words = re.split(" ", obj)
                for word in words:
                    if re.search(word, command):
                        x, y = self.objCoord[obj]
                        if re.search("(left|west)", command):
                            y -= 1
                        elif re.search("(right|east)", command):
                            y += 1
                        elif re.search("(below|south|bottom)", command):
                            x += 1
                        elif re.search("(above|north|top)", command):
                            x -= 1
                        command = self.replaceWithCoord(command, x, y)
                        self.prettyPrint(command)
                        break

            if re.search("at.*(\d+|to).*(\d+|to)", command):
                words = re.split("[^a-zA-Z0-9]", command)
                coords = self.extractCoord(words)
                if len(coords) < 2: return self.prettyPrint("Not enough coordinates!", returnValue = False)

                x, y = coords
                obj = self.extractObj(words)

                # errors
                if len(self.grid) == 0 or len(self.grid[0]) == 0: return self.prettyPrint("Grid is not initialized yet!", returnValue = False)
                if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]): return self.prettyPrint("Coordinate is out of grid!", returnValue = False)
                if obj == "": return self.prettyPrint("You didn't specify what the obstacle(s) is/are!", returnValue = False)

                self.grid[x][y] = obj
                u = (x, y)
                for v in self.G.neighbors(u):
                    self.G.neighborhood[v].discard(u)
                self.objCoord[obj] = (x, y)
                self.prettyPrintGrid(self.grid)
                return True
        elif re.search("go.*to", command):
            # Replace obj with its coordinates
            for obj in self.objCoord:
                words = re.split(" ", obj)
                for word in words:
                    if re.search(word, command):
                        x, y = self.objCoord[obj]
                        if re.search("(left|west)", command):
                            y -= 1
                        elif re.search("(right|east)", command):
                            y += 1
                        elif re.search("(below|south|bottom)", command):
                            x += 1
                        elif re.search("(above|north|top)", command):
                            x -= 1
                        command = "go to " + str(x) + " , " + str(y)
                        self.prettyPrint(command)
                        break
            if re.search("(\d+|to).*(\d+|to)", command):
                arr = re.split("[^a-zA-Z0-9]", command)
                coords = self.extractCoord(arr)
                if len(coords) < 2: return self.prettyPrint("Not enough coordinates!", returnValue = False)
                x, y = coords

                # errors
                if len(self.grid) == 0 or len(self.grid[0]) == 0: self.prettyPrint("Grid is not initialized yet!", returnValue = False)
                if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]): return self.prettyPrint("Coordinate is out of grid!", returnValue = False)
                if self.pos == (-1, -1): return self.prettyPrint("Current position hasn't been specified!", returnValue = False)
                if (x, y) in self.objCoord.values(): return self.prettyPrint("Impossible to get to the target! There is an object there!", returnValue = False)

                target = (x, y)
                if target == self.pos: return self.prettyPrint("You are already there!")

                self.prettyPrintGrid(self.grid, target)

                moves = A_star(self.G, self.pos, target, manhattan_distance_heuristic)
                if moves is None: return self.prettyPrint("Impossible to get to the target!", returnValue = False)
                else: self.prettyPrint(moves)
                for i in range(1, len(moves)):
                    # Move right
                    if moves[i][1] > moves[i - 1][1]:
                        with noStdOut(): self.droid.roll(self.speed, 90, self.gridSize*self.oneFootConstant/self.speed)
                    # Move left
                    elif moves[i][1] < moves[i - 1][1]:
                        with noStdOut(): self.droid.roll(self.speed, 270, self.gridSize*self.oneFootConstant/self.speed)
                    # Move down
                    elif moves[i][0] > moves[i - 1][0]:
                        with noStdOut(): self.droid.roll(self.speed, 180, self.gridSize*self.oneFootConstant/self.speed)
                    # Move up
                    elif moves[i][0] < moves[i - 1][0]:
                        with noStdOut(): self.droid.roll(self.speed, 0, self.gridSize*self.oneFootConstant/self.speed)
                self.pos = (x, y)
                self.objCoord["you"] = (x, y)
                self.prettyPrintGrid(self.grid)
                return True
        return False

    def prettyPrintGrid(self, grid, target = None):
        grid = copy.deepcopy(grid)

        if target:
            grid[target[0]][target[1]] = "target"

        if self.pos != (-1, -1):
            grid[self.pos[0]][self.pos[1]] = "you"

        print("****************************************")
        print("")
        for row in grid:
            strList = []
            for elem in row:
                if elem == "": elem = "x"
                strList.append(elem.capitalize().center(12))
            print("".join(strList))
            print("")
        print("****************************************")

    # Given a sentence as an array of words, extract the coordinate as an array of ints
    def extractCoord(self, words, limit = 2):
        ret = []
        middleTo = False
        for i in range(len(words) - 1, -1, -1):
            word = words[i]
            if word in self.numDict: word = self.numDict[word]
            if word.isdigit():
                ret = [int(word)] + ret
            if word in {"to", "too"}:
                if len(ret) != 2 or middleTo: 
                    ret = [2] + ret
                if len(ret) == 2:
                    middleTo = True
            if len(ret) == limit:
                break
        return ret

    # Given a sentence as an array of words, extract the object as a string
    def extractObj(self, words):
        ret = ""
        activated = False
        for word in words:
            if word == "at":
                activated = False
            if activated and word not in {"a", "an", "the"}:
                ret += word + " "
            if word in {"s", "re", "is", "are"}:
                activated = True
        if len(ret) > 0 and ret[-1] == " ":
            return ret[:-1]
        else:
            return ret

    # Replace obj with its coordinates
    def replaceWithCoord(self, command, x, y):
        words = re.split("[^a-zA-Z0-9]", command)
        ret = ""
        for word in words:
            if word not in {"above", "below", "to", "on"}:
                ret += word + " "
            else:
                break
        ret += "at " + str(x) + " , " + str(y)
        return ret