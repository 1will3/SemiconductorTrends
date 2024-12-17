import os

current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    exec(open(os.path.join(current_dir, "1DataCollectionV3.py")).read())
    exec(open(os.path.join(current_dir, "2TextPreprocessingV3.py")).read())
    exec(open(os.path.join(current_dir, "3SentimentAnalysisV3.py")).read())
    exec(open(os.path.join(current_dir, "4TopicModelingV3.py")).read())
    exec(open(os.path.join(current_dir, "5DataVisualizationV3.py")).read())