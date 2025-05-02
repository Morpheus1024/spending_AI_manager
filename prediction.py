from google_sheet_API import Transaction
from dotenv import load_dotenv
import json
import os

import fasttext
import numpy as np
import fasttext.util

working_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

class Prediction_model():
    def __init__(self):
        
        fasttext.util.download_model('pl', if_exists='ignore')
        self.model = fasttext.load_model('cc.pl.300.bin')
        self.category_config_path = os.getenv('CATEGORY_FILE')
        self.categories = []
        self.load_categories
        
    
    def load_categories(self):
        with open(self.category_config_path, 'r') as f:
            data = json.load(f)
            self.categories = data['categories']
            
    def predict_category(self, transaction: Transaction):
        pass
    
    def test_model(self):    
        description = "Kawa"
        #match description to category
        # Make sure categories are loaded
        if not self.categories:
            self.load_categories()

        # Get the embedding for the description
        description_embedding = self.model.get_sentence_vector(description)

        # Find the closest category
        best_match = None
        best_score = -1.0

        for category in self.categories:
            # Handle different category formats (string or dict)
            category_name = category if isinstance(category, str) else category.get('name', '')
            print(f"Category: {category_name}")
            
            # Get embedding for category
            category_embedding = self.model.get_sentence_vector(category_name)
            print(f"Category embedding: {category_embedding}")
            
            # Calculate cosine similarity
            similarity = np.dot(description_embedding, category_embedding) / (
                np.linalg.norm(description_embedding) * np.linalg.norm(category_embedding)
            )
            print(f"Similarity: {similarity}")
            
            if similarity > best_score:
                best_score = similarity
                best_match = category_name

        print(f"Description: '{description}'")
        print(f"Best matching category: '{best_match}' with similarity score: {best_score:.4f}")
        
        
        
        
        
if __name__ == "__main__":
    model = Prediction_model()
    model.test_model()
