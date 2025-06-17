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
PATH_exe = os.path.join (CURRENT_DIR, 'PeakSearch')
PATH_log = os.path.join (CURRENT_DIR, 'LOG_PEAKSEARCH.txt')

app = Flask(__name__)

@app.route("/run_cpp", methods = ["POST"])
def run_cpp_with_cntl():
    if os.path.exists (PATH_param): os.remove (PATH_param)
    if os.path.exists (PATH_hist): os.remove (PATH_hist)
    if os.path.exists (PATH_out): os.remove (PATH_out)
    if os.path.exists (PATH_log): os.remove (PATH_log)

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

@app.route ('/log_file', methods = ['POST'])
def log_file ():
    if os.path.exists (PATH_log):
        return send_file (PATH_log, as_attachment = True), 200
    else:
        return jsonify ({'error' : '送信ファイルがありません'}), 500

@app.route("/", methods=["GET"])
def root():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.methods} {rule.rule}")
    return "<br>".join(routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000, debug = False)
