import { ChartConfiguration, ChartData, ChartOptions } from 'chart.js';
import React, { FC, useEffect, useRef } from 'react';
import socket from '../../Services/SocketService';
import { Bar } from 'react-chartjs-2';
import { CardTitle } from '../../Styles/Containers';
import * as Styles from './SensorFeed.styles';


const chartData: ChartData = {
	labels: ['Temp', 'Hum', 'CO2', 'Pressure', 'Light', 'Noise'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [],
			backgroundColor: [
				'rgba(255, 99, 132, 0.2)',
				'rgba(255, 159, 64, 0.2)',
				'rgba(255, 205, 86, 0.2)',
				'rgba(75, 192, 192, 0.2)',
				'rgba(54, 162, 235, 0.2)',
				'rgba(153, 102, 255, 0.2)',
			],
			borderColor: [
				'rgb(255, 99, 132)',
				'rgb(255, 159, 64)',
				'rgb(255, 205, 86)',
				'rgb(75, 192, 192)',
				'rgb(54, 162, 235)',
				'rgb(153, 102, 255)',
			],
		},
	],
};

const chartOptions: ChartOptions = {
	responsive: true,
	maintainAspectRatio: false,
};

const SensorFeed: FC = () => {
	const ref = useRef<ChartConfiguration | any>(null);
	// Subscribe to socket
	useEffect(() => {
		socket.on('sensor', data => {
			console.log(data);
		});
		socket.on('message', message => {
		// Update data
		const data = ref.current?.data.datasets;
		console.log(message)
		data?.shift();
		data?.push(message);

		// Update chart
		ref.current.update();
	 });
	}, []);

	return (
		<Styles.Container>
			<CardTitle>Sensor Feed</CardTitle>
			<Styles.ChartContainer>
				<Bar ref = {ref} data={chartData} options={chartOptions} />
			</Styles.ChartContainer>
		</Styles.Container>
	);
};

export default SensorFeed;
