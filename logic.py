from sentiment_analysis_thesis_10th_april import load_models_from_joblib
from sentiment_analysis_thesis_10th_april import preprocessing
from sentiment_analysis_thesis_10th_april import preprocessing_text
from sentiment_analysis_thesis_10th_april import convertSingleToBOG
from sentiment_analysis_thesis_10th_april import convertToBOG
import joblib

def load_models_and_vectorizer():
    try:
        # Load the models from file
        path="best_models/best_models.joblib"

        models=load_models_from_joblib(path)

        # Load the vectorizer from file
        vectorizer = joblib.load('count_vectorizer.joblib')
        return models,vectorizer

    except:
        print("There was an error in uploading the models or vectorizer")

def predict_single_sentiment(x,name,models,vectorizer):

    x=preprocessing_text(x)
    x=convertSingleToBOG(x,vectorizer)
    return models[name].predict(x)

def predict_block_sentiment(x,name,models):
    x=preprocessing(x)
    x=convertToBOG(x)
    return models[name].predict(x)
