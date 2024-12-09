# Getting Started with YTGermanizer 🚀

This guide will help you set up and run YTGermanizer on your system.

## 📋 Prerequisites

1. **Python Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate     # On Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg Installation**
   - Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - macOS:
     ```bash
     brew install ffmpeg
     ```
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## 🎮 Basic Usage

1. **Run the Application**
   ```bash
   python src/main.py --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
   ```

2. **Command Line Options**
   ```bash
   python src/main.py --help
   ```
   Available options:
   - `--url`: YouTube video URL (required)
   - `--output`: Output file path (optional)
   - `--keep-temp`: Keep temporary files (optional)
   - `--voice`: Specify Bark voice preset (optional)

## 🎯 Example Usage

1. **Basic Translation**
   ```bash
   python src/main.py --url "https://www.youtube.com/watch?v=example"
   ```

2. **Custom Output Path**
   ```bash
   python src/main.py --url "https://www.youtube.com/watch?v=example" --output "my_video_german.mp4"
   ```

3. **Using Specific Voice**
   ```bash
   python src/main.py --url "https://www.youtube.com/watch?v=example" --voice "v2/de_speaker_6"
   ```

## 🔧 Troubleshooting

1. **FFmpeg Not Found**
   - Ensure FFmpeg is installed and in your system PATH
   - Try running `ffmpeg -version` to verify installation

2. **GPU Memory Issues**
   - Reduce batch size in `config.py`
   - Free up GPU memory from other applications
   - Consider using CPU mode if GPU memory is limited

3. **Network Issues**
   - Check your internet connection
   - Verify YouTube URL is accessible
   - Consider using a VPN if YouTube is blocked

## 📚 Additional Resources

- [Bark Documentation](https://github.com/suno-ai/bark)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)

## 🆘 Getting Help

If you encounter any issues:
1. Check the [Issues](https://github.com/raulduke9119/ytgermanizer/issues) page
2. Search for similar problems in closed issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System information
   - Log output
