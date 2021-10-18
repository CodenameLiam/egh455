import axios from 'axios';
import { SERVER } from '../Services/SocketService';
import { SensorData } from '../Types/SensorData';
import { TargetData } from '../Types/TargetData';

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
