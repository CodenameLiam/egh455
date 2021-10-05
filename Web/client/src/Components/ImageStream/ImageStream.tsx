import React, { FC, useEffect, useState } from 'react';
import socket from '../../Services/SocketService';
import { CardTitle } from '../../Styles/Containers';
import * as Styles from './ImageStream.styles';

const ImageStream: FC = () => {
	const [images, setImages] = useState<Array<string>>([]);

	// Subscribe to socket
	useEffect(() => {
		socket.on('image', message => {
			const base64 = btoa(new Uint8Array(message).reduce((data, byte) => data + String.fromCharCode(byte), ''));
			setImages(_images => [base64, ..._images]);
		});
	}, []);

	return (
		<Styles.Container>
			<CardTitle>Image Stream</CardTitle>
			<Styles.ImageContainer>
				{images.map(image => (
					<Styles.Image src={`data:image/png;base64, ${image}`} />
				))}
			</Styles.ImageContainer>
		</Styles.Container>
	);
};

export default ImageStream;
