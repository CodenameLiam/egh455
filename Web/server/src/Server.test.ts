import { server } from './Server';
import request from 'supertest';
import path from 'path';

afterAll(done => {
	server.close();
	done();
});

describe('Sensor Endpoint', () => {
	const data = {
		id: 1,
		temperature: 5,
		pressure: 3,
		humidity: 7,
		light: 5,
		oxidised: 1,
		reduced: 9,
		nh3: 3,
	};

	const createData = async () => {
		return await request(server).post('/sensor').send(data);
	};

	const getData = async () => {
		return await request(server).get('/sensor');
	};

	it('should post data', async () => {
		const res = await createData();
		expect(res.statusCode).toEqual(200);
	});

	it('should get data', async () => {
		const res = await getData();
		expect(res.body).toEqual([data]);
	});
});

describe('Image Endpoint', () => {
	const createImageData = async () => {
		return await request(server)
			.post('/image')
			.field('personDetected', 'True')
			.attach('file', path.resolve(__dirname, './Mock/mock.png'));
	};

	it('should post data', async () => {
		const res = await createImageData();
		expect(res.statusCode).toEqual(200);
	});
});

describe('Target Endpoint', () => {
	const getTargetData = async () => {
		return request(server).get('/target');
	};

	it('should get data', async () => {
		const res = await getTargetData();
		expect(res.body).toEqual([
			{
				id: 1,
				type: 'Person detected',
				date: new Date().toLocaleTimeString(),
			},
		]);
	});
});
