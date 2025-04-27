from flask import Flask, request, render_template, flash, url_for, redirect

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


app = Flask(__name__)
app.config['SECRET_KEY'] = "N1F2F9DCidfqrf100"





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



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'file' in request.files:
            file = request.files['file']

            if file.filename != '':

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

                        return render_template('index.html', tfidf_data=df_to_html)

                    except:
                        pass #сюда лучше воткнуть обработку db соединения, если мы хотим реализовать историю обработок док-ов
                else:
                    print('Выбран файл неправильного формата(')
                    flash('Обработать возможно только .txt файл!!')
            else:
                print('Не выбрали файл(')
                flash("Вы не выбрали файл!")
        else:
            print('Не прогрузился файл(')
            flash('Файл не прогрузился!!')

        #этот ретерн для ловли флеш-сообщений
        return render_template('index.html')

    #этот ретерн для GET-запроса
    else:
        return render_template('index.html')

#чисто заглушки для ловли вских ошибок
@app.route("/all_errors/<int:error_code>")
def all_errors(error_code):
    return render_template('all_errors.html', error_data=error_code)

@app.after_request
def redirect_to_start(response):
    #можно для каждоцй ошибки добавить еще текст, из-за чего она произошла
    if response.status_code >= 400:
        print(response.status_code)
        return redirect(url_for('all_errors', error_code=response.status_code))
    return response


if __name__ == '__main__':
    app.run(debug=False)