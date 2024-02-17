// Establish a connection to the WebSocket server
const socket = io();

const canvas = document.getElementById('waveform');
const canvasCtx = canvas.getContext('2d');

document.getElementById('connectBtn').addEventListener('click', function () {
    let name = document.getElementById('nameInput').value;
    let xCoordinate = document.getElementById('xInput').value; // Get the X coordinate from the input field
    let yCoordinate = document.getElementById('yInput').value; // Get the Y coordinate from the input field

    if (!name) {
        alert('Please enter your name.');
        return;
    }

    // Inform the server of the new user and their coordinates
    socket.emit('newUser', { name, xCoordinate, yCoordinate });

    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(stream => {
            const audioContext = new AudioContext();
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

            processor.onaudioprocess = function (e) {
                const input = e.inputBuffer.getChannelData(0);
                const inputArray = Array.from(input);
                const timestamp = new Date().toISOString();
                socket.emit('audioData', { name: name, data: inputArray, timestamp: timestamp });
            };

        })
        .catch(err => {
            console.error('Error accessing the microphone', err);
        });
});

socket.on('incomingAudioData', (payload) => {
    const { id, data, name } = payload;
    if (id !== socket.id) {
        drawIncomingWaveform(data, id, name);
    }
});

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
    const sliceWidth = newCanvas.width * 1.0 / dataArray.length;
    let x = 0;

    newCanvasCtx.beginPath();
    for (let i = 0; i < dataArray.length; i++) {
        const v = dataArray[i] / 128.0;
        let y = v * newCanvas.height / 2 + newCanvas.height / 2;
        if (i === 0) {
            newCanvasCtx.moveTo(x, y);
        } else {
            newCanvasCtx.lineTo(x, y);
        }
        x += sliceWidth;
    }
    newCanvasCtx.stroke();
}
