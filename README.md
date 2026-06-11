VAANI — Real-Time Speech Captioning & ISL Recognition

Vaani

Vaani is an accessibility application designed for deaf and hard-of-hearing users in India. It provides real-time speech-to-text captioning and Indian Sign Language (ISL) gesture recognition across both web and Android platforms.

Features

	•	Real-time speech transcription using OpenAI Whisper (web) and Android SpeechRecognizer (mobile)
	•	Indian Sign Language recognition using MediaPipe hand landmark detection
	•	Cosine similarity-based gesture classifier with user-trainable custom gesture support
	•	Notification-based live captions for background operation on Android
	•	Transcript saving with timestamps
	•	Dark-themed accessible UI

Tech Stack

Web: Python, Flask, Flask-SocketIO, OpenAI Whisper (tiny model), HTML/CSS/JS
Android: Java, Android Studio, MediaPipe Tasks Vision, AccessibilityService API, Android SpeechRecognizer

Setup — Web

	1.	Clone the repository
	2.	Install dependencies: pip install flask flask-socketio openai-whisper
	3.	Run: python app.py
	4.	Open http://localhost:5000 in your browser

Setup — Android

	1.	Open the project in Android Studio
	2.	Build and install on your device (Android 10+)
	3.	Grant microphone and accessibility service permissions when prompted
	4.	Tap Start to begin live captioning

Notes

	•	Tested on Realme RMX3870 running Android 16
	•	Overlay permissions are not used; captions are delivered via system notifications for compatibility with Android 16
	•	Third-party audio capture (e.g., from WhatsApp calls) is not supported due to FLAG_SECURE restrictions

Project Status

Working end-to-end on both platforms. Planned improvements include cloud deployment, multi-device testing, and real-world validation with deaf communities.
