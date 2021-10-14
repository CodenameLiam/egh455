/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ImageData = {
    file: string;
    personDetected?: ImageData.personDetected;
    backpackDetected?: ImageData.backpackDetected;
    markerDetected?: ImageData.markerDetected;
}

export namespace ImageData {

    export enum personDetected {
        TRUE = 'True',
        FALSE = 'False',
    }

    export enum backpackDetected {
        TRUE = 'True',
        FALSE = 'False',
    }

    export enum markerDetected {
        TRUE = 'True',
        FALSE = 'False',
    }


}
