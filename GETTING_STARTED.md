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
   python src/main.py
   ```

2. **Interactive Workflow**
   The application will guide you through the process:
   1. Enter YouTube video URL
   2. Choose TTS model (Bark or Tacotron2)
   3. Select voice preset
   4. Configure speed and pitch settings
   5. Wait for processing
   6. Get your translated video!

## 🎯 Example Session

```
Welcome to YTGermanizer! 🎥 🇩🇪

Please enter the YouTube URL: https://www.youtube.com/watch?v=example

Choose TTS Model:
1. Bark (High quality, slower)
2. Tacotron2 (Faster, good quality)
Enter your choice (1/2): 1

Select German voice:
1. Male Speaker (v2/de_speaker_6)
2. Female Speaker (v2/de_speaker_7)
Enter your choice (1/2): 1

Processing your video:
1. Downloading video... ✅
2. Extracting audio... ✅
3. Transcribing... ✅
4. Translating to German... ✅
5. Generating German speech... ⏳
6. Synchronizing... 
7. Finalizing...

Your video will be saved in: downloads/output/translated_video_20241209_115448.mp4
```

## 🔧 Advanced Configuration

### TTS Models

1. **Bark**
   - Best for short videos (1-5 minutes)
   - Most natural-sounding speech
   - Multiple voice options
   - Requires NVIDIA GPU (no CPU support)
   - Not suitable for CPU-only systems

2. **Tacotron2**
   - Better for longer videos
   - Faster processing
   - Consistent quality
   - Single voice option
   - Works on both CPU and GPU
   - CPU mode available (slower but functional)

### Processing Times

**Tacotron2:**
- With GPU: ~10-20x realtime
- With CPU: ~30-50x realtime
  (e.g., 1-minute video takes 30-50 minutes to process)

**Bark:**
- Requires GPU: ~30-40x realtime
- No CPU support available

### Hardware Recommendations

For best experience:
- **Using Bark:** NVIDIA GPU with 6GB+ VRAM required
- **Using Tacotron2 with GPU:** Any NVIDIA GPU with 4GB+ VRAM
- **Using Tacotron2 with CPU:** Modern multi-core processor (expect longer processing times)

### File Management

The project maintains three main directories:
- `/downloads`: Main working directory
- `/downloads/temp`: Temporary processing files
- `/downloads/output`: Final output videos

Files are automatically cleaned up:
- Temp files: Immediately after processing
- Output files: Keeps last 10 by default

## 🔍 Troubleshooting

1. **Memory Issues with Bark**
   - Switch to Tacotron2 for longer videos
   - Close other GPU-intensive applications
   - Try processing in smaller segments

2. **FFmpeg Issues**
   - Ensure FFmpeg is in system PATH
   - Check FFmpeg installation: `ffmpeg -version`
   - For Windows: Restart terminal after installation

3. **Speed/Sync Issues**
   - Try different voice presets
   - Use Tacotron2 for better timing control
   - Check original video quality

4. **Network Issues**
   - Verify YouTube URL accessibility
   - Check internet connection
   - Consider using a VPN if services are blocked

## 📚 Additional Resources

- [Bark Documentation](https://github.com/suno-ai/bark)
- [Tacotron2 Documentation](https://github.com/mozilla/TTS)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)

## 🆘 Getting Help

If you encounter issues:
1. Check the [Issues](https://github.com/raulduke9119/ytgermanizer/issues) page
2. Search closed issues for similar problems
3. Create a new issue with:
   - Error message and stack trace
   - Steps to reproduce the issue
   - System information (OS, GPU, RAM)
   - Sample input video (if possible)
