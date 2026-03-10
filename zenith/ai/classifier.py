import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import sessionmaker
from zenith.db.models import get_engine, Dataset, Context

class ContextClassifier:
    def __init__(self, db_path='zenith.db', model_path='context_model.pkl'):
        self.db_path = db_path
        self.model_path = model_path
        self.pipeline = None
        
        engine = get_engine(self.db_path)
        self.Session = sessionmaker(bind=engine)
        self._load_or_init()
        
    def _load_or_init(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            # Create a basic pipeline
            self.pipeline = Pipeline([
                ('vectorizer', CountVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 2))),
                ('classifier', MultinomialNB())
            ])
            self._train_initial()

    def _train_initial(self):
        """Train on basic heuristics if no human data is provided yet."""
        initial_data = [
            ("Visual Studio Code", "Coding"),
            ("Spyder", "Coding"),
            ("StackOverflow - Google Chrome", "Coding"),
            ("GitHub - Mozilla Firefox", "Coding"),
            ("Zenith - main.py", "Coding"),
            ("YouTube - Google Chrome", "Entertainment"),
            ("Netflix", "Entertainment"),
            ("Spotify", "Entertainment"),
            ("Wikipedia - Research", "Research"),
            ("PDF Reader - Architecture Paper", "Research"),
            ("Word Document - Report", "Research")
        ]
        X, y = zip(*initial_data)
        self.pipeline.fit(X, y)
        self.save_model()
        
    def save_model(self):
        joblib.dump(self.pipeline, self.model_path)
        
    def train(self, window_title, context_label):
        """Add a single data point and retrain (for online learning)."""
        session = self.Session()
        session.add(Dataset(window_title=window_title, context_label=context_label))
        session.commit()
        
        # Pull all data and retrain
        all_data = session.query(Dataset).all()
        if all_data:
            X = [d.window_title for d in all_data]
            y = [d.context_label for d in all_data]
            
            # Simple fallback to partial_fit or fresh fit
            self.pipeline.fit(X, y)
            self.save_model()
        session.close()

    def predict(self, window_title):
        if not window_title or window_title == "[SYSTEM IDLE]":
            return "Idle"
        if hasattr(self.pipeline, 'classes_'):
            return self.pipeline.predict([window_title])[0]
        return "Unknown"

if __name__ == '__main__':
    classifier = ContextClassifier()
    test_titles = ["StackOverflow python list comprehension", "Watching random videos on YouTube"]
    for title in test_titles:
         print(f"'{title}' -> {classifier.predict(title)}")
