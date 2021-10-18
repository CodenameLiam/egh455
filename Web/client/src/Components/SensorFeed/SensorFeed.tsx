import { ChartConfiguration, ChartData, ChartOptions } from 'chart.js';
import React, { FC, useEffect, useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import socket from '../../Services/SocketService';
import Colours from '../../Styles/Colours';
import { CardTitle } from '../../Styles/Containers';
import { SensorData } from '../../Types/SensorData';
import * as Styles from './SensorFeed.styles';

const tempData: ChartData = {
	labels: ['Temp'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.temperatureLight],
			borderColor: [Colours.temperature],
		},
	],
};

const preData: ChartData = {
	labels: ['Pressue'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.pressureLight],
			borderColor: [Colours.pressure],
		},
	],
};

const humData: ChartData = {
	labels: ['Hummidity'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.humidityLight],
			borderColor: [Colours.humidity],
		},
	],
};

const lightData: ChartData = {
	labels: ['Light'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.lightLight],
			borderColor: [Colours.light],
		},
	],
};

const oxData: ChartData = {
	labels: ['Oxideised'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.oxidisedLight],
			borderColor: [Colours.oxidised],
		},
	],
};

const reData: ChartData = {
	labels: ['Reduced'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.reducedLight],
			borderColor: [Colours.reduced],
		},
	],
};

const nh3Data: ChartData = {
	labels: ['NH3'],
	datasets: [
		{
			label: 'Sensor value',
			borderWidth: 2,
			fill: true,
			data: [null],
			backgroundColor: [Colours.nh3Light],
			borderColor: [Colours.nh3],
		},
	],
};

// const chartData: ChartData = {
// 	labels: ['Temp', 'Pressue', 'Hum', 'Light', 'Oxideised', 'Reduced', 'NH3'],
// 	datasets: [
// 		{
// 			label: 'Sensor value',
// 			borderWidth: 2,
// 			fill: true,
// 			data: [65, 59, 80, 81, 56, 55, 12],
// 			backgroundColor: [
// 				'rgba(255, 99, 132, 0.2)',
// 				'rgba(255, 159, 64, 0.2)',
// 				'rgba(255, 205, 86, 0.2)',
// 				'rgba(75, 192, 192, 0.2)',
// 				'rgba(54, 162, 235, 0.2)',
// 				'rgba(102, 120, 255, 0.2)',
// 				'rgba(153, 102, 255, 0.2)',
// 			],
// 			borderColor: [
// 				'rgb(255, 99, 132)',
// 				'rgb(255, 159, 64)',
// 				'rgb(255, 205, 86)',
// 				'rgb(75, 192, 192)',
// 				'rgb(54, 162, 235)',
// 				'rgb(102, 120, 255)',
// 				'rgb(153, 102, 255)',
// 			],
// 		},
// 	],
// };

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
	// Chart references
	const tempRef = useRef<ChartConfiguration | any>(null);
	const preRef = useRef<ChartConfiguration | any>(null);
	const humRef = useRef<ChartConfiguration | any>(null);
	const lightRef = useRef<ChartConfiguration | any>(null);
	const oxRef = useRef<ChartConfiguration | any>(null);
	const reRef = useRef<ChartConfiguration | any>(null);
	const nh3Ref = useRef<ChartConfiguration | any>(null);

	// Subscribe to socket
	useEffect(() => {
		socket.on('sensor', (data: SensorData) => {
			if (tempRef.current) {
				tempRef.current.data.datasets[0].data = [data.temperature];
				tempRef.current.update();
			}
			if (preRef.current) {
				preRef.current.data.datasets[0].data = [data.pressure];
				preRef.current.update();
			}
			if (humRef.current) {
				humRef.current.data.datasets[0].data = [data.humidity];
				humRef.current.update();
			}
			if (lightRef.current) {
				lightRef.current.data.datasets[0].data = [data.light];
				lightRef.current.update();
			}
			if (oxRef.current) {
				oxRef.current.data.datasets[0].data = [data.oxidised];
				oxRef.current.update();
			}
			if (reRef.current) {
				reRef.current.data.datasets[0].data = [data.reduced];
				reRef.current.update();
			}
			if (nh3Ref.current) {
				nh3Ref.current.data.datasets[0].data = [data.nh3];
				nh3Ref.current.update();
			}
		});
	}, []);

	return (
		<Styles.Container>
			<CardTitle>Sensor Feed</CardTitle>
			<Styles.ChartContainer>
				<Styles.ChartCell>
					<Bar ref={tempRef} data={tempData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={preRef} data={preData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={humRef} data={humData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={lightRef} data={lightData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={oxRef} data={oxData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={reRef} data={reData} options={chartOptions} />
				</Styles.ChartCell>
				<Styles.ChartCell>
					<Bar ref={nh3Ref} data={nh3Data} options={chartOptions} />
				</Styles.ChartCell>
			</Styles.ChartContainer>
		</Styles.Container>
	);
};

export default SensorFeed;
