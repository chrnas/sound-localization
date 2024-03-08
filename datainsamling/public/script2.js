// Establish a connection to the WebSocket server
const socket = io();

const canvas = document.getElementById('waveform');
const canvasCtx = canvas.getContext('2d');

const perf_counter = performance.now() / 1000
let clockOffset=0

document.getElementById('connectBtn').addEventListener('click', async function () {
    let name = document.getElementById('nameInput').value;
    let xCoordinate = document.getElementById('xInput').value;
    let yCoordinate = document.getElementById('yInput').value;
    if (!name) {
        alert('Please enter your name.');
        return;
    }
    
    // Inform the server of the new user and their coordinates
    socket.emit('newUser', { name, xCoordinate, yCoordinate });
    syncTime();

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        const audioContext = new AudioContext();

        // Check if the AudioContext is in a suspended state (this is particularly important for Safari on iOS)
        if (audioContext.state === 'suspended') {
            await audioContext.resume();
        }

        const source = audioContext.createMediaStreamSource(stream);
        const analyser = audioContext.createAnalyser();
        source.connect(analyser);
        analyser.fftSize = 2048;

        function drawLocalWaveform() {
            requestAnimationFrame(drawLocalWaveform);
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyser.getByteTimeDomainData(dataArray);

            canvasCtx.fillStyle = 'rgb(200, 200, 200)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
            canvasCtx.lineWidth = 1;
            canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
            canvasCtx.beginPath();

            let sliceWidth = canvas.width * 1.0 / bufferLength;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                let v = dataArray[i] / 128.0;
                let y = v * canvas.height / 2;
                if (i === 0) {
                    canvasCtx.moveTo(x, y);
                } else {
                    canvasCtx.lineTo(x, y);
                }
                x += sliceWidth;
            }

            canvasCtx.lineTo(canvas.width, canvas.height / 2);
            canvasCtx.stroke();
        }

        drawLocalWaveform();

        const processor = audioContext.createScriptProcessor(2048, 1, 1);
        source.connect(processor);
        processor.connect(audioContext.destination);

        let lastTriggeredTime = null;
        const debounceInterval = 300; // Debounce interval in milliseconds
        const soundThreshold = 0.15; // RMS threshold for sound detection

        function calculateRMS(buffer) {
            let sum = 0;
            for (let i = 0; i < buffer.length; i++) {
                sum += buffer[i] * buffer[i];
            }
            return Math.sqrt(sum / buffer.length);
        }

        processor.onaudioprocess = function (e) {
            const inputBuffer = e.inputBuffer.getChannelData(0);
            const rms = calculateRMS(inputBuffer);
            now = performance.now()
            if (rms > soundThreshold) {
                if (!lastTriggeredTime || now - lastTriggeredTime > debounceInterval) {
                    const timestamp = performance.now() / 1000 - perf_counter + clockOffset;
                    socket.emit('audioData', { name: name, timestamp: timestamp }); 
                    lastTriggeredTime = now;
                }
            }
        };

    } catch (err) {
        console.error('Error accessing the microphone', err);
    }
});

let clientSendTime
// Function to initiate clock synchronization
function syncTime() {
    const clientTime  = performance.now() / 1000 - perf_counter + clockOffset; // Use performance.now() for high-resolution time
    clientSendTime = clientTime; // Use performance.now() for high-resolution time
    socket.emit('syncTime')
}

// Handle server's response for time synchronization
socket.on('syncResponse', (serverTimestamp) => {

    const clientTime =  performance.now() / 1000 - perf_counter + clockOffset; // Use performance.now() for high-resolution time

    const roundTripTime = clientTime - clientSendTime

    const serverTime = serverTimestamp; 

    const estimatedServerTime = serverTime + roundTripTime / 2;

    // Update the clock offset (adjustment needed to align client clock with server clock)
    clockOffset = estimatedServerTime - clientTime;
    console.log(`Clock offset: ${clockOffset} milliseconds. Adjust your clock accordingly.`);
});
// Function to get the current time with clock offset applied





