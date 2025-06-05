# api_server.py
from flask import Flask, request, send_file, jsonify
import subprocess
import os
from dataIO import read_cntl_inp_xml

current_dir = os.path.dirname(os.path.abspath(__file__))
work = os.path.join (current_dir, 'work')
exePath = os.path.join (work, 'PeakSearch.cpp')
assert os.path.exists (work)
assert os.path.exists (exePath)

app = Flask(__name__)

@app.route('/parse_cntl', methods = ['POST'])
def parse_cntl_file():
    assert 'file' in request.files
    file = request.files['file']
    assert file.name == 'cntl.imp.xml',  f"ファイル名が不正です: {file.filename}"
    path = os.path.join (work, file.name)
    file.save (path)
    assert os.path.exists (path)
    param_file, hist_file, _ = read_cntl_inp_xml (path)
    ans = [param_file, hist_file]
    return jsonify ({'required_files' : ans})

@app.route("/run_cpp", methods = ["POST"])
def run_cpp_with_cntl():
    #os.makedirs("work", exist_ok=True)

    for key in request.files:
        f = request.files[key]
        path = os.path.join(work, f.filename)
        f.save(path)

    result = subprocess.run(['./PeakSearch.cpp'],
                    capture_output=True, text=True)
    cntlPath = os.path.join (work, 'cntl.imp.xml')
    _,_,out_path = read_cntl_inp_xml (cntlPath)
    out_path = os.path.join (work, out_path)
    if os.path.exists (out_path):
        return send_file(out_path, as_attachment = True)
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
