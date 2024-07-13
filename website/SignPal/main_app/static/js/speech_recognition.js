document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.getElementById('mic-button');
    const speechText = document.getElementById('speech-text');
    const statusMessage = document.getElementById('status-message');
    const video = document.getElementById('sign-language-video');
    const videoPlaceholder = document.getElementById('video-placeholder');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        let videoTimer;

        recognition.onstart = function() {
            statusMessage.textContent = 'Listening...';
            micButton.textContent = '🛑'; // Change button to stop symbol
            
            // Start the timer for video playback
            videoTimer = setTimeout(() => {
                videoPlaceholder.style.display = 'none';
                video.style.display = 'block';
                video.muted = false; // Ensure the video is not muted
                video.play().then(() => {
                    statusMessage.textContent = 'Playing sign language video...';
                }).catch(e => {
                    console.error('Error playing video:', e);
                    statusMessage.textContent = 'Error playing video. Please try again.';
                });
            }, 10000); // 10 seconds
        };

        recognition.onresult = function(event) {
            const result = event.results[0][0].transcript;
            speechText.value = result;
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            statusMessage.textContent = 'Error: ' + event.error;
            clearTimeout(videoTimer);
        };

        recognition.onend = function() {
            statusMessage.textContent = 'Listening stopped.';
            micButton.textContent = '🎤'; // Change button back to microphone
            clearTimeout(videoTimer);
            
            // Stop and reset the video if it's playing
            video.pause();
            video.currentTime = 0;
            video.style.display = 'none';
            videoPlaceholder.style.display = 'flex';
        };

        let isListening = false;

        micButton.addEventListener('click', function() {
            if (!isListening) {
                recognition.start();
                isListening = true;
            } else {
                recognition.stop();
                isListening = false;
            }
        });

        // Add event listeners for video
        video.addEventListener('play', () => {
            console.log('Video started playing');
        });

        video.addEventListener('error', (e) => {
            console.error('Video error:', e);
        });
    } else {
        micButton.style.display = 'none';
        speechText.value = 'Speech recognition is not supported in this browser.';
        statusMessage.textContent = 'Speech recognition is not supported in this browser.';
    }
});