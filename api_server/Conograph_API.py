# api_server.py
import shutil
from flask import Flask, request, send_file, jsonify
import subprocess
import os
import stat
from dataIO import read_cntl_inp_xml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
PATH_cntl = os.path.join (CURRENT_DIR, 'cntl.inp.xml')
PATH_param, PATH_hist, PATH_out =  read_cntl_inp_xml (PATH_cntl)
FOLDER_out = os.path.dirname (PATH_out)
if FOLDER_out is not None: os.makedirs (FOLDER_out, exist_ok = True)
#work = os.path.join (current_dir, 'work')
PATH_exe = os.path.join (CURRENT_DIR, 'PeakSearch')
#assert os.path.exists (work)
#assert os.path.exists (exePath)

app = Flask(__name__)

#@app.route('/parse_cntl', methods = ['POST'])
#def parse_cntl_file():
#    #assert 'file' in request.files
#    file = request.files['file']
#    #assert isinstance (file.name, str)
#    path = os.path.join (work, file.name)
#    file.save (path)
    #assert os.path.exists (path)
#    param_file, hist_file, _ = read_cntl_inp_xml (path)
#    ans = [param_file, hist_file]
#    return jsonify ({'required_files' : ans})

@app.route("/run_cpp", methods = ["POST"])
def run_cpp_with_cntl():
    #os.makedirs("work", exist_ok=True)
    #paths = []
    pathDict = {'xml' : PATH_param, 'dat' : PATH_hist,
                'histogramIgor' : PATH_hist}
    for key in request.files:
        f = request.files[key]
        fname = f.name
        suffix = fname.split('.')[-1]
        path = pathDict[suffix]
        path = os.path.join (CURRENT_DIR, path)
        f.save(path)
    
    if not os.access (PATH_exe, os.X_OK):
       os.chmod(PATH_exe, os.stat (PATH_exe).st_mode | stat.S_IEXEC)
    result = subprocess.run([PATH_exe],
                    capture_output=True, text=True)
    #result = subprocess.run('PeakSearch.exe')
    

    if os.path.exists (PATH_out):
        return send_file(PATH_out, as_attachment = True), 200
    else:
        return jsonify({"error": "出力ファイルがありません"}), 500

@app.route("/", methods=["GET"])
def root():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.methods} {rule.rule}")
    return "<br>".join(routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000, debug = False)
