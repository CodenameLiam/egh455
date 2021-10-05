import React, { FC, useEffect, useState } from 'react';
import socket from '../../Services/SocketService';
import { CardTitle } from '../../Styles/Containers';
import * as Styles from './VideoFeed.styles';

const VideoFeed: FC = () => {
	const [image, setImage] = useState<string>();

	// Subscribe to socket
	useEffect(() => {
		socket.on('image', message => {
			const base64 = btoa(new Uint8Array(message).reduce((data, byte) => data + String.fromCharCode(byte), ''));
			setImage(base64);
		});
	}, []);

	return (
		<Styles.Container>
			<CardTitle>Video Feed</CardTitle>
			{image && <Styles.VideoContainer src={`data:image/png;base64, ${image}`} />}
		</Styles.Container>
	);
};

export default VideoFeed;
