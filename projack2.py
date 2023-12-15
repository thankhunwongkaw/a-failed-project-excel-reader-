from flask import Flask , request , render_template , redirect , url_for
from werkzeug.utils import secure_filename
import pandas as pd
from pandas import read_excel
import datetime 
import os
import openpyxl
app = Flask(__name__)
@app.route('/')
def main():
    return render_template("cal.html")
@app.route("/get" , methods=["Post" ,"Get"])
def get():
    global df ,af
    file = request.files['file']
    name , extension = os.path.splitext(file.filename)
    op = request.form['option']
    #get file
    if extension in ['.xlsx' , '.xls']:
            af = pd.read_excel(request.files['file'])
            df =  af.head(0)
    else:
        return 'Allowed file types are .xlsx, .xls', 400
    if op =="count":
        return  render_template('select.html' , df=df) , 200
    else:
        return render_template("selmean.html" , df=df)

@app.route('/select' , methods=["post"])
def select():
    global df ,af
    e = request.form['name']
    res = af[e].value_counts().to_dict()
    return render_template("selfun.html" , res = res)   
    #return how many same value there are   
#@app.route("/mean" , methods=["post"])
#def mean():
#    global df,af
#    e =request.form["name"]
#    try:
#        mean = af.groupby(e).mean().to_dict()
#        return render_template("mean.html" , mean =mean)
#    except:
#        return 'please gave us excel file that has only one line of string and choose the string line :>'
@app.route("/mean", methods=["post"])
def mean():
    global df, af
    e = request.form["name"]
    #try:
        # Calculate mean without group names
    mean_data = af.groupby(e).mean()

        # Access individual values
    mean_values = {}
    for indicator in mean_data.index:
           mean_values[indicator] = mean_data[indicator]

        # Pass indicator and mean values to template
    return render_template("mean.html", mean_values=mean_values)
    #except:
        #return "please gave us excel file that has only one line of string and choose the string line :>"

if __name__ == '__main__':
    app.run(port=5287 , debug = True)
