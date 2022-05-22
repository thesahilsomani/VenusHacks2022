from flask import Flask, render_template, request, g, session
import os
import grammar as gmAPI
import assembly as asmAPI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/gotfile', methods=['GET','POST'])
def gotfile():
    if request.method == 'POST':
        file = request.files['myfile']
        filename = file.filename
        file.save(os.path.join('static',filename))
        file_path = os.path.join('..','static',filename)
        with open('data.txt', 'w') as f:
            f.write(filename); f.write('\n')
            f.write(file_path); f.write('\n')
        return render_template("processing.html", file_name = filename,
                                file_path=file_path, assembly_out='', grammar_out='') 

@app.route('/processing', methods=['GET','POST'])
def processing():
    if request.method == 'POST':
        with open('data.txt', 'r') as f:
            lines = f.readlines()
        filename, file_path = lines[0].rstrip(), lines[1].rstrip()
        if len(lines) == 2:
            asm = asmAPI.Assembly()
            assembly_out = asm.convert_file(os.path.join('static',filename))
            with open('data.txt', 'a') as f:
                f.write(assembly_out); f.write('\n')
            return render_template("processing.html", file_name = filename,
                                    file_path=file_path, assembly_out=assembly_out, 
                                    grammar_out='')
        else:
            assembly_out = lines[2].rstrip()
            gm = gmAPI.Grammar()
            grammar_out = gm.check(assembly_out)
            return render_template("processing.html", file_name = filename,
                                    file_path=file_path, assembly_out=assembly_out, 
                                    grammar_out=grammar_out)

if __name__ == "__main__":
    app.run(debug=True)