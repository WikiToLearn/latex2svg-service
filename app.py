from flask import Flask, render_template, request, jsonify
from urllib import parse

import uuid
import subprocess
import latex2mathml.converter

app = Flask("Latex 2 Svg")


@app.route("/", methods=["POST"])
def makeIndex():
    return render_json()

@app.route("/texvcinfo", methods=["POST"])
def texvcinfo():
    input_query = request.form['q']
    response = { "success": True,
            "checked": input_query,
            "requiredPackages":[],
            "identifiers": [""],
            "endsWithDot": False
        }
    return jsonify(response)
        
@app.route("/json", methods=["POST"])
def render_json():
    input_query = request.form['q']
    response = {
        "speakText": "bla bla bla",
        "svg": renderSVG(input_query),
        "mml": latex2mathml.converter.convert(input_query),
        "success": True,
        "log": "success",
        "sanetex": input_query
    }
    return jsonify(response)

@app.route("/mml", methods=["POST"])
def render_mml():
    input_query = request.form['q']
    return latex2mathml.converter.convert(input_query)

@app.route("/svg", methods=["POST"])
def render_svg():
    input_query = request.form['q']
    return renderSVG(input_query)

def renderSVG(formula):
    filename = str(uuid.uuid4());
    filenameTEX = filename + ".tex"
    filenamePDF = filename + ".pdf"
    filenameSVG = filename + ".svg"

    formula = formula.strip()

    latex = render_template("latex/document.tex", formula=formula)
    with open("/tmp/" + filename + ".tex", "w") as file:
        file.write(latex)

    subprocess.call(["pdflatex", "-output-directory", "/tmp", "/tmp/" + filenameTEX])
    subprocess.call(["pdfcrop", "/tmp/" + filenamePDF, "/tmp/" + filenamePDF])
    subprocess.call(["pdf2svg", "/tmp/" + filenamePDF, "/tmp/" + filenameSVG])
    
    with open("/tmp/" + filenameSVG) as f: 
        s = f.read()
    
    return s

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10044, debug=True)    
