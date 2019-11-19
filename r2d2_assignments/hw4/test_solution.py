from gradescope_utils.autograder_utils.decorators import weight, visibility, partial_credit
import unittest
import numpy as np
import re
import r2d2_hw4 as X

def tokenize(sentence):
    words = re.findall(r"[\w]+", sentence)
    return [x.lower() for x in words]

def calcSentenceEmbeddingBaseline(sentence):
    words = tokenize(sentence)
    return X.vectors.query(words).sum(axis = 0)

def sentenceToEmbeddings(commandTypeToSentences):
    indexToSentence = {}

    i = 0
    for category in commandTypeToSentences:
        sentences = commandTypeToSentences[category]
        for sentence in sentences:
            indexToSentence[i] = (sentence, category)
            i += 1

    sentenceEmbeddings = np.zeros((len(indexToSentence), X.vectors.dim))

    for i in range(len(indexToSentence)):
        sentence = indexToSentence[i][0]
        sentenceEmbedding = calcSentenceEmbeddingBaseline(sentence)

        sentenceEmbeddings[i, :] = sentenceEmbedding

    return sentenceEmbeddings, indexToSentence

def accuracy():
    countTotal = 0
    countRight = 0
    testSentences = X.loadTrainingSentences("data/r2d2TestingSentences.txt")
    for category in testSentences:
        for sentence in testSentences[category]:
            countTotal += 1
            if X.getCategory(sentence, "data/r2d2TrainingSentences.txt") == category:
                countRight += 1

    return countRight / countTotal

trainingSentences = X.loadTrainingSentences("data/r2d2TrainingSentences.txt")
sentenceEmbeddings, indexToSentence = sentenceToEmbeddings(trainingSentences)

class TestSolution(unittest.TestCase):

############################################################
# Section 3: Intent Detection [65 points]
############################################################

# Section 3, Problem 1 [5 points]

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_tokenize_1(self):
        self.assertTrue(set(X.tokenize("  This is an example.  ")) == set(['this', 'is', 'an', 'example' ]))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_tokenize_2(self):
        self.assertTrue(set(X.tokenize("'Medium-rare,' she said.")) == set(['medium', 'rare', 'she', 'said']))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_tokenize_3(self):
        self.assertTrue(X.tokenize("REALLY?!") == ['really'])

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_tokenize_4(self):
        self.assertTrue(X.tokenize("") == [])

# Section 3, Problem 2 [5 points]

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_cosineSimilarity_1(self):
        self.assertAlmostEqual(X.cosineSimilarity(np.array([2, 0]), np.array([0, 1])), 0)

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_cosineSimilarity_2(self):
        self.assertEqual(X.cosineSimilarity(X.vectors.query("cat"), X.vectors.query("dog")), X.vectors.similarity("cat", "dog"))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_cosineSimilarity_3(self):
        self.assertAlmostEqual(X.cosineSimilarity(np.array([-1, 4, 5]), np.array([2, 3, 7])), 0.881844, delta = 0.000001)

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_cosineSimilarity_4(self):
        self.assertAlmostEqual(X.cosineSimilarity(np.array([2]), np.array([1])), 1, delta = 0.000001)

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_cosineSimilarity_5(self):
        self.assertAlmostEqual(X.cosineSimilarity(np.array([2, 4]), np.array([-4, -8])), -1, delta = 0.000001)

# Section 3, Problem 3 [5 points]

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_calcSentenceEmbeddingBaseline_1(self):
        self.assertTrue(np.allclose(X.calcSentenceEmbeddingBaseline("  This is an example.  "), calcSentenceEmbeddingBaseline("  This is an example.  ")))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_calcSentenceEmbeddingBaseline_2(self):
        self.assertTrue(np.array_equal(X.calcSentenceEmbeddingBaseline("    "), np.zeros(300)))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_calcSentenceEmbeddingBaseline_3(self):
        self.assertTrue(np.allclose(X.calcSentenceEmbeddingBaseline("Drive forward and turn left."), calcSentenceEmbeddingBaseline("Drive forward and turn left.")))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_calcSentenceEmbeddingBaseline_4(self):
        self.assertTrue(np.allclose(X.calcSentenceEmbeddingBaseline("REALLY?!"), calcSentenceEmbeddingBaseline("REALLY?!")))

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_calcSentenceEmbeddingBaseline_5(self):
        self.assertTrue(np.allclose(X.calcSentenceEmbeddingBaseline("I'm an apostrophe."), calcSentenceEmbeddingBaseline("I'm an apostrophe.")))

