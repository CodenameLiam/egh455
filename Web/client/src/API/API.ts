import axios from 'axios';
import { SensorData } from '../Types/SensorData';
import { TargetData } from '../Types/TargetData';

const SERVER = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
// const SERVER = 'http://192.168.1.20:5000';

/**
 * Gets sensor data from the server database
 * @returns Array of the last 200 sensor data records
 */
const getSensorData = async (): Promise<SensorData[]> => {
	const response = await axios.get<SensorData[]>(`${SERVER}/sensor`);
	return response.data;
};

/**
 * Gets sensor data from the server database
 * @returns Array of the last 200 sensor data records
 */
const getTargetData = async (): Promise<TargetData[]> => {
	const response = await axios.get<TargetData[]>(`${SERVER}/target`);
	return response.data;
};

/**
 * API Definition
 */
export const API = {
	getSensorData,
	getTargetData,
};
