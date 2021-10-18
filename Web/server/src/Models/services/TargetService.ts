/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TargetData } from '../models/TargetData';
import { request as __request } from '../core/request';

export class TargetService {

    /**
     * Get target data from the database
     * @returns TargetData OK
     * @throws ApiError
     */
    public static async getTargetService(): Promise<Array<TargetData>> {
        const result = await __request({
            method: 'GET',
            path: `/target`,
        });
        return result.body;
    }

}