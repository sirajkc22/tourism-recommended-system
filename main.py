from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df = pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
location=pickle.load(open('location.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__,template_folder='template')

@app.route('/')
def index():
    return render_template('index.html',
                           destination=list(popular_df['destination'].values),
                           city=list(popular_df['city'].values),
                           image=list(popular_df['Image-URL'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = location[location['destination'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('destination')['destination'].values))
        item.extend(list(temp_df.drop_duplicates('destination')['city'].values))
        item.extend(list(temp_df.drop_duplicates('destination')['Image-URL'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)