function drawGrid() {
    const gridSize = 10; // Adjust grid size as needed
    const numLinesX = gridnet.width / gridSize;
    const numLinesY = gridnet.height / gridSize;

    gridCtx.strokeStyle = '#e0e0e0'; // Light grey lines for the grid

    // Draw vertical lines
    for (let i = 0; i <= numLinesX; i++) {
        gridCtx.beginPath();
        gridCtx.moveTo(i * gridSize, 0);
        gridCtx.lineTo(i * gridSize, gridnet.height);
        gridCtx.stroke();
    }

    // Draw horizontal lines
    for (let i = 0; i <= numLinesY; i++) {
        gridCtx.beginPath();
        gridCtx.moveTo(0, i * gridSize);
        gridCtx.lineTo(gridnet.width, i * gridSize);
        gridCtx.stroke();
    }

    // Draw origin lines
    gridCtx.strokeStyle = '#000000'; // Black lines for the axes
    // X-axis
    gridCtx.beginPath();
    gridCtx.moveTo(0, gridnet.height / 2);
    gridCtx.lineTo(gridnet.width, gridnet.height / 2);
    gridCtx.stroke();
    // Y-axis
    gridCtx.beginPath();
    gridCtx.moveTo(gridnet.width / 2, 0);
    gridCtx.lineTo(gridnet.width / 2, gridnet.height);
    gridCtx.stroke();
}



function drawIncomingWaveform(dataArray, id, name) {
    let canvasId = 'canvas-' + id;
    let newCanvas = document.getElementById(canvasId);

    if (!newCanvas) {
        let container = document.createElement('div');
        container.className = 'audio-container';

        newCanvas = document.createElement('canvas');
        newCanvas.id = canvasId;
        newCanvas.className = 'audio-canvas';
        newCanvas.width = canvas.width;
        newCanvas.height = 100;

        let nameTag = document.createElement('div');
        nameTag.textContent = name;

        container.appendChild(nameTag);
        container.appendChild(newCanvas);
        document.getElementById('canvasContainer').appendChild(container);
    }

    let newCanvasCtx = newCanvas.getContext('2d');
    newCanvasCtx.clearRect(0, 0, newCanvas.width, newCanvas.height);
    newCanvasCtx.lineWidth = 1;
    newCanvasCtx.strokeStyle = 'rgb(255, 0, 0)';
    const sliceWidth = newCanvas.width / dataArray.length;
    let x = 0;

    newCanvasCtx.beginPath();
    for (let i = 0; i < dataArray.length; i++) {
        const v = dataArray[i] / 128.0;
        let y = v * 10000 + 50; // Adjusted for visibility
        if (i === 0) {
            newCanvasCtx.moveTo(x, y);
        } else {
            newCanvasCtx.lineTo(x, y);
        }
        x += sliceWidth;
    }
    newCanvasCtx.stroke();
}

function plotPoint(x, y) {
    const pointSize = 5; // Size of the point
    gridCtx.fillStyle = '#ff0000'; // Red color for the points

    // Translate coordinates so (0, 0) is at the center of the gridnet
    const centerX = gridnetCanvas.width / 2;
    const centerY = gridnetCanvas.height / 2;
    const translatedX = centerX + x;
    const translatedY = centerY - y; // Subtract y because canvas y-coordinates increase downwards

    gridCtx.beginPath();
    gridCtx.arc(translatedX, translatedY, pointSize, 0, 2 * Math.PI);
    gridCtx.fill();
}

socket.on('incomingAudioData', (payload) => {
    const { id, data, name } = payload;
    if (id !== socket.id) {
        drawIncomingWaveform(data, id, name);
    }
});

const gridnetCanvas = document.getElementById('gridnet'); // Ensure this canvas element exists in your HTML
const gridCtx = gridnetCanvas.getContext('2d');

// Function to plot a point on the grid with the origin in the middle
function plotPoint(x, y) {
    const pointSize = 5; // Size of the point
    gridCtx.fillStyle = '#ff0000'; // Red color for the points

    // Translate coordinates so (0, 0) is at the center of the gridnet
    const centerX = gridnetCanvas.width / 2;
    const centerY = gridnetCanvas.height / 2;
    const translatedX = centerX + x;
    const translatedY = centerY - y; // Subtract y because canvas y-coordinates increase downwards

    gridCtx.beginPath();
    gridCtx.arc(translatedX, translatedY, pointSize, 0, 2 * Math.PI);
    gridCtx.fill();
}

// Listen for 'updatePositions' event from the server
socket.on('updatePositions', (users) => {
    // Clear the grid before redrawing
    gridCtx.clearRect(0, 0, gridnetCanvas.width, gridnetCanvas.height);

    drawGrid();
    // Optionally redraw the grid here if needed

    // Plot each user's position on the grid
    users.forEach((user) => {
        plotPoint(user.xCoordinate * 10, user.yCoordinate * 10); // Adjust scaling factor as needed
    });
});
