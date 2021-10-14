/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImageData } from '../models/ImageData';
import { request as __request } from '../core/request';

export class ImageService {

    /**
     * Send image data to the web interface
     * @param requestBody
     * @returns any OK
     * @throws ApiError
     */
    public static async postImageService(
        requestBody: ImageData,
    ): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/image`,
            body: requestBody,
        });
        return result.body;
    }

}