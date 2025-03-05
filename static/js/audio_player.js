class MelodyPlayer {
    constructor() {
        this.audioContext = null;
        this.source = null;
        this.isPlaying = false;
        this.audioBuffer = null;
        this.analyser = null;
        this.canvas = null;
        this.canvasCtx = null;
        this.animationId = null;
    }

    async init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 2048;

            // Set up canvas
            this.canvas = document.getElementById('visualizer');
            this.canvasCtx = this.canvas.getContext('2d');

            // Make canvas responsive
            this.resizeCanvas();
            window.addEventListener('resize', () => this.resizeCanvas());
        } catch (error) {
            console.error('Web Audio API is not supported:', error);
        }
    }

    resizeCanvas() {
        if (this.canvas) {
            this.canvas.width = this.canvas.offsetWidth;
            this.canvas.height = this.canvas.offsetHeight;
        }
    }

    async loadMelody(base64Data) {
        try {
            // Convert base64 to array buffer
            const binaryString = window.atob(base64Data);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // Decode audio data
            this.audioBuffer = await this.audioContext.decodeAudioData(bytes.buffer);
        } catch (error) {
            console.error('Error loading melody:', error);
            throw error;
        }
    }

    draw() {
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        this.analyser.getByteTimeDomainData(dataArray);

        const width = this.canvas.width;
        const height = this.canvas.height;

        this.canvasCtx.fillStyle = 'transparent';
        this.canvasCtx.fillRect(0, 0, width, height);
        this.canvasCtx.lineWidth = 2;
        this.canvasCtx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--bs-info');
        this.canvasCtx.beginPath();

        const sliceWidth = width / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * height / 2;

            if (i === 0) {
                this.canvasCtx.moveTo(x, y);
            } else {
                this.canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        this.canvasCtx.lineTo(width, height / 2);
        this.canvasCtx.stroke();

        if (this.isPlaying) {
            this.animationId = requestAnimationFrame(() => this.draw());
        }
    }

    play() {
        if (!this.audioBuffer) return;

        // Stop if already playing
        if (this.isPlaying) {
            this.stop();
        }

        // Create new source and connect to analyser
        this.source = this.audioContext.createBufferSource();
        this.source.buffer = this.audioBuffer;
        this.source.connect(this.analyser);
        this.analyser.connect(this.audioContext.destination);
        this.source.start(0);
        this.isPlaying = true;

        // Start visualization
        this.draw();

        // Update UI when playback ends
        this.source.onended = () => {
            this.stop();
        };
    }

    stop() {
        if (this.source) {
            this.source.stop(0);
            this.source.disconnect();
        }
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        this.isPlaying = false;
        document.getElementById('playButton').innerHTML = '<i class="fas fa-play"></i> Play';

        // Clear canvas
        if (this.canvas && this.canvasCtx) {
            this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

// Initialize player
const player = new MelodyPlayer();
player.init();

// Form submission handler
document.getElementById('melodyForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitButton = document.getElementById('submitButton');
    const playButton = document.getElementById('playButton');
    const statusDiv = document.getElementById('status');

    submitButton.disabled = true;
    playButton.disabled = true;
    statusDiv.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';

    try {
        const formData = new FormData(e.target);
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        await player.loadMelody(data.melody);
        statusDiv.innerHTML = '<div class="alert alert-success">Melody generated successfully!</div>';
        playButton.disabled = false;

    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
    } finally {
        submitButton.disabled = false;
    }
});

// Play button handler
document.getElementById('playButton').addEventListener('click', () => {
    const button = document.getElementById('playButton');
    if (!player.isPlaying) {
        player.play();
        button.innerHTML = '<i class="fas fa-stop"></i> Stop';
    } else {
        player.stop();
        button.innerHTML = '<i class="fas fa-play"></i> Play';
    }
});

