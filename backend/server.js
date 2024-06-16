const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const scrapingController = require('./controllers/scrapingController');
const analysisController = require('./controllers/analysisController');
const blingController = require('./controllers/blingController');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.json());

// Rotas
app.use('/api/scraping', scrapingController);
app.use('/api/analysis', analysisController);
app.use('/api/bling', blingController);

// Configuração do Socket.IO para atualizações em tempo real
io.on('connection', (socket) => {
    console.log('New client connected');
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});