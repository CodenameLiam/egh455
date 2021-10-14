import styled from '@emotion/styled';
import { Card } from '../../Styles/Containers';

export const Container = styled(Card)`
	margin: 1rem;
	margin-bottom: 0rem;
	flex: 2;
`;

export const ChartContainer = styled.div`
	height: 80%;
	padding: 1rem;
`;

export const TabContainer = styled.div`
	display: flex;
	border-bottom: 1px solid #ededed;
`;

interface TabProps {
	active: boolean;
	colour: string;
}

export const Tab = styled.div<TabProps>`
	padding: 0.5rem 2rem;
	border-right: 1px solid #ededed;
	cursor: pointer;
	transition: all 0.3s;
	background-color: ${({ active, colour }) => (active ? colour : 'unset')};
	/* background: red; */

	&:hover {
		background-color: ${({ active, colour }) => (active ? colour : '#ededed')};
	}
`;
