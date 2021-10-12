import socketio


class webServerConnection:
    # Establish socket connection
    sio = socketio.Client()
    def __init__(self):
        self.connect()

    @sio.event
    def connect():
        self.sio.connect('http://172.19.28.216:5000')
        print('connection established')
    @sio.event
    def sensor_message(data):
        print('sending message of sensor data')
        self.sio.emit('sensor_data', {'Temperature': data[0], 'Pressure': data[1], 'Humidity': data[2], 'Light': data[3], 'Oxidised': data[4], 'Reduced': data[5], 'NH3': data[6]})

    @sio.event
    def vision_message(data):
        print('sending message of sensor data')
        self.sio.emit('sensor_data', {'Temperature': data[0], 'Pressure': data[1], 'Humidity': data[2], 'Light': data[3], 'Oxidised': data[4], 'Reduced': data[5], 'NH3': data[6]})

    @sio.event
    def disconnect():
        print('disconnected from server')


