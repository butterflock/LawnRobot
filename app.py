#!/usr/bin/env python
import argparse
import logging
import os
import time
import zipfile
from io import BytesIO

from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO

from control.AutomaticController import AutomaticController
from control.ManualController import ManualController
from perception import Perception
from processor.StoreFileProcessor import StoreFileProcessor
from processor.network_processor import NetworkProcessor
from util.connection_validator import ConnectionValidator

argparser = argparse.ArgumentParser()
argparser.add_argument("-t", "--test", default=False, action="store_true")
args = argparser.parse_args()

connection_validator = ConnectionValidator(disconnect_callback=lambda: disconnect())

perception = None

app = Flask(__name__)
socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if args.test:
    from control.TestDriveController import TestDriveController

    drive_controller = TestDriveController()
    network_processor = NetworkProcessor(None, update_callback=lambda update: socketio.emit("update", update))

else:
    from gpiozero import Buzzer

    buzzer = Buzzer(18)
    buzzer.on()
    time.sleep(0.25)
    buzzer.off()

    from control.ArduinoDriveController import ArduinoDriveController
    from control.safety_controller import SafetyController

    drive_controller = SafetyController(ArduinoDriveController(), buzzer)
    network_processor = NetworkProcessor(drive_controller,
                                         update_callback=lambda update: socketio.emit("update", update))

manual_controller = ManualController(drive_controller)

automatic_controller = AutomaticController(drive_controller, [network_processor])


def available_models():
    models = []
    for root, _, files in os.walk("models"):
        for file in files:
            if file.endswith(".tflite"):
                models.append(f"{root}/{file}")
    return sorted(models, reverse=True)


def available_recordings():
    return os.listdir("img")


@app.route('/')
def index():
    models = available_models()
    recordings = available_recordings()
    return render_template('index.html', models=models, recordings=recordings)


@app.route('/drive')
def drive():
    camera = request.args.get("camera")
    model = request.args.get("model")
    record = request.args.get("record")

    recordings_dir = None
    if record is not None:
        processor = StoreFileProcessor()
        automatic_controller.processors.append(processor)
        recordings_dir = processor.output_folder

    global perception
    if perception is not None:
        perception.shutdown()
    perception = Perception(camera, model)
    automatic_controller.start(perception)
    return render_template('drive.html', recordings_dir=recordings_dir)


@app.route('/img/<folder>')
def download_images(folder):
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        files = os.listdir(f"img/{folder}")
        for filename in files:
            with open(f"img/{folder}/{filename}", "rb") as file:
                data = zipfile.ZipInfo(filename)
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, file.read())
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename=f'{folder}.zip', as_attachment=True)


@socketio.on("connect")
def on_connect():
    print("Client connected")
    connection_validator.on_connect()


@socketio.on("command_start_automatic_drive")
def on_command_automatic_drive():
    print("Start Automatic Drive")
    automatic_controller.enable_automatic_drive()


@socketio.on("command_steer")
def on_command_steer(angle):
    manual_controller.exec_command_steer(angle)


@socketio.on("command_speed")
def on_command_speed(speed):
    manual_controller.exec_command_speed(float(speed) / 100)


@socketio.on("command_active")
def on_command_active(active):
    if active:
        automatic_controller.disable_automatic_drive()
    manual_controller.exec_command_active(active)


@socketio.on("alive_signal")
def on_alive_signal():
    connection_validator.on_alive_signal()


def disconnect():
    print('Client disconnected')
    automatic_controller.stop()


def start():
    socketio.run(app, host='0.0.0.0', port=80)


if __name__ == '__main__':
    start()
