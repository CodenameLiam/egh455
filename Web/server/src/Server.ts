// Register aliases
import 'module-alias/register';

import path from 'path';
import cors from 'cors';
import multer from 'multer';
import express, { Request, Response } from 'express';
import { Database } from 'sqlite3';
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

// Docs
import swaggerUI from 'swagger-ui-express';
import docs from './../swagger.json';

// Models
import Emitter from 'Models/Emitter';
import { play } from 'sound-play';

import { SensorData } from 'Models';
import { ImageData } from 'Models';

// ----------------------------------------------------------------------------------------
// Initialisation
// ----------------------------------------------------------------------------------------
const app = express(); // Init app
export const server = createServer(app); // Create http server
const io = new Server(server, { cors: { origin: 'http://localhost:3000' } }); // Init sockets
const upload = multer(); // Add multi-part form data

// ----------------------------------------------------------------------------------------
// Setup middleware
// ----------------------------------------------------------------------------------------
app.use(express.static(path.join(__dirname, '../../client/build'))); // Serve static files
app.use(cors({ origin: '*' })); // Allow connections from external users
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/docs', swaggerUI.serve, swaggerUI.setup(docs)); // API documentation

/* -------------------------------------------------------------------------- */
/*                             Configure Database                             */
/* -------------------------------------------------------------------------- */
const db = new Database(':memory:', err => {
	if (err) {
		console.error(err.message);
		throw err;
	} else {
		console.info('Connected to the SQlite database.');
		// Create sensor table
		db.run(
			`CREATE TABLE IF NOT EXISTS sensor (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				temperature REAL,
				pressure REAL,
				humidity REAL,
				light REAL,
				oxidised REAL,
				reduced REAL,
				nh3 REAL
			 )`,
			err => {
				if (err) {
					console.error(err);
					throw err;
				} else {
					console.info('Sensor table created');
				}
			},
		);
		// Create target table
		db.run(
			`CREATE TABLE IF NOT EXISTS target (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				type TEXT,
				date TEXT
			 )`,
			err => {
				if (err) {
					console.error(err);
					throw err;
				} else {
					console.info('Target table created');
				}
			},
		);
	}
});

/* -------------------------------------------------------------------------- */
/*                              Configure Sockets                             */
/* -------------------------------------------------------------------------- */
io.on('connection', (socket: Socket) => {
	console.log(`User connected from ${socket.handshake.address}`);

	socket.on('disconnect', () => {
		console.log(`User from ${socket.handshake.address} has disconnected`);
	});
});

/* -------------------------------------------------------------------------- */
/*                             Configure Endpoints                            */
/* -------------------------------------------------------------------------- */

/**
 * Accepts multipart form data containing a single image, and flags for each target
 */
app.post('/image', upload.single('file'), async (req: Request<{}, {}, ImageData>, res: Response) => {
	console.log('Image endpoint hit');

	const personDetected = req.body.personDetected == 'True';
	const markerDetected = req.body.markerDetected == 'True';
	const backpackDetected = req.body.backpackDetected == 'True';

	if (personDetected) {
		db.run(
			`INSERT INTO target (type, date)
			VALUES (?, ?)`,
			['Person detected', new Date().toLocaleTimeString()],
			err => {
				if (err) {
					console.error(err.message);
				}
			},
		);
	}

	if (markerDetected) {
		db.run(
			`INSERT INTO target (type, date)
			VALUES (?, ?)`,
			['Marker detected', new Date().toLocaleTimeString()],
			err => {
				if (err) {
					console.error(err.message);
				}
			},
		);
	}

	if (backpackDetected) {
		db.run(
			`INSERT INTO target (type, date)
			VALUES (?, ?)`,
			['Backpack detected', new Date().toLocaleTimeString()],
			err => {
				if (err) {
					console.error(err.message);
				}
			},
		);
	}

	io.emit('image', req.file.buffer);

	io.emit('detection', {
		personDetected,
		markerDetected,
		backpackDetected,
	});
	res.sendStatus(200);
});

/**
 * Gets last 200 rows of sensor data from the database
 */
app.get('/sensor', async (req: Request, res: Response) => {
	db.all(`SELECT * FROM sensor ORDER BY id DESC LIMIT 200`, (err, rows) => {
		if (err) {
			console.error(err.message);
			res.status(400).json({ error: err.message });
		} else {
			res.status(200).json(rows.reverse());
		}
	});
});

/**
 * Accepts an object of sensor data in and emits that to the client
 */
app.post('/sensor', async (req: Request<{}, {}, SensorData>, res: Response) => {
	console.log('Sensor endpoint hit');

	const { temperature, pressure, humidity, light, oxidised, reduced, nh3 } = req.body;

	db.run(
		`INSERT INTO sensor (temperature, pressure, humidity, light, oxidised, reduced, nh3)
	    VALUES (?, ?, ?, ?, ?, ?, ?)`,
		[temperature, pressure, humidity, light, oxidised, reduced, nh3],
		err => {
			if (err) {
				console.error(err.message);
			}
		},
	);

	io.emit('sensor', req.body);
	res.sendStatus(200);
});

/**
 * Gets last 100 rows of target data from the database
 */
app.get('/target', async (req: Request, res: Response) => {
	db.all(`SELECT * FROM target ORDER BY id DESC LIMIT 100`, (err, rows) => {
		if (err) {
			console.error(err.message);
			res.status(400).json({ error: err.message });
		} else {
			res.status(200).json(rows);
		}
	});
});

/* -------------------------------------------------------------------------- */
/*                                Start Server                                */
/* -------------------------------------------------------------------------- */
// Define port
const port = 5000;

// Listen for new connections
server.listen(port, () => console.log('App is listening on port ' + port));

// Close db on exit
process.on('exit', () => {
	db.close(err => {
		if (err) {
			return console.error(err.message);
		}
		console.log('Close the database connection.');
	});
});
