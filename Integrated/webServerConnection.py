import socketio



class webServerConnection:
    # Establish socket connection
    sio = socketio.Client()
    def __init__(self):
        self.sio.connect('//localhost:5000')


    @sio.event
    def connect():
        print('connection established')

    def connect(self):
       
        print('connection established')
    @sio.event
    def sensor_message(self, data):
        print('sending message of sensor data')
        self.sio.emit('sensor_data', {'Temperature': data[0], 'Pressure': data[1], 'Humidity': data[2], 'Light': data[3], 'Oxidised': data[4], 'Reduced': data[5], 'NH3': data[6]})
    
    @sio.event
    def image_message(self, image_data, markers):
        print('sending message of detection data')
        if(len(markers)>0):
            self.sio.emit("marker_detected", {"file":image_data.tobytes(), "marker": markers})
        else:
            if(image_data is not None):
                self.sio.emit("marker_detected", {"file":image_data.tobytes(), "marker": '0'})

    @sio.event
    def vision_message(self, data):
        print('sending message of sensor data')
        self.sio.emit('sensor_data', {'Temperature': data[0], 'Pressure': data[1], 'Humidity': data[2], 'Light': data[3], 'Oxidised': data[4], 'Reduced': data[5], 'NH3': data[6]})

    @sio.event
    def disconnect():
        print('disconnected from server')


