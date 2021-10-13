import { Button } from '@material-ui/core';
import { ChartConfiguration, ChartData, ChartOptions } from 'chart.js/auto';
import React, { FC, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import socket from '../../Services/SocketService';
import { CardTitle } from '../../Styles/Containers';
import * as Styles from './SensorPlot.styles';


const labels = ["Temp", "Hum", "CO2", "Pressure", "Light", "Noise"];
const chartData: ChartData = {
	datasets: [
		{
			label: "Temp",
			data: [],
			fill: true,
			cubicInterpolationMode: 'monotone',
			backgroundColor: 'rgb(255, 99, 132, 0.2)',
			borderColor: 'rgba(255, 99, 132)',
		},
	],
};

const chartOptions: ChartOptions = {
	scales: {
		yAxes: {
			suggestedMax: 1.5,
			suggestedMin: -1.5,
		},
	},
	elements: {
		point: {
			radius: 0,
		},
	},
	responsive: true,
	maintainAspectRatio: false,
};



const SensorPlot: FC = () => {
	var currentChart = 0; 
	
	// Chart reference
	const ref = useRef<ChartConfiguration | any>(null);
	// Subscribe to socket
	useEffect(() => {
		socket.on('sensor', data => {
			console.log(data);
		});
		socket.on('message', message => {
		// Update data
		const data = ref.current?.data.datasets.data;
		console.log(message)
		data?.shift();
		data?.push(message);

		// Update chart
		ref.current.update();
	 });
	}, [currentChart]);
	function changeGraph(name:number){
		currentChart = name;
		ref.current.data.datasets.label = labels[currentChart];
		ref.current.update();
	}
	return (
		<Styles.Container>
			<CardTitle>Sensor Plot</CardTitle>
			<Styles.ChartContainer>
				{labels.map((label, index) => <Button key={index} onClick={() => changeGraph(index)}>{label}</Button>)}
				<Line ref={ref} data={chartData} options={chartOptions} />
			</Styles.ChartContainer>
		</Styles.Container>
	);
};

export default SensorPlot;
