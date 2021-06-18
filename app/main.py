import statistics
import os
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

device_dict = {}
output = {}

def check_reference(line):
    """Return Reference Values"""
    if line.startswith('reference'):
        return True
    else:
        return False

# Add new devices here
def check_device(line):
    """Valid Device Types"""
    if line.startswith('thermometer'):
        return True
    elif line.startswith('humidity'):
        return True
    else:
        return False

# Each Devices needs a rule to return its status
def rule_validation(device_type, name, metrics, ref_temp, ref_humidity):
    """Determine Rules for Device types"""
    metrics = list(map(float, metrics))
    if device_type == "thermometer":
        return check_thermometer(metrics, ref_temp)
        
    elif device_type == "humidity":
        return check_humidity(metrics, ref_humidity)

def check_thermometer(metrics, ref_temp):
    mean = statistics.mean(metrics)
    deviation = statistics.pstdev(metrics)

    if (mean <= ref_temp + 0.5 and mean >= ref_temp - 0.5 ) and (deviation < 3):
        return "Ultra Precise"
    elif (mean <= ref_temp + 0.5 and mean >= ref_temp - 0.5 ) and (deviation < 5):
        return "Very Precise"
    else:
        return "Precise"

def check_humidity(metrics, ref_humidity):
    for metric in metrics:
        if (metric < ref_humidity - 1.0) or (metric > ref_humidity + 1.0):
            return "Discard"
    return "Keep"


@app.route("/")
def hello():
    return "Hello World from Flask"

@app.route("/process", methods=['POST'])
def process():
    file = request.files['file']
    filename=secure_filename(file.filename)
    file.save(filename)

    with open(filename) as f:
        metrics_list = [line.rstrip('\n') for line in f]
        for line in metrics_list:
            if check_reference(line):
                _, ref_temp, ref_humidity = line.split()
                continue
            if check_device(line):
                type, name = line.split()
                metrics = device_dict.setdefault(type, {}).setdefault(name, [])
                continue
            date, metric = line.split()
            metrics.append(metric)

    for device_type in device_dict:
        devices = device_dict[device_type]
        for device in devices:
            output[device] = rule_validation(device_type, device, devices[device], float(ref_temp), float(ref_humidity))


    return output
