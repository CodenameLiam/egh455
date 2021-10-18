import { io } from 'socket.io-client';

export const SERVER = 'http://localhost:5000';
// export const SERVER = 'http://192.168.1.20:5000';

const socket = io(process.env.NODE_ENV === 'development' ? SERVER : '');

export default socket;
