from pymagnitude import *
from graph import *
from a_star import *
import random
import time
import csv
import re
import numpy as np
from r2d2_hw4 import *

from client import DroidClient

class Robot:
    def __init__(self, droidID, wordSimilarityCutoff, voice):
        self.embeddings = WordEmbeddings("Your Path Here: ") # Change the path
        self.createSentenceEmbeddings()
        self.droid = DroidClient()
        self.name = "R2"
        self.wordSimilarityCutoff = wordSimilarityCutoff
        self.holoProjectorIntensity = 0
        self.logicDisplayIntensity = 0
        self.frontRGB = (0, 0, 0)
        self.backRGB = (0, 0, 0)
        self.voice = voice
        self.grid = [[]]
        self.speed = 0.5
        self.pos = (-1, -1)
        self.happiness = 0 # from -1 to 1

        self.colorToRGB = {}
        with open('data/colors.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.colorToRGB[row[0]] = (int(row[2]), int(row[3]), int(row[4]))

        connected = self.droid.connect_to_droid(droidID)
        while not connected:
            connected = self.droid.connect_to_droid(droidID)

    def createSentenceEmbeddings(self):
        trainingSentences = loadTrainingSentences("data/r2d2TrainingSentences.txt")

        self.categories = [x for x in trainingSentences]

    def inputCommand(self, command):
        commandType = self.embeddings.getCategory(command, "data/r2d2TrainingSentences.txt")

        if "i like you" in command.lower():
            self.happiness = 1
            choice = random.choice([0, 1, 2, 3])
            if choice == 0: self.droid.play_sound(30)
            elif choice == 1: self.droid.animate(5)
            elif choice == 2: self.droid.play_sound(34)
            else: self.droid.animate(24)
            time.sleep(1)
        elif "i hate you" in command.lower():
            self.happiness = -1

        if commandType == "no" and not self.voice:
            subcommand = input(self.name + ": I could not understand your command. Do you want to add this command to the training set? (yes/no): ")
            if "yes" in subcommand.lower():
                subcommand = input("What category do you want to add it to? Choices are state, driving, light, animation, head, or grid: ")
                subcommand = subcommand.lower()
                if subcommand in self.categories:
                    with open("data/r2d2TrainingSentences.txt", 'a') as the_file:
                        the_file.write(subcommand + 'Sentences :: ' + command + '\n')
                    print("Command added. Changes will be present on restart.")
                else:
                    print(subcommand + " not a valid category.")
            else:
                self.happiness = max(-1, self.happiness - 0.1)
            return
        elif commandType == "no":
            self.happiness = max(-1, self.happiness - 0.1)
            subcommand = print(self.name + ": I could not understand your command.")
            self.commandNotUnderstood()
            return

        if self.happiness < 0:
            if random.random() < abs(self.happiness):
                print(self.name + ": I'm angry at you! I will not execute your "  + commandType + " command. (Say I like you to make me happy.)")
                self.droid.play_sound(random.choice([4, 12]))
                return
        result = getattr(self, commandType + "Parser")(command.lower())
        if result:
            print(self.name + ": Done executing "  + commandType + " command.")
            self.droid.play_sound(random.choice([20, 29]))
        else:
            print(self.name + ": I could not understand your " + commandType + " command.")
            self.happiness = max(-1, self.happiness - 0.1)
            self.commandNotUnderstood()

    def commandNotUnderstood(self):
        if self.happiness <= -0.8:
            self.droid.play_sound(7)
        elif self.happiness <= -0.6:
            self.droid.play_sound(2)
            time.sleep(1)
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
                    superDumbVariable = 1
            elif len(words) == 3:
                try:
                    color = (int(words[0]), int(words[1]), int(words[2]))
                except ValueError:
                    superDumbVariable = 1

        return color

    def lightParser(self, command):
        # slot filler for lights
        slots = {"holoEmit": False, "logDisp": False, "lights": [], "add": False, "sub": False,
        "percent": False, "whichRGB": [], "colors": [], "intensities": [], "rgb": False, "increment/seconds": False}

        solutionSlots = self.embeddings.lightParser(command)

        slots["holoEmit"] = solutionSlots["holoEmit"]
        slots["logDisp"] = solutionSlots["logDisp"]
        slots["lights"] = solutionSlots["lights"]
        slots["add"] = solutionSlots["add"]
        slots["sub"] = solutionSlots["sub"]
        if solutionSlots["off"]:
            slots["intensities"].append("off")
        if solutionSlots["on"]:
            slots["intensities"].append("on")

        if "dim" in command:
            slots["intensities"].append("dim")
        if "blink" in command:
            slots["intensities"].append("blink")

        if "%" in command:
            slots["percent"] = True

        if "red" in command:
            slots["whichRGB"].append("red")
        if "green" in command:
            slots["whichRGB"].append("green")
        if "blue" in command:
            slots["whichRGB"].append("blue")

        words = re.split('\W+', command)
        words = [x for x in words if x != ""]

        i = 0
        for word in words:
            if i < len(words) - 2:
                try:
                    slots["rgb"] = (int(words[i]), int(words[i+1]), int(words[i+2]))
                except ValueError:
                    superDumbVariable = True
            if self.embeddings.vectors.similarity("percent", word) > self.wordSimilarityCutoff:
                slots["percent"] = True
            if word in self.colorToRGB:
                slots["colors"].append(self.colorToRGB[word])
            i += 1

            try:
                increment = int(word)
                slots["increment/seconds"] = increment
            except ValueError:
                continue

        return self.lightSlotsToActions(slots)

    def lightSlotsToActions(self, slots):
        if slots["holoEmit"]:
            if "off" in slots["intensities"]:
                self.holoProjectorIntensity = 0
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "dim" in slots["intensities"]:
                self.holoProjectorIntensity = self.holoProjectorIntensity / 2
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "on" in slots["intensities"]:
                self.holoProjectorIntensity = 1
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            elif "blink" in slots["intensities"]:
                self.droid.set_holo_projector_intensity((self.holoProjectorIntensity + 1)%2)
                time.sleep(0.3)
                self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            else:
                return False
            return True

        if slots["logDisp"]:
            if "off" in slots["intensities"]:
                self.logicDisplayIntensity = 0
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "dim" in slots["intensities"]:
                self.logicDisplayIntensity = self.logicDisplayIntensity / 2
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "on" in slots["intensities"]:
                self.logicDisplayIntensity = 1
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            elif "blink" in slots["intensities"]:
                self.droid.set_logic_display_intensity((self.logicDisplayIntensity + 1)%2)
                time.sleep(0.3)
                self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            else:
                return False
            return True

        if (slots["add"] or slots["sub"]) and (slots["percent"]):
            lights = slots["lights"]

            if not slots["increment/seconds"]:
                if self.voice: return False
                command = input("Percent not found in command, please input percent to change by here: ")
                try:
                    command = command.replace("%", "")
                    slots["increment/seconds"] = int(command)
                except ValueError:
                    return False

            if slots["sub"]: slots["increment/seconds"] = -slots["increment/seconds"]

            percent = slots["increment/seconds"]

            if len(slots["whichRGB"]) == 0:
                command = input("Did not find what values (red/blue/green) to change, input what values to change: ")
                if "red" in command: slots["whichRGB"].append("red")
                if "green" in command: slots["whichRGB"].append("green")
                if "blue" in command: slots["whichRGB"].append("blue")

            if len(slots["whichRGB"]) == 0: return False

            if "red" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (max(0, min(rgb[0] + rgb[0]*percent/100, 255)), rgb[1], rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if "green" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], max(0, min(rgb[1] + rgb[1]*percent/100, 255)), rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if "blue" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], rgb[1], max(0, min(rgb[2] + rgb[2]*percent/100, 255))))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))

            return True

        if slots["add"] or slots["sub"]:
            lights = slots["lights"]

            if not slots["increment/seconds"]:
                if self.voice: return False
                command = input("Increment not found in command, please input amount to change by here: ")
                try:
                    slots["increment/seconds"] = int(command)
                except ValueError:
                    return False

            if slots["sub"]: slots["increment/seconds"] = -slots["increment/seconds"]

            increaseValue = slots["increment/seconds"]

            if len(slots["whichRGB"]) == 0:
                command = input("Did not find what values (red/blue/green) to change, input what values to change: ")
                if "red" in command: slots["whichRGB"].append("red")
                if "green" in command: slots["whichRGB"].append("green")
                if "blue" in command: slots["whichRGB"].append("blue")

            if len(slots["whichRGB"]) == 0: return False

            if "red" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (max(0, min(rgb[0] + increaseValue, 255)), rgb[1], rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if "green" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], max(0, min(rgb[1] + increaseValue, 255)), rgb[2]))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))
            if "blue" in slots["whichRGB"]:
                for light in lights:
                    rgb = getattr(self, light+"RGB")
                    setattr(self, light+"RGB", (rgb[0], rgb[1], max(0, min(rgb[2] + increaseValue, 255))))
                    getattr(self.droid, "set_"+light+"_LED_color")(*getattr(self, light+"RGB"))

            return True

        askedForColor = False

        if "back" in slots["lights"] and len(slots["lights"]) == 1:
            if len(slots["colors"]) > 1:
                seconds = slots["increment/seconds"]
                if not seconds: seconds = 1
                self.flash_colors(slots["colors"], seconds, False)
            elif len(slots["colors"]) == 1:
                self.backRGB = slots["colors"][0]
            else:
                if not slots["rgb"]:
                    color = self.askForColor("back")
                    askedForColor = True
                    if not color: return False
                    self.backRGB = color
                else:
                    self.backRGB = slots["rgb"]

            self.droid.set_back_LED_color(*self.backRGB)
            return True

        if ("front" in slots["lights"] and len(slots["lights"]) == 1) or len(slots["colors"]) > 1:
            if len(slots["colors"]) > 1:
                seconds = slots["increment/seconds"]
                if not seconds: seconds = 1
                self.flash_colors(slots["colors"], seconds)
            elif len(slots["colors"]) == 1:
                self.frontRGB = slots["colors"][0]
            else:
                if not slots["rgb"]:
                    color = self.askForColor("front")
                    askedForColor = True
                    if not color: return False
                    self.frontRGB = color
                else:
                    self.frontRGB = slots["rgb"]

            self.droid.set_front_LED_color(*self.frontRGB)
            return True

        if len(slots["colors"]) == 1:
            self.backRGB = slots["colors"][0]
            self.frontRGB = slots["colors"][0]
            self.droid.set_back_LED_color(*self.backRGB)
            self.droid.set_front_LED_color(*self.frontRGB)
            return True

        if len(slots["colors"]) == 0:
            if slots["rgb"]:
                self.backRGB = slots["rgb"]
                self.frontRGB = slots["rgb"]
                self.droid.set_back_LED_color(*self.backRGB)
                self.droid.set_front_LED_color(*self.frontRGB)
                return True

        if "off" in slots["intensities"]:
            self.holoProjectorIntensity = 0
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.logicDisplayIntensity = 0
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            self.backRGB = (0, 0, 0)
            self.frontRGB = (0, 0, 0)
            self.droid.set_back_LED_color(*self.backRGB)
            self.droid.set_front_LED_color(*self.frontRGB)
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
        elif "on" in slots["intensities"]:
            self.holoProjectorIntensity = 1
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.logicDisplayIntensity = 1
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)
            return True
        elif "blink" in slots["intensities"]:
            self.droid.set_holo_projector_intensity((self.holoProjectorIntensity + 1)%2)
            self.droid.set_logic_display_intensity((self.holoProjectorIntensity + 1)%2)
            time.sleep(0.3)
            self.droid.set_holo_projector_intensity(self.holoProjectorIntensity)
            self.droid.set_logic_display_intensity(self.logicDisplayIntensity)  
            return True

        if not slots["rgb"] and not askedForColor:
            color = self.askForColor()
            if color:
                self.backRGB = color
                self.frontRGB = color
                self.droid.set_back_LED_color(*self.backRGB)
                self.droid.set_front_LED_color(*self.frontRGB)
                return True

        return False

    def drivingParser(self, command):
        slots = {"increase": False, "decrease": False, "shape": [], "reverse": False,
        "percent": False, "directions": [], "increment/seconds": False, "speedModifier": []}

        solutionSlots = self.embeddings.drivingParser(command)

        slots["increase"] = solutionSlots["increase"]
        slots["decrease"] = solutionSlots["decrease"]
        slots["directions"] = solutionSlots["directions"]

        if re.search(r"\b(circle|donut)\b", command, re.I):
            slots["shape"].append("circle")
        if re.search(r"\b(square)\b", command, re.I):
            slots["shape"].append("square")
        if re.search(r"\b(counter)\b", command, re.I):
            slots["reverse"] = True

        if "half" in command:
            slots["speedModifier"].append("half")
        if "twice" in command or "two" in command:
            slots["speedModifier"].append("twice")

        if "%" in command:
            slots["percent"] = True

        words = re.split('\W+', command)
        words = [x for x in words if x != ""]

        for word in words:
            if self.embeddings.vectors.similarity("percent", word) > self.wordSimilarityCutoff:
                slots["percent"] = True
            try:
                increment = int(word)
                slots["increment/seconds"] = increment
            except ValueError:
                continue

        return self.drivingSlotsToActions(slots)

    def drivingSlotsToActions(self, slots):
        if "circle" in slots["shape"]:
            if slots["counter"]:
                for heading in range(360, 0, -30):
                    self.droid.roll(self.speed, heading % 360, 0.6)
            else:
                for heading in range(0, 360, 30):
                    self.droid.roll(self.speed, heading, 0.6)
            self.droid.roll(0, 0, 0)
            return True
        elif "square" in slots["shape"]:
            if slots["counter"]:
                for heading in range(360, 0, -90):
                    self.droid.roll(0, heading % 360, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed, heading % 360, 0.6)
            else:
                for heading in range(0, 360, 90):
                    self.droid.roll(0, heading, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed, heading, 0.6)
            self.droid.roll(0, 0, 0)
            return True
        elif slots["increase"] or slots["decrease"]:
            if slots["percent"] and slots["increment/seconds"]:
                if slots["increase"]:
                    self.speed = self.speed * (1 + slots["increment/seconds"]/100)
                elif slots["decrease"]:
                    self.speed = self.speed * (1 - slots["increment/seconds"]/100)
                else:
                    self.speed = self.speed * slots["increment/seconds"]/100
            elif slots["increase"]:
                if slots["increment/seconds"]:
                    self.speed += slots["increment/seconds"]
                self.speed += 0.25
            else:
                if slots["increment/seconds"]:
                    self.speed -= slots["increment/seconds"]
                self.speed -= 0.25
            return True
        else:
            flag = False
            tokens = slots["directions"]
            seconds = 0.6
            speedModifier = 1

            if "half" in slots["speedModifier"]:
                speedModifier = speedModifier / 2
            elif "twice" in slots["speedModifier"]:
                speedModifier = speedModifier * 2

            if slots["increment/seconds"]:
                seconds = slots["increment/seconds"]

            for token in tokens:
                if token in {"up", "forward", "ahead", "straight", "north"}:
                    self.droid.roll(0, 0, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed * speedModifier, 0, seconds)
                    flag = True
                elif token in {"down", "back", "south"}:
                    self.droid.roll(0, 180, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed * speedModifier, 180, seconds)
                    flag = True
                elif token in {"left", "west"}:
                    self.droid.roll(0, 270, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed * speedModifier, 270, seconds)
                    flag = True
                elif token in {"right", "east"}:
                    self.droid.roll(0, 90, 0)
                    time.sleep(0.35)
                    self.droid.roll(self.speed * speedModifier, 90, seconds)
                    flag = True
            self.droid.roll(0, 0, 0)
            return flag


    def animationParser(self, command):
        if re.search(r"\b(dance|move|moves)\b", command, re.I):
            self.droid.animate(3)
            return True
        elif re.search(r"\b(sing|sound|sounds|noise|noises)\b", command, re.I):
            self.droid.play_sound(3)
            return True
        elif re.search(r"\b(fall)\b", command, re.I):
            self.droid.animate(14)
            return True
        elif re.search(r"\b(scream)\b", command, re.I):
            self.droid.play_sound(7)
            return True
        return False

    def headParser(self, command):
        if re.search(r"\b(left)\b", command, re.I):
            self.droid.rotate_head(-90)
            return True
        elif re.search(r"\b(right)\b", command, re.I):
            self.droid.rotate_head(90)
            return True
        elif re.search(r"\b(behind|back)\b", command, re.I):
            self.droid.rotate_head(180)
            return True
        elif re.search(r"\b(forward|ahead)\b", command, re.I):
            self.droid.rotate_head(0)
            return True
        return False

    def gridParser(self, command):
        if re.search("\d+ (x|by) \d+", command):
            print
            arr = command.split()
            ind = -1
            for i in range(len(arr)):
                if arr[i] == "x" or arr[i] == "by":
                    ind = i
            if ind != -1 and ind < len(arr) - 1:
                x = int(arr[ind - 1])
                y = int(arr[ind + 1])
                self.grid = [["" for col in range(y)] for row in range(x)]
                self.droid.animate(1)
            print(self.grid)
            return True
        elif re.search("there is .+ at [(]?\d+,[ ]?\d+", command):
            temp = re.split("[^a-zA-Z0-9]", command)
            arr = []
            for x in temp:
                if x != "":
                    arr.append(x)
            ind1 = -1
            ind2 = -1
            for i in range(len(arr)):
                if arr[i] == "is":
                    ind1 = i
                elif arr[i].isdigit():
                    ind2 = i
                    break
            if ind1 != -1 and ind2 != -1:
                if int(arr[ind2]) < 0 or int(arr[ind2]) >= len(self.grid) or int(arr[ind2 + 1]) < 0 or int(arr[ind2 + 1]) >= len(self.grid[0]):
                    self.droid.play_sound(7)
                    return False
                else:
                    self.grid[int(arr[ind2])][int(arr[ind2 + 1])] = arr[ind1 + 1]
                    print(self.grid)
            return True
        elif re.search("go to [(]?\d+,[ ]?\d+", command):
            temp = re.split("[^a-zA-Z0-9]", command)
            arr = []
            for x in temp:
                if x != "":
                    arr.append(x)
            ind = -1
            for i in range(len(arr)):
                if arr[i].isdigit():
                    ind = i
                    break
            if ind != -1:
                if int(arr[ind]) < 0 or int(arr[ind]) >= len(self.grid) or int(arr[ind + 1]) < 0 or int(arr[ind + 1]) >= len(self.grid[0]):
                    self.droid.play_sound(7)
                    return False
                else:
                    target = (int(arr[ind]), int(arr[ind + 1]))
                    G = Graph(self.grid)
                    moves = A_star(G, self.pos, target, manhattan_distance_heuristic)
                    print("**************")
                    print(moves)
                    print("**************")
                    for i in range(1, len(moves)):
                        if moves[i][1] > moves[i - 1][1]:
                            self.droid.roll(0, 0, 0)
                            time.sleep(0.35)
                            self.droid.roll(1, 0, 0.62)
                        elif moves[i][1] < moves[i - 1][1]:
                            self.droid.roll(0, 180, 0)
                            time.sleep(0.35)
                            self.droid.roll(1, 180, 0.62)
                        elif moves[i][0] > moves[i - 1][0]:
                            self.droid.roll(0, 90, 0)
                            time.sleep(0.35)
                            self.droid.roll(1, 90, 0.62)
                        elif moves[i][0] < moves[i - 1][0]:
                            self.droid.roll(0, 270, 0)
                            time.sleep(0.35)
                            self.droid.roll(1, 270, 0.62)
                        self.pos = moves[i]
                        if self.pos == target:
                            break
                    self.reset()
                    self.pos = target
            return True
        elif re.search("you are at [(]?\d+,[ ]?\d+", command):
            temp = re.split("[^a-zA-Z0-9]", command)
            arr = []
            for x in temp:
                if x != "":
                    arr.append(x)
            ind = -1
            for i in range(len(arr)):
                if arr[i].isdigit():
                    ind = i
                    break
            if ind != -1:
                if int(arr[ind]) < 0 or int(arr[ind]) >= len(self.grid) or int(arr[ind + 1]) < 0 or int(arr[ind + 1]) >= len(self.grid[0]):
                    self.droid.play_sound(7)
                    return False
                else:
                    print(int(arr[ind]), int(arr[ind + 1]))
                    self.pos = (int(arr[ind]), int(arr[ind + 1]))
                    print(self.pos)
            return True
        return False

    def stateParser(self, command):
        if re.search(r"\b(color)\b", command, re.I):
            if re.search(r"\b(front|forward)\b", command, re.I):
                print("***************")
                print(self.frontRGB)
                print("***************")
            elif re.search(r"\b(back|rear)\b", command, re.I):
                print("***************")
                print(self.backRGB)
                print("***************")
            else:
                print("***************")
                print(self.frontRGB)
                print(self.backRGB)
                print("***************")
            return True
        elif re.search(r"\b(name)\b", command, re.I):
            print("***************")
            print(self.name)
            print("***************")
            return True
        elif re.search(r"\b(power|battery)\b", command, re.I):
            print("***************")
            self.droid.battery()
            print("***************")
            return True
        return False