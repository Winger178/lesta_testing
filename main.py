from flask import Flask, request, render_template, flash
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import math


app = Flask(__name__)

#чот хрень выходит пока что, надо узнать о Векторайзере
def process_text(text):
    documents = text.split('\n\n')
    documents = [doc.strip() for doc in documents if doc.strip()]

    count_vectorizer = CountVectorizer()
    count_matrix = count_vectorizer.fit_transform(documents)
    tf_array = count_matrix.toarray()
    feature_names = count_vectorizer.get_feature_names_out()

    tf = tf_array.sum(axis=0)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(documents)
    idf = tfidf_vectorizer.idf_



    return feature_names, tf, idf


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('Не прогрузился файл(')



    file = request.files['file']

    if file.filename == '':
        print('Не выбрали файл(')


    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        feature_names, tf, idf = process_text(content)

        df = pd.DataFrame({
            'слово': feature_names,
            'tf': tf,
            'idf': idf
        })


        result = df.sort_values(by='idf', ascending=False).head(50)
        df_to_html = result.to_html(classes='table table-striped', index=False)
        try:

            return render_template('result.html', tfidf_data=df_to_html)

        except:
            return render_template('error_db.html')
    return render_template('all_errors.html')


if __name__ == '__main__':
    app.run(debug=True)