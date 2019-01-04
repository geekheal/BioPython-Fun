#!/usr/bin/python
from flask import Flask, render_template, url_for, request, jsonify, redirect
from App.methods import retrieve, preview, upload, get_files, global_record, comp

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    get_files()
    return render_template("index.html", files=global_record, prev="None")


@app.route('/query', methods=['POST'])
def db_query():
    if request.form["action"] == "query":
        db = request.form["database"]
        acc_num = request.form["id"]
        rettype = request.form["type"]
        retrieve(db, acc_num, rettype)
        return redirect(url_for("index"))
    elif request.form["action"] == "preview":
        db = request.form["database"]
        acc_num = request.form["id"]
        rettype = request.form["type"]
        result = preview(db, acc_num, rettype)
        return render_template("index.html", files=global_record, prev=result)


@app.route('/upload', methods=['POST'])
def file_upload():
    file_path = request.form["file"]
    db = request.form["database"]
    upload(file_path, db)
    return redirect(url_for("index"))


@app.route('/chart', methods=['POST'])
def show_chart():
    if request.form["action"] == "chart":
        title = request.form["charts"]
        file = request.form["filename"]
        file_type = request.form["filetype"]
        file_db = request.form["file"]
        if (title == "Nucleotide Composition") or (title == "Amino Acid Composition"):
            x_data, y_data = comp(file, file_type, file_db)
        else:
            x_data = [0]
            y_data = [0]
        return render_template("BioP_chart.html", title=title, file=file, x=x_data, y=y_data)
    elif request.form["action"] == "previous":
        return redirect(url_for("index"))