# Section 3, Problem 4 [10 points]

    @weight(1)
    @timeout_decorator.timeout(10)
    def test_sentenceToEmbeddings_1(self):
        self.assertEqual(X.sentenceToEmbeddings({})[0], sentenceToEmbeddings({})[0])
        self.assertEqual(X.sentenceToEmbeddings({})[1], sentenceToEmbeddings({})[1])

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_sentenceToEmbeddings_2(self):
        sentenceDictionary = {'unseenCommand': ["Become bipedal."]}

        self.assertTrue(np.allclose(X.sentenceToEmbeddings(sentenceDictionary)[0], sentenceToEmbeddings(sentenceDictionary)[0]))
        self.assertEqual(X.sentenceToEmbeddings(sentenceDictionary)[1], {0: ("Become bipedal.", 'unseenCommand')})

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_sentenceToEmbeddings_3(self):
        sentenceDictionary = {'state': ["What is your speed at this moment?"], 'head': ["Turn your head to the left."]}

        studentAnswer = X.sentenceToEmbeddings(sentenceDictionary)
        correctAnswer = sentenceToEmbeddings(sentenceDictionary)

        self.assertEqual(studentAnswer[0].shape, correctAnswer[0].shape)

        seenIndices = set()

        for i in range(studentAnswer[0].shape[0]):
            currentSentence = studentAnswer[0][i, :]
            foundSentence = False
            for j in range(correctAnswer[0].shape[0]):
                if j in seenIndices: continue
                if np.allclose(currentSentence, correctAnswer[0][j, :]):
                    if studentAnswer[1][i] == correctAnswer[1][j]:
                        seenIndices.add(j)
                        foundSentence = True
                        break
            self.assertTrue(foundSentence)

    @weight(5)
    @timeout_decorator.timeout(10)
    def test_sentenceToEmbeddings_4(self):
        studentAnswer = X.sentenceToEmbeddings(trainingSentences)

        self.assertEqual(studentAnswer[0].shape, sentenceEmbeddings.shape)

        seenIndices = set()

        for i in range(studentAnswer[0].shape[0]):
            currentSentence = studentAnswer[0][i, :]
            foundSentence = False
            for j in range(sentenceEmbeddings.shape[0]):
                if j in seenIndices: continue
                if np.allclose(currentSentence, sentenceEmbeddings[j, :]):
                    if studentAnswer[1][i] == indexToSentence[j]:
                        seenIndices.add(j)
                        foundSentence = True
                        break
            self.assertTrue(foundSentence)

# Section 3, Problem 5 [10 points]

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_closestSentence_1(self):
        self.assertEqual(X.closestSentence("Lights on.", sentenceEmbeddings), 32)

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_closestSentence_2(self):
        self.assertEqual(X.closestSentence("The chair was over there.", sentenceEmbeddings), 51)

    @weight(2)
    @timeout_decorator.timeout(10)
    def test_closestSentence_3(self):
        self.assertEqual(X.closestSentence("Drive in a forward direction.", sentenceEmbeddings), 23)

    @weight(4)
    @timeout_decorator.timeout(10)
    def test_closestSentence_4(self):
        x = np.zeros((2, 300))
        x[1, 50] = 1
        x[0, 49] = 1
        self.assertEqual(X.closestSentence("Can you test me.", x), 1)

# Section 3, Problem 6a [25 points]

    @partial_credit(25)
    @timeout_decorator.timeout(30)
    def test_getCategory(self, set_score=None):
        studentAccuracy = accuracy()
        score = round(max((min(15, studentAccuracy - 60)), 0) * 25/15)
        set_score(score)
        message = "getCategory test set accuracy: %g%%" % studentAccuracy
        print(message)

    @leaderboard("Test Set Score")
    def test_score(self, set_leaderboard_value = None):
        self.set_leaderboard_value(accuracy())

# Section 3, Problem 6b [5 points]

    @weight(5)
    @timeout_decorator.timeout(30)
    def test_accuracy(self):
        studentAccuracy = accuracy()
        self.assertEqual(X.accuracy("data/r2d2TrainingSentences.txt", "data/r2d2TestingSentences.txt"), studentAccuracy)

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
    def test_drivingParser(self):
        sentences = ["Increase your speed!", "Go forward, left, right, and then East.", "Go North and then South at California Boulevard", "Speed", 
        "Decrease how fast you are going", "Go backward at the next corner", "Don't increase your speed, decrease it!"]

        studentAnswers = [X.drivingParser(x) for x in sentences]

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

if __name__ == '__main__':
    unittest.main()