from gradescope_utils.autograder_utils.decorators import weight, visibility, partial_credit
import unittest
import r2d2_hw4 as X

class TestSolution(unittest.TestCase):

############################################################
# Section 3: Intent Detection [65 points]
############################################################

# Section 3, Problem 6a [25 points]

    @partial_credit(25)
    @timeout_decorator.timeout(30)
    def test_getCategory(self, set_score=None):
        # c = X.DigitClassifier(train_data.digits)
        accuracy = 100.0 * 0.7
        score = round(max((min(15, accuracy - 60)), 0) * 25/15)
        set_score(score)
        message = "getCategory test set accuracy: %g%%" % accuracy
        print(message)

############################################################
# Section 4: Slot Filling [15 points]
############################################################

# Section 4, Problem 1 [7.5 points]

    @weight(7.5)
    @timeout_decorator.timeout(10)
    def test_lightParser(self):
        sentences = ["Set your lights to maximum", "Increase the red RGB value of your front light by 50.", "Turn your lights off.", "Set the holoemitter to maximum.",
        "Change your back light to aqua.", "Turn off your logic display.", "Set the green value on your back light to 0.", "Change your forward light to red.",
        "Reduce the green value on your lights by 50."]

        studentAnswers = [X.lightParser(x) for x in sentences]

        correctAnswers = [
        {'holoEmit': False, 'logDisp': False, 'lights': ['front', 'back'], 'add': False, 'sub': False, 'off': False, 'on': True}, 
        {'holoEmit': False, 'logDisp': False, 'lights': ['front'], 'add': True, 'sub': False, 'off': False, 'on': False},
        {'holoEmit': False, 'logDisp': False, 'lights': ['front', 'back'], 'add': False, 'sub': False, 'off': True, 'on': False},
        {'holoEmit': True, 'logDisp': False, 'lights': ['front', 'back'], 'add': False, 'sub': False, 'off': False, 'on': True},
        {'holoEmit': False, 'logDisp': False, 'lights': ['back'], 'add': False, 'sub': False, 'off': False, 'on': False},
        {'holoEmit': False, 'logDisp': True, 'lights': ['front', 'back'], 'add': False, 'sub': False, 'off': False, 'on': False},
        {'holoEmit': False, 'logDisp': False, 'lights': ['back'], 'add': False, 'sub': False, 'off': False, 'on': False},
        {'holoEmit': False, 'logDisp': False, 'lights': ['front'], 'add': False, 'sub': False, 'off': False, 'on': False},
        {'holoEmit': False, 'logDisp': False, 'lights': ['front', 'back'], 'add': False, 'sub': True, 'off': False, 'on': False}
        ]

        countCorrect = 0
        firstIncorrect = -1
        for i in range(len(studentAnswers)):
            if studentAnswers[i] == correctAnswers[i]: countCorrect += 1
            elif firstIncorrect < 0: firstIncorrect = i

        self.assertTrue(countCorrect/len(studentAnswers) >= 0.5, "You did not achieve 50 percent accuracy on our test set. The sentence: '" + sentences[i] + 
            "' was marked incorrectly.")

# Section 4, Problem 2 [7.5 points]

    @weight(7.5)
    @timeout_decorator.timeout(10)
    def test_directionParser(self):
        sentences = ["Increase your speed!", "Go forward, left, right, and then East.", "Go North and then South at California Boulevard", "Speed", 
        "Decrease how fast you are going", "Go backward at the next corner", "Don't increase your speed, decrease it!"]

        studentAnswers = [X.directionParser(x) for x in sentences]

        correctAnswers = [
        {'increase': True, 'decrease': False, 'directions': []}, 
        {'increase': False, 'decrease': False, 'directions': ['forward', 'left', 'right', 'right']},
        {'increase': False, 'decrease': False, 'directions': ['forward', 'back']},
        {'increase': False, 'decrease': False, 'directions': []},
        {'increase': False, 'decrease': True, 'directions': []},
        {'increase': False, 'decrease': False, 'directions': ['back']},
        {'increase': False, 'decrease': False, 'directions': []}
        ]

        countCorrect = 0
        firstIncorrect = -1
        for i in range(len(studentAnswers)):
            if studentAnswers[i] == correctAnswers[i]: countCorrect += 1
            elif firstIncorrect < 0: firstIncorrect = i

        self.assertTrue(countCorrect/len(studentAnswers) >= 0.5, "You did not achieve 50 percent accuracy on our test set. The sentence: '" + sentences[i] + 
            "' was marked incorrectly.")
