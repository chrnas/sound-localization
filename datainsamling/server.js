const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public')); // Serve static files from 'public' directory

io.on('connection', (socket) => {
    console.log(`A user connected with ID: ${socket.id}`);

    // Broadcast the new connection ID to all other users
    socket.broadcast.emit('userConnected', { id: socket.id });

    socket.on('audioData', (data) => {
        // Include the sender's ID with the broadcasted audio data
        socket.broadcast.emit('incomingAudioData', { id: socket.id, name: data.name, data: data.data });    });

    socket.on('disconnect', () => {
        console.log(`User ${socket.id} disconnected`);

        // Notify other users that this user has disconnected
        socket.broadcast.emit('userDisconnected', { id: socket.id });
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
