// Register aliases
import 'module-alias/register';

import path from 'path';
import express, { Request, Response } from 'express';
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';
import Emitter from 'Models/Emitter';
import {play} from 'sound-play';


// ----------------------------------------------------------------------------------------
// Initialisation
// ----------------------------------------------------------------------------------------
const app = express(); // Init app
const server = createServer(app); // Create http server
const io = new Server(server, { cors: { origin: 'http://localhost:3000' } }); // Init sockets
// ----------------------------------------------------------------------------------------
// Setup middleware
// ----------------------------------------------------------------------------------------
app.use(express.static(path.join(__dirname, '../../client/build'))); // Serve static files

// ----------------------------------------------------------------------------------------
// Configure sockets
// ----------------------------------------------------------------------------------------
io.on('connection', (socket: Socket) => {
	console.log(`User connected from ${socket.handshake.address}`);

	const emitter = new Emitter(socket);

	socket.on('pause', () => {
		emitter.pause();

	});

	socket.on('play', () => {
		emitter.play();
	});

	socket.on('disconnect', () => {
		console.log(`User from ${socket.handshake.address} has disconnected`);
		emitter.pause();
	});

	socket.on('marker_detected', function(data){
		console.log(`Marker type detected: ${data.Type} ` + `File: ${data.File}`);
		const sound = require("sound-play");
		sound.play('Web/server/src/Assets/Marker_Alerts/trump_backpack_china.wav')
		io.sockets.emit('marker_detected', data);
	});

	socket.on('sensor_data', function(data){
		console.log(`New Data: Gas: ${data.Gas}` + `, Humidity: ${data.Humidity} `+ `, Pressure: ${data.Pressure} `+ `, Temperature: ${data.Temperature}` + 
			`, Light ${data.Lux}` + `, Noise: ${data.Noise}`);
		io.sockets.emit('sensor_data', data);
	});

});

// ----------------------------------------------------------------------------------------
// Configure endpoints
// ----------------------------------------------------------------------------------------
app.get('/image', async (req: Request, res: Response) => {
	res.sendFile(path.join(__dirname, 'result.png'));
});

// ----------------------------------------------------------------------------------------
// Start server
// ----------------------------------------------------------------------------------------
// Define port
const port = 5000;
// Listen for new connections
server.listen(port, () => console.log('App is listening on port ' + port));
