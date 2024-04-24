from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/descriptive', methods=['GET', 'POST'])
def descriptive_analysis():
    if request.method == 'POST':
        if 'data_file' not in request.files:
            return "No file part"
        file = request.files['data_file']
        if file.filename == '':
            return "No selected file"
        
        data = pd.read_csv(file)
        
        descriptive_stats = data.describe()
        
        descriptive_html = descriptive_stats.to_html(classes="table table-striped")
        return render_template('descriptive_result.html', descriptive_html=descriptive_html)
    
    return render_template('descriptive.html')

if __name__ == '__main__':
    app.run(debug=True)
