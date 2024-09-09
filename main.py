from flask import Flask, render_template, request,jsonify
import threading
from rs232 import rs232Comunication
from gpiosManager import GpiosManager
from MecanismLogic import Manager
from database.SqliteManager import SqliteManager

#from audioManager import AudioManager
app = Flask(__name__)
stop_event = threading.Event()

@app.route('/', methods=['GET', 'POST'])
def helloworld():
    result = None
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'ReadSensor':
            estado = gpios.ReadSensor()
            result = f'sensor: {estado}'
        elif operation == 'ReadFin':
            estado = gpios.ReadFinCarrera()
            result = f'sensor: {estado}'
        elif operation == 'generatePass':
            manager.generarPase()
            result = f'Pase generado'
        elif operation == 'TestCerradura1':
            result = gpios.testCerradura1()
        elif operation == 'TestCerradura2':
            result = gpios.testCerradura2()
        elif operation == 'TestLuzLed':
            result = gpios.testLuzLed()
        elif operation == 'TestSpecial':
            result = manager.generarEspecialPass()
        elif operation == 'ElectroImanOn':
            result == gpios.electroImanOn()
        elif operation == 'ElectroImanOff':
            result == gpios.electroImanOff()
        elif operation == 'TestearReles':
            result == gpios.testearReles()
        elif operation == 'ActuadorOff':
            result == gpios.specialDoorOff()
    return render_template('home.html', result=result)

@app.route('/api/rs232', methods=['GET', 'POST'])
def rs232_Api():
    if request.method == 'GET':
        operation = request.get_json()
        if operation['operation'] == "validations":
            return  jsonify({"validations":rs232.n_validations})
        return

@app.route('/api/mecanism', methods=['GET', 'POST'])
def mecanism_Api():
    if request.method == 'GET':
        params_mecanism = {
            "time_puerta_general":manager.time_puerta_general,
            "time_puerta_especial":manager.time_puerta_especial,
            "time_open_special":manager.time_open_special,
            "time_close_special":manager.time_close_special,
            "time_delay_turnstile":manager.time_delay_turnstile,
            "time_delay_special":manager.time_delay_special,
        }
        return jsonify({'result':params_mecanism})
    elif request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No se recibió JSON"}), 400
        if json_data['operation'] == 'ReadSensor':
            result = gpios.ReadSensor()
        elif json_data['operation'] == 'ReadFin':
            result = gpios.ReadFinCarrera()
        elif json_data['operation'] == 'generatePass':
            manager.generarPase()
            result = 'Pase Generado'
        elif json_data['operation'] == 'TestCerradura1':
            result = gpios.testCerradura1()
        elif json_data['operation'] == 'TestCerradura2':
            result = gpios.testCerradura2()
        elif json_data['operation'] == 'TestLuzLed':
            result = gpios.testLuzLed()
        elif json_data['operation'] == 'TestSpecial':
            result = manager.generarEspecialPass()
        elif json_data['operation'] == 'ElectroImanOn':
            result = gpios.electroImanOn()
        elif json_data['operation'] == 'ElectroImanOff':
            result = gpios.electroImanOff()
        elif json_data['operation'] == 'TestearReles':
            result = gpios.testearReles()
        elif json_data['operation'] == 'ActuadorOff':
            result = gpios.specialDoorOff()
        elif json_data['operation'] == 'OpenSpecial':
            gpios.specialDoorOpen()
            result = "puerta especial abriendose !!!!"
        elif json_data['operation'] == 'CloseSpecial':
            gpios.specialDoorClose()
            result = "puerta especial cerrandose !!!!"
        return jsonify({'result':result})
    else:
        return 'bad request!', 400
    





@app.route("/datos")
def datos():
    return rs232.getData()

if __name__ == "__main__":
    rs232 = rs232Comunication( stop_event=stop_event,com='/dev/ttyUSB0')
    manager = Manager(stop_event=stop_event,rs232=rs232) 
    
    # audio = AudioManager(stop_event=stop_event,rs232=rs232)
    gpios = GpiosManager()
    rs232.start()
    manager.start()
    # audio.start()
    try:
        app.run(host='0.0.0.0', port=5000,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()
        manager.join()
        # audio.join()
        print("programa terminado!")