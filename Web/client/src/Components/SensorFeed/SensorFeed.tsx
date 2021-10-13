import { ChartConfiguration, ChartData, ChartOptions } from 'chart.js';
import React, { FC, useEffect, useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import socket from '../../Services/SocketService';
import { CardTitle } from '../../Styles/Containers';
import { SensorData } from '../../Types/SensorData';
import * as Styles from './SensorFeed.styles';

const chartData: ChartData = {
	labels: ['Temp', 'Pressue', 'Hum', 'Light', 'Oxideised', 'Reduced', 'NH3'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [65, 59, 80, 81, 56, 55, 12],
			backgroundColor: [
				'rgba(255, 99, 132, 0.2)',
				'rgba(255, 159, 64, 0.2)',
				'rgba(255, 205, 86, 0.2)',
				'rgba(75, 192, 192, 0.2)',
				'rgba(54, 162, 235, 0.2)',
				'rgba(102, 120, 255, 0.2)',
				'rgba(153, 102, 255, 0.2)',
			],
			borderColor: [
				'rgb(255, 99, 132)',
				'rgb(255, 159, 64)',
				'rgb(255, 205, 86)',
				'rgb(75, 192, 192)',
				'rgb(54, 162, 235)',
				'rgb(102, 120, 255)',
				'rgb(153, 102, 255)',
			],
		},
	],
};

const chartOptions: ChartOptions = {
	responsive: true,
	maintainAspectRatio: false,
	plugins: {
		legend: {
			display: false,
		},
	},
};

const SensorFeed: FC = () => {
	// Chart reference
	const ref = useRef<ChartConfiguration | any>(null);

	// Subscribe to socket
	useEffect(() => {
		socket.on('sensor', (data: SensorData) => {
			if (ref.current) {
				ref.current.data.datasets[0].data = Object.values(data);
				ref.current.update();
			}
		});
	}, []);

	return (
		<Styles.Container>
			<CardTitle>Sensor Feed</CardTitle>
			<Styles.ChartContainer>
				<Bar ref={ref} data={chartData} options={chartOptions} />
			</Styles.ChartContainer>
		</Styles.Container>
	);
};

export default SensorFeed;
