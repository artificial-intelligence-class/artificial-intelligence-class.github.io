import unittest
from pymagnitude import *

class TestR2D2HW4(unittest.TestCase):
    @weight(0.5)
    @timeout_decorator.timeout(10)
    def cos_similarity(self):
        vectors = Magnitude("/Volumes/SD/hw4_2019/vectors/GoogleNews-vectors-negative300.magnitude")
        vector1 = vectors.query("cat")
        vector2 = vectors.query("dog")
        ret = cos_similarity(vector1, vector2)
        exp = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def cos_similarity(self):
        vectors = Magnitude("/Volumes/SD/hw4_2019/vectors/GoogleNews-vectors-negative300.magnitude")
        ret = calc_sentence_embedding("Go straight and come back")
        words = re.findall(r"[\w']+", "Go straight and come back")
        words = [word.lower() for word in words]
        exp = vectors.query(words).sum(axis = 0)
        self.assertTrue(ret == exp)
        
    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_light_parser1(self):
        ret = lightParser("Turn off the holoemitter.")
        exp = {"holoEmit": True, "logDisp": False, "lights": [], "add": False, "sub": False, "off": True, "on": False}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_light_parser2(self):
        ret = lightParser("Turn off all your lights.")
        exp = {"holoEmit": True, "logDisp": False, "lights": ["front", "back"], "add": False, "sub": False, "off": True, "on": False}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_light_parser2(self):
        ret = lightParser("Turn off all your lights.")
        exp = {"holoEmit": True, "logDisp": False, "lights": ["front", "back"], "add": False, "sub": False, "off": True, "on": False}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_direction_parser1(self):
        ret = directionParser("Increase your speed.")
        exp = {"increase": True, "decrease": False, "directions": []}
        self.assertTrue(ret == exp)
    
    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_direction_parser2(self):
        ret = directionParser("Run faster.")
        exp = {"increase": True, "decrease": False, "directions": []}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_direction_parser3(self):
        ret = directionParser("Decrease your speed")
        exp = {"increase": False, "decrease": True, "directions": []}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_direction_parser4(self):
        ret = directionParser("Slow down.")
        exp = {"increase": False, "decrease": True, "directions": []}
        self.assertTrue(ret == exp)

    @weight(0.5)
    @timeout_decorator.timeout(10)
    def test_direction_parser5(self):
        ret = directionParser("Go straight, turn left, then come back")
        exp = {"increase": False, "decrease": False, "directions": ["up", "left", "back"]}
        self.assertTrue(ret == exp)

if __name__ == "__main__":
    unittest.main()