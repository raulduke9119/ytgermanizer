# YTGermanizer 🎥 🇩🇪

YTGermanizer is a powerful tool that automatically translates YouTube videos into German, complete with natural-sounding German voice synthesis using state-of-the-art AI technology.

## 🌟 Features

- 🎥 YouTube video downloading
- 🔊 Audio extraction
- 📝 Speech-to-text transcription
- 🔄 Translation to German
- 🗣️ High-quality German text-to-speech using Bark AI
- 🎬 Automatic video synchronization
- ⚡ Speed adjustment with pitch preservation

## 🛠️ Architecture

The project is organized into modular components:

```
src/
├── main.py                 # Main application entry point
└── modules/
    ├── video_downloader.py # YouTube video downloading
    ├── audio_extractor.py  # Audio extraction from video
    ├── transcriber.py      # Speech-to-text conversion
    ├── translator.py       # Text translation
    ├── tts_generator.py    # Text-to-speech generation
    ├── synchronizer.py     # Audio-video synchronization
    └── cleanup.py          # Temporary file management
```

## 🚀 Quick Start

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions and usage examples.

## 📋 Requirements

- Python 3.8+
- FFmpeg
- Internet connection for YouTube access and API services
- GPU recommended for faster TTS generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Bark](https://github.com/suno-ai/bark) for the amazing text-to-speech technology
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for reliable YouTube video downloading
- [MoviePy](https://zulko.github.io/moviepy/) for video processing
