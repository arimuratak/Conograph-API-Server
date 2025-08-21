from flask import Flask, request, send_file, jsonify
import subprocess
import os
import stat
import xml.etree.ElementTree as ET

def read_cntl_inp_xml (path):
    # XMLファイルを読み込む
    tree = ET.parse(path)  # ファイル名を適宜変更
    root = tree.getroot()

    # 各要素の取得
    control_param = root.find('.//ControlParamFile')
    control_param_file = control_param.text.strip() if control_param is not None else None

    histogram_file = root.find('.//HistogramDataFile/FileName')
    histogram_file_name = histogram_file.text.strip() if histogram_file is not None else None

    outfile = root.find('.//Outfile')
    outfile_name = outfile.text.strip() if outfile is not None else None
    return control_param_file, histogram_file_name, outfile_name


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
PATH_cntl = os.path.join (CURRENT_DIR, 'cntl.inp.xml')
PATH_param, PATH_hist, PATH_out =  read_cntl_inp_xml (PATH_cntl)
FOLDER_out = os.path.dirname (PATH_out)
if FOLDER_out is not None: os.makedirs (FOLDER_out, exist_ok = True)
PATH_exe = os.path.join (CURRENT_DIR, 'PeakSearch')
PATH_log = os.path.join (CURRENT_DIR, 'LOG_PEAKSEARCH.txt')

if os.name == 'nt':
    PATH_exe = 'PeakSearch.exe'
else:
    PATH_exe = os.path.join (CURRENT_DIR, 'PeakSearch')
    if not os.access (PATH_exe, os.X_OK):
            os.chmod(PATH_exe, os.stat (PATH_exe).st_mode | stat.S_IEXEC)

app = Flask(__name__)

@app.route("/run_cpp", methods = ["POST"])
def run_cpp_with_cntl():
    if os.path.exists (PATH_param): os.remove (PATH_param)
    if os.path.exists (PATH_hist): os.remove (PATH_hist)
    if os.path.exists (PATH_out): os.remove (PATH_out)
    if os.path.exists (PATH_log): os.remove (PATH_log)

    pathDict = {'xml' : PATH_param, 'dat' : PATH_hist,
                'histogramigor' : PATH_hist}
    for key in request.files:
        f = request.files[key]
        fname = f.name
        suffix = fname.split('.')[-1].lower()
        path = pathDict[suffix]
        path = os.path.join (CURRENT_DIR, path)
        f.save(path)
    
    result = subprocess.run([PATH_exe])
    
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
