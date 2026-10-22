#!/usr/bin/env python3
"""
Start the web application server
"""
import sys
import os
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if web dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import aiofiles
        return True
    except ImportError:
        return False


def main():
    """Start the web server."""
    print("=" * 60)
    print("Instagram Video Editor - Web Application")
    print("=" * 60)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Web dependencies not installed.")
        print("\nInstall them with:")
        print("  pip install -r web_requirements.txt")
        print("\nOr install individually:")
        print("  pip install fastapi uvicorn[standard] python-multipart aiofiles jinja2")
        return 1

    # Check FFmpeg
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  Warning: FFmpeg not found.")
        print("Please install FFmpeg to process videos:")
        print("  macOS:    brew install ffmpeg")
        print("  Ubuntu:   sudo apt install ffmpeg")
        print("  Windows:  Download from https://ffmpeg.org/download.html")
        print()

    # Start server
    print("\n✓ Starting server...")
    print("\n📱 Open in your browser:")
    print("   http://localhost:8000")
    print("\n🛑 Press Ctrl+C to stop")
    print("=" * 60)
    print()

    try:
        import uvicorn
        # Use PORT environment variable for Railway/Render, default to 8000 for local
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(
            "web.app:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
