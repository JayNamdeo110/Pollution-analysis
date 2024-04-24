from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_diagnostic_analysis(file_path):
    df = pd.read_csv(file_path)
    X = df[['CO']].values.reshape(-1, 1)  
    y = df[['Result']].values.reshape(-1, 1)  
    
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)
    
    return predictions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnostic', methods=['GET', 'POST'])
def diagnostic():
    if request.method == 'POST':
        if 'data_file' not in request.files:
            return "No file part"
        
        uploaded_file = request.files['data_file']
        
        if uploaded_file.filename == '':
            return "No selected file"
        
        if uploaded_file and allowed_file(uploaded_file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            
            predictions = perform_diagnostic_analysis(file_path)
            
            os.remove(file_path)
            
            return render_template('diagnostic_result.html', predictions=predictions)
        else:
            return "Invalid file format or file not allowed"
    else:
        return render_template('diagnostic.html')

if __name__ == '__main__':
    app.run(debug=True)
