from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": {"Access-Control-Allow-Origin"}}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/house_price_model', methods=['POST'])
@cross_origin(origin='*', headers=['content-type'])
def house_price_model():
    if request.method == 'POST':
        data = request.files.get('data')
        df = pd.read_csv(data)

        X = df.drop('price', axis=1)
        y = df['price']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)

        filename = 'house_price_model.sav'
        pickle.dump(model, open(filename, 'wb'))

        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(X_test)

        return jsonify({'model': filename, 'predictions': y_pred.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
