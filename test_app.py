import unittest
import json
from app import app

class TestTextAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_empty_text(self):
        # Тест на пустой текст
        response = self.app.post('/analyze', 
                                json={"text": ""})
        self.assertEqual(response.status_code, 400)
    
    def test_missing_text_field(self):
        # Тест на отсутствие поля text
        response = self.app.post('/analyze', 
                                json={"message": "Привет"})
        self.assertEqual(response.status_code, 400)
    
    def test_word_count(self):
        # Тест подсчета слов
        response = self.app.post('/analyze', 
                                json={"text": "Привет, это Алина и Полина"})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_words'], 4)
    
    def test_top_words(self):
        # Тест определения самых частотных слов
        response = self.app.post('/analyze', 
                                json={"text": "Алина Полина Алина Полина Полина"})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_words'], 5)
        self.assertEqual(data['top_words'][0]['word'], 'полина')
        self.assertEqual(data['top_words'][0]['count'], 3)
        self.assertEqual(data['top_words'][1]['word'], 'алина')
        self.assertEqual(data['top_words'][1]['count'], 2)
    
    def test_health_endpoint(self):
        # Тест эндпоинта health
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()