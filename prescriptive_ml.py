from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prescriptive', methods=['GET', 'POST'])
def prescriptive_analysis():
    if request.method == 'POST':
        if 'data_file' not in request.files:
            return "No file part"
        file = request.files['data_file']
        if file.filename == '':
            return "No selected file"
        
        data = pd.read_csv(file)
        
        X = data[['feature1', 'feature2', 'feature3']]  
        y = data['target']
        
        model = LinearRegression()
        model.fit(X, y)
        
        prediction = model.predict(X.head())
        
        result = {'prediction': prediction}
        return render_template('prescriptive_result.html', result=result)
    
    return render_template('prescriptive.html')

if __name__ == '__main__':
    app.run(debug=True)
