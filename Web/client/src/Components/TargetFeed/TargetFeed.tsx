import { TableBody, Table, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { FC, useEffect, useRef, useState } from 'react';
import socket from '../../Services/SocketService';
import { CardTitle } from '../../Styles/Containers';
import * as Styles from './TargetFeed.styles';

interface Detections {
	text: string;
	date: string;
}

const TargetFeed: FC = () => {
	const [detections, setDetections] = useState<Detections[]>([]);
	const personAudio = useRef<HTMLAudioElement>(null);
	const backpackAudio = useRef<HTMLAudioElement>(null);
	const markerAudio = useRef<HTMLAudioElement>(null);

	// Subscribe to socket
	useEffect(() => {
		socket.on('detection', data => {
			const _detections: Detections[] = [];
			if (data.personDetected) {
				_detections.push({ text: 'Person detected', date: new Date().toLocaleTimeString() });
				// Play person sound
				if (backpackAudio.current?.paused && markerAudio.current?.paused) {
					personAudio.current?.play();
				}
			}
			if (data.backpackDetected) {
				_detections.push({ text: 'Backpack detected', date: new Date().toLocaleTimeString() });
				// Play backpack sound
				if (markerAudio.current?.paused && personAudio.current?.paused) {
					backpackAudio.current?.play();
				}
			}
			if (data.markerDetected) {
				_detections.push({ text: 'Marker detected', date: new Date().toLocaleTimeString() });
				// Play marker sound
				if (backpackAudio.current?.paused && personAudio.current?.paused) {
					markerAudio.current?.play();
				}
			}
			setDetections(prev => [..._detections, ...prev]);
		});
	}, []);

	return (
		<Styles.Container>
			<audio ref={personAudio} src={process.env.PUBLIC_URL + '/Audio/trump_person_wall.wav'} />
			<audio ref={backpackAudio} src={process.env.PUBLIC_URL + '/Audio/trump_backpack_china.wav'} />
			<audio ref={markerAudio} src={process.env.PUBLIC_URL + '/Audio/trump_aruco_great.wav'} />
			<CardTitle>Target Feed</CardTitle>
			<Styles.Table>
				<Table>
					<TableHead>
						<TableRow>
							<TableCell width="80%">Message</TableCell>
							<TableCell width="20%">Timestamp</TableCell>
							<TableCell />
						</TableRow>
					</TableHead>
					<TableBody>
						{detections.map(detection => (
							<TableRow>
								<TableCell>{detection.text}</TableCell>
								<TableCell>{detection.date}</TableCell>
								<TableCell />
							</TableRow>
						))}
					</TableBody>
				</Table>
			</Styles.Table>
		</Styles.Container>
	);
};

export default TargetFeed;
