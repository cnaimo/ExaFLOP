from flask import Flask, request
import platform
import multiprocessing
import subprocess
from typing import Union
import nvgpu
import logging
import os
app = Flask(__name__)

is_working = False
default_venv_name = 'venv_server_node'
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def execute(cmd: Union[list, str]):
    if isinstance(cmd, str):
        cmd = [cmd]
    p = subprocess.Popen('', shell=True, stdout=subprocess.PIPE)
    for command in cmd:
        p.communicate(input=command.encode('utf-8'))
        for x in p.stdout:
            print(x.strip().decode('utf-8'))
        p.wait()
    if p.returncode != 0:
        print('oops')


def create_venv():
    os.system('python3 -m venv ' + default_venv_name)


def clear_uploads():
    logging.info("Cleared node_uploads directory")
    os.system('rm -rf "node_uploads"*; mkdir node_uploads')


@app.route('/is_node', methods=['GET'])
def is_node():
    return 'True'


@app.route('/info', methods=['GET'])
def info():
    data = {'Architecture': '', 'CPUopmodes': '', 'ByteOrder': '', 'CPUs': 0, 'OnlineCPUslist': '',
            'Threadspercore': 0, 'Corespersocket': 0, 'Sockets': 0, 'NUMAnodes': 0, 'VendorID': '',
            'CPUfamily': 0, 'Model': 0, 'Modelname': '', 'Stepping': 0, 'CPUMHz': 0, 'CPUmaxMHz': 0, 'CPUminMHz': 0,
            'BogoMIPS': 0, 'Virtualization': '', 'L1dcache': '', 'L1icache': '', 'L2cache': '', 'L3cache': '',
            'NUMAnode0CPUs': '', 'System': platform.system()}
    if data['System'] == 'Windows':
        data['CPUmaxMHz'] = 0
        data['CPUs'] = multiprocessing.cpu_count()
        data['Threadspercore'] = 0
    elif data['System'] == 'Linux':
        cpu_raw = (subprocess.check_output("lscpu", shell=True)).strip().decode()\
            .replace(' ', '').replace('(', '').replace(')', '').replace('-', '').split('\n')
        cpu_data = {}
        for x in cpu_raw:
            kv = x.split(':')
            if '.' in kv[1]:
                kv[1] = float(kv[1])
            else:
                try:
                    kv[1] = int(kv[1])
                except ValueError:
                    pass
            cpu_data[kv[0]] = kv[1]
        del cpu_data['Flags']
        data.update(cpu_data)

    gpu = nvgpu.gpu_info()
    data['GPUcount'] = len(gpu)
    gpu_type = []
    for i in range(len(gpu)):
        gpu_type.append(gpu[i]['type'])
    data['GPUtype'] = gpu_type
    return data


@app.route('/is_working', methods=['GET'])
def run():
    global is_working
    if is_working:
        return 'True'
    else:
        return 'False'


@app.route('/start_task', methods=['GET'])
def start_task():
    global is_working
    is_working = True
    return 'running...'


@app.route('/empty_venv', methods=['GET'])
def empty_venv():
    # uninstall all libraries
    global default_venv_name
    execute('./' + default_venv_name + '/bin/pip freeze | xargs ./' + default_venv_name + '/bin/pip uninstall -y')
    return 'Done'


@app.route('/list_venv_libraries', methods=['GET'])
def list_venv_libraries():
    data = (subprocess.check_output('./' + default_venv_name + '/bin/pip list --format=legacy', shell=True))\
        .strip().decode().replace(' ', '').replace('(', '\n').replace(')', '').split('\n')
    packages = {}
    i = 0
    while i < len(data):
        packages[data[i]] = data[i+1]
        i += 2
    return packages


@app.route('/install_requirements', methods=['POST'])
def install_requirements():
    print(list(request.files.keys()))
    if 'requirements.txt' not in list(request.files.keys()):
        return 'requirements.txt not in request', 400
    file = request.files['requirements.txt']
    file.save('uploads/requirements.txt')
    return 'Done'


@app.route('/upload', methods=['POST'])
def upload():
    for filename, file in request.files.items():
        os.makedirs(os.path.dirname('node_uploads/' + filename), exist_ok=True)
        file.save('node_uploads/' + filename)
    return 'Done'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if not os.path.isdir('node_uploads'):
        logging.info('Creating node_uploads directory')
        os.system('mkdir node_uploads')
    if not os.path.isdir(default_venv_name):
        logging.info('Creating venv: ' + default_venv_name)
        create_venv()
    app.run(host='0.0.0.0', port=5432, threaded=True)
