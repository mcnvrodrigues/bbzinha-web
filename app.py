from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arquivos = request.files.getlist('files')
        dfs = []
        for arquivo in arquivos:
            filename = secure_filename(arquivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(filepath)
            df = pd.read_excel(filepath)
            dfs.append(df)
        df_consolidado = pd.concat(dfs)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'vendas.xlsx')
        df_consolidado.to_excel(output_path, index=False)
        return send_file(output_path, as_attachment=True)
    return render_template('index.html')
