from flask import Flask, request, jsonify, render_template
from collections import Counter
import sys

app = Flask(__name__)

# Список слов, которые нужно игнорировать
ignor_words = {
    'и', 'в', 'во', 'не', 'на', 'я', 'с', 'со', 'а', 'то', 'но', 'да',
    'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'от', 'о', 'из', 'ну',
    'ли', 'ни', 'до', 'уж', 'ей', 'они', 'тут', 'для', 'мы', 'их', 'чем',
    'под', 'ж', 'кто', 'мой', 'тот', 'об', 'про', 'им', 'или', 'нём', 'как'
}

def analyze_text(text):
    # Анализирует текст и возвращает статистику
    # Удаляем знаки препинания
    for char in '.,!?;:"()[]{}<>/*-+=—«»„“':
        text = text.replace(char, ' ')
    
    # Разбиваем на слова и приводим к нижнему регистру
    words = text.lower().split()
    
    # Убираем предлоги и короткие слова (меньше 2 букв)
    filtered_words = []
    for word in words:
        if word not in ignor_words and len(word) > 2:
            filtered_words.append(word)
    
    total_words = len(filtered_words)
    
    # Считаем частоту слов
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(10)
    
    # Формируем результат
    result_words = []
    for word, count in top_words:
        word_info = {
            "word": word,
            "count": count
        }
        result_words.append(word_info)
    
    return {
        "total_words": total_words,
        "top_words": result_words
    }
@app.route('/', methods=['GET', 'POST'])
def index():
    # Главная страница с формой
    if request.method == 'POST':
        text = request.form.get('text', '')
        
        if not text:
            return render_template('index.html', error="Текст не может быть пустым")
        
        result = analyze_text(text)
        result["server_port"] = request.environ.get('SERVER_PORT', 'unknown')
        
        return render_template('index.html', result=result)
    
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Эндпоинт для анализа текста
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "The text is required"}), 400
    
    text = data['text']
    
    if not text:
        return jsonify({"error": "The text cannot be empty"}), 400
    
    result = analyze_text(text)
    result["server_port"] = request.environ.get('SERVER_PORT', 'unknown')
    
    return jsonify(result), 200

@app.route('/health', methods=['GET'])
def health():
    # Эндпоинт для проверки состояния сервера
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    # Запускаем на порту 5000 по умолчанию
    # Для разных инстансов будем передавать порт как аргумент
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port, debug=False)