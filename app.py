from flask import Flask, render_template, request
from urllib import parse

import uuid
import subprocess

app = Flask("Latex 2 Svg")

@app.route("/")
def makeIndex():
    return render_template("html/index.html")

@app.route("/render/<formula>")
def renderGET(formula):
    formula = parse.unquote(formula)
    return renderFormula(formula)

@app.route("/renderPOST", methods=['POST'])
def renderPOST():
    return renderFormula(request.json['formula'])

def renderFormula(formula):
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
    app.run(host='0.0.0.0', debug=True)    
