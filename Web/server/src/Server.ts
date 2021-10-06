// Register aliases
import 'module-alias/register';

import path from 'path';
import multer from 'multer';
import express, { Request, Response } from 'express';
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

// Docs
import swaggerUI from 'swagger-ui-express';
import docs from './../swagger.json';

// Models
import Emitter from 'Models/Emitter';
import { play } from 'sound-play';

import SensorData from 'Models/Sensor';
import ImageData from 'Models/Image';

// ----------------------------------------------------------------------------------------
// Initialisation
// ----------------------------------------------------------------------------------------
const app = express(); // Init app
const server = createServer(app); // Create http server
const io = new Server(server, { cors: { origin: 'http://localhost:3000' } }); // Init sockets
const upload = multer();

// ----------------------------------------------------------------------------------------
// Setup middleware
// ----------------------------------------------------------------------------------------
app.use(express.static(path.join(__dirname, '../../client/build'))); // Serve static files
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/docs', swaggerUI.serve, swaggerUI.setup(docs));

// ----------------------------------------------------------------------------------------
// Configure sockets
// ----------------------------------------------------------------------------------------
io.on('connection', (socket: Socket) => {
	console.log(`User connected from ${socket.handshake.address}`);

	// const emitter = new Emitter(socket);

	// socket.on('pause', () => {
	// 	emitter.pause();
	// });

	// socket.on('play', () => {
	// 	emitter.play();
	// });

	socket.on('disconnect', () => {
		console.log(`User from ${socket.handshake.address} has disconnected`);
		// emitter.pause();
	});

	socket.on('marker_detected', function (data) {
		console.log(`Marker type detected: ${data.Type} ` + `File: ${data.File}`);
		const sound = require('sound-play');
		sound.play('Web/server/src/Assets/Marker_Alerts/trump_backpack_china.wav');
		io.sockets.emit('marker_detected', data);
	});

	socket.on('sensor_data', function (data) {
		console.log(
			`New Data: Gas: ${data.Gas}` +
				`, Humidity: ${data.Humidity} ` +
				`, Pressure: ${data.Pressure} ` +
				`, Temperature: ${data.Temperature}` +
				`, Light ${data.Lux}` +
				`, Noise: ${data.Noise}`,
		);
		io.sockets.emit('sensor_data', data);
	});
});

// ----------------------------------------------------------------------------------------
// Configure endpoints
// ----------------------------------------------------------------------------------------
/**
 * Accepts multipart form data containing a single image, and flags for each target
 */
app.post('/image', upload.single('file'), async (req: Request<{}, {}, ImageData>, res: Response) => {
	io.emit('image', req.file.buffer);
	res.sendStatus(200);
});

/**
 * Accepts an object of sensor data in and emits that to the client
 */
app.post('/sensor', async (req: Request<{}, {}, SensorData>, res: Response) => {
	io.emit('sensor', req.body);
	res.sendStatus(200);
});

// app.get

// ----------------------------------------------------------------------------------------
// Start server
// ----------------------------------------------------------------------------------------
// Define port
const port = 5000;
// Listen for new connections
server.listen(port, () => console.log('App is listening on port ' + port));
