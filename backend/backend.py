from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)
ASSEMBLER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Assembler.py'))
SIMULATOR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Simulator.py'))
WORK_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/assemble', methods=['POST'])
def assemble():
    data = request.get_json()
    code = data.get('code', '')
    input_path = os.path.join(WORK_DIR, 'input.txt')
    output_path = os.path.join(WORK_DIR, 'output.txt')
    try:
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(code)
        result = subprocess.run(['python', ASSEMBLER_PATH], cwd=WORK_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr or result.stdout or 'Assembly failed.'}), 400
        with open(output_path, 'r', encoding='utf-8') as f:
            machine_code = f.read()
        return jsonify({'machine_code': machine_code})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    machine_code = data.get('machine_code', '')
    siminput_path = os.path.join(WORK_DIR, 'siminput.txt')
    simoutput_path = os.path.join(WORK_DIR, 'simoutput.txt')
    try:
        with open(siminput_path, 'w', encoding='utf-8') as f:
            f.write(machine_code)
        result = subprocess.run(['python', SIMULATOR_PATH], cwd=WORK_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr or result.stdout or 'Simulation failed.'}), 400
        with open(simoutput_path, 'r', encoding='utf-8') as f:
            sim_output = f.read()
        return jsonify({'sim_output': sim_output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
