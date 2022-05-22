from flask import Flask, render_template, request, g, session
import os
from modules import grammar as gmAPI
from modules import assembly as asmAPI

app = Flask(__name__)

@app.route("/")
def home(): 
    return render_template("index.html")

@app.route('/uploadsuccess', methods=['GET','POST'])
def uploadsuccess():
    if request.method == 'POST':
        file = request.files['myfile']
        filename = file.filename
        file.save(os.path.join('static',filename))
        file_path = os.path.join('..','static',filename)
        with open('./static/data/data.txt', 'w') as f:
            f.write(filename); f.write('\n')
            f.write(file_path); f.write('\n')
        return render_template("uploaded.html", file_name = filename, file_path=file_path) 

@app.route('/processing', methods=['GET','POST'])
def processing():
    if request.method == 'POST':
        with open('./static/data/data.txt', 'r') as f:
            lines = f.readlines()
        filename, file_path = lines[0].rstrip(), lines[1].rstrip()
        if len(lines) == 2:
            asm = asmAPI.Assembly()
            assembly_out = asm.convert_file(os.path.join('static',filename))
            with open('./static/data/data.txt', 'a') as f:
                f.write(assembly_out); f.write('\n')
            return render_template("assembly.html", file_name = filename,
                                    file_path=file_path, assembly_out=" "+assembly_out)
        else:
            assembly_out = lines[2].rstrip()
            gm = gmAPI.Grammar()
            grammar_out = gm.check(assembly_out)
            print(assembly_out, grammar_out)
            if assembly_out == grammar_out:
                status = " All looks good!"
                start = "None!"
                changed = end = ''
            else:
                status = " Needs Improvement."
                flag = False
                start = changed = end = ''
                i = j = 0
                while(i < len(grammar_out)):
                    if grammar_out[i] == assembly_out[j]:
                        if not flag: start += grammar_out[i]
                        else: end += grammar_out[i]
                        i += 1
                        j += 1
                    else:
                        changed += grammar_out[i]
                        flag = True
                        i += 1
                if changed[-1] == ' ': 
                    changed = changed[:-1]
                    end = ' '+end
                    
            
            return render_template("grammar.html", file_name = filename,
                                    file_path=file_path, assembly_out=assembly_out, 
                                    status=status, start=start, changed=changed, end=end)

if __name__ == "__main__":
    app.run(debug=True)