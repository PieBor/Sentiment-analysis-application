import unittest
import pandas as pd
from sentiment_analysis_thesis_30_march import preprocessing, convertToBOG, pipelines, grid_searches

class TestSentimentAnalysis(unittest.TestCase):
    
    # Test preprocessing function
    def test_preprocessing(self):
        test1 = pd.DataFrame({'text': ["This is a test.", "Another example!"]})
        expected_output = pd.DataFrame({'text': ["test", "another example"]})
        
        result = preprocessing(test1)
        pd.testing.assert_frame_equal(result, expected_output)

        test2 = pd.DataFrame({'text': ["I hate the ninja turtles! The world will be mine!"]})
        expected_output = pd.DataFrame({'text': ["hate ninja turtle world will mine"]})
        
        result = preprocessing(test2)
        pd.testing.assert_frame_equal(result, expected_output)
    
    # Test convertToBOG function
    def test_convertToBOG(self):
        test1 = pd.DataFrame({'text': ["this is a test", "another example"]})
        expected_output = [[1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]]

        X_bog = convertToBOG(test1)
        self.assertEqual(X_bog.tolist(), expected_output)  # Check if the converted output matches the expected output

        test2 = pd.DataFrame({'text': ["i want a pizza", "more pizza"]})
        expected_output = [[1, 1, 1, 1, 0], [0, 0, 0, 1, 1]]

        X_bog = convertToBOG(test2)
        self.assertEqual(X_bog.tolist(), expected_output)  # Check if the converted output matches the expected output
        

                
if __name__ == '__main__':
    unittest.main()
