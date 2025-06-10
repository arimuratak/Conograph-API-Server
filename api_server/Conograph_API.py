# api_server.py
import shutil
from flask import Flask, request, send_file, jsonify
import subprocess
import os
from dataIO import read_cntl_inp_xml

current_dir = os.path.dirname(os.path.abspath(__file__))
work = os.path.join (current_dir, 'work')
exePath = os.path.join (work, 'PeakSearch')
assert os.path.exists (work)
assert os.path.exists (exePath)

app = Flask(__name__)

@app.route('/parse_cntl', methods = ['POST'])
def parse_cntl_file():
    reset_workspace (work)
    #assert 'file' in request.files
    file = request.files['file']
    #assert isinstance (file.name, str)
    path = os.path.join (work, file.name)
    file.save (path)
    #assert os.path.exists (path)
    param_file, hist_file, _ = read_cntl_inp_xml (path)
    ans = [param_file, hist_file]
    return jsonify ({'required_files' : ans})

def reset_workspace (workSpace):
    for fname in os.listdir (workSpace):
        if 'PeakSearch' in fname: continue
        #if 'PeakSearch.exe' in fname: continue

        path = os.path.join (workSpace, fname)
        
        if os.path.isdir (path):
            shutil.rmtree (path)
        else:
            os.remove (path)

@app.route("/run_cpp", methods = ["POST"])
def run_cpp_with_cntl():
    #os.makedirs("work", exist_ok=True)
    #paths = []
    for key in request.files:
        f = request.files[key]
        path = os.path.join(work, f.filename)
        #paths.append (path)
        f.save(path)

    cntlPath = os.path.join (work, 'cntl.inp.xml')
    _,_,out_path = read_cntl_inp_xml (cntlPath)
    out_path = os.path.join (work, out_path)
    out_folder = os.path.dirname (out_path)
    if out_folder is not None:
        os.makedirs (out_folder, exist_ok=True)

    #paramPath, histPath = paths
    #os.chdir (work)
    result = subprocess.run([exePath],
                    capture_output=True, text=True)
    #result = subprocess.run('PeakSearch.exe')
    #os.chdir (current_dir)
    

    if os.path.exists (out_path):
        return send_file(out_path, as_attachment = True), 200
    else:
        return jsonify({"error": "出力ファイルがありません"}), 500

@app.route("/", methods=["GET"])
def root():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.methods} {rule.rule}")
    return "<br>".join(routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000, debug = True)
