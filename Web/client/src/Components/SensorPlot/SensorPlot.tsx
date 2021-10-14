import { ChartConfiguration, ChartData, ChartOptions } from 'chart.js/auto';
import React, { FC, useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import socket from '../../Services/SocketService';
import Colours from '../../Styles/Colours';
import { CardTitle } from '../../Styles/Containers';
import { SensorData } from '../../Types/SensorData';
import * as Styles from './SensorPlot.styles';

interface DataType {
	key: keyof SensorData;
	name: string;
	colour: string;
}

const dataType: DataType[] = [
	{ key: 'temperature', name: 'Temp', colour: Colours.temperature },
	{ key: 'pressure', name: 'Pre', colour: Colours.pressure },
	{ key: 'humidity', name: 'Hum', colour: Colours.humidity },
	{ key: 'light', name: 'Light', colour: Colours.light },
	{ key: 'oxidised', name: 'Ox', colour: Colours.oxidised },
	{ key: 'reduced', name: 'Red', colour: Colours.reduced },
	{ key: 'nh3', name: 'NH3', colour: Colours.nh3 },
];

const chartData: ChartData = {
	datasets: [
		{
			label: 'Temp',
			data: [],
			fill: true,
			cubicInterpolationMode: 'monotone',
			backgroundColor: Colours.temperatureLight,
			borderColor: Colours.temperature,
		},
	],
};

const chartOptions: ChartOptions = {
	scales: {
		yAxes: {
			suggestedMax: 1.5,
			suggestedMin: 0,
		},
	},
	elements: {
		point: {
			radius: 0,
		},
	},
	plugins: {
		legend: {
			display: false,
		},
	},
	responsive: true,
	maintainAspectRatio: false,
};

const SensorPlot: FC = () => {
	var currentChart = 0;

	// Chart reference
	const ref = useRef<ChartConfiguration | any>(null);
	const [sensor, setSensor] = useState<keyof SensorData>('temperature');

	// Subscribe to socket
	useEffect(() => {
		socket.on('sensor', data => {
			console.log(data);
			if (ref.current) {
				const chartData = ref.current.data.datasets[0].data;
				chartData?.shift();
				chartData?.push(data[sensor]);
				ref.current.update();
			}
		});
	}, []);

	useEffect(() => {
		if (ref.current) {
			ref.current.data.datasets[0].data = Array.from(Array(200));
			ref.current.data.datasets[0].backgroundColor = Colours[`${sensor}Light` as keyof typeof Colours];
			ref.current.data.datasets[0].borderColor = Colours[sensor as keyof typeof Colours];
			ref.current.update();
		}
	}, [sensor]);

	return (
		<Styles.Container>
			<CardTitle>Sensor Plot</CardTitle>
			<Styles.TabContainer>
				{dataType.map(_data => (
					<Styles.Tab
						key={_data.key}
						active={_data.key === sensor}
						colour={Colours[`${sensor}Light` as keyof typeof Colours]}
						onClick={() => setSensor(_data.key)}
					>
						{_data.name}
					</Styles.Tab>
				))}
			</Styles.TabContainer>
			<Styles.ChartContainer>
				<Line ref={ref} data={chartData} options={chartOptions} />
			</Styles.ChartContainer>
		</Styles.Container>
	);
};

export default SensorPlot;
