/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SensorData } from '../models/SensorData';
import { request as __request } from '../core/request';

export class SensorService {

    /**
     * Send sensor data to the web interface
     * @param requestBody
     * @returns any OK
     * @throws ApiError
     */
    public static async postSensorService(
        requestBody: SensorData,
    ): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/sensor`,
            body: requestBody,
            mediaType: 'application/json',
        });
        return result.body;
    }

}