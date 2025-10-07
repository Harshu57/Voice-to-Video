#!/usr/bin/env python3
"""
AI Video Studio Launcher
Run our own Veo3-like app locally
"""

import os
import sys
import subprocess

def main():
    print("🎬 Starting AI Video Studio...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app/ai_video_studio.py"):
        print("❌ Error: Please run this from the project root directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_python = ".venv/Scripts/python.exe" if os.name == 'nt' else ".venv/bin/python"
    if not os.path.exists(venv_python):
        print("❌ Error: Virtual environment not found. Please run:")
        print("   python -m venv .venv")
        print("   .venv\\Scripts\\Activate.ps1  # Windows")
        print("   .venv/bin/activate  # Linux/Mac")
        sys.exit(1)
    
    # Install dependencies if needed
    print("📦 Checking dependencies...")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies ready")
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Some dependencies might be missing")
    
    # Start the app
    print("🚀 Launching AI Video Studio...")
    print("📍 App will open at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        subprocess.run([
            venv_python, "-m", "streamlit", "run", 
            "app/ai_video_studio.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n👋 AI Video Studio stopped. Thanks for using!")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == "__main__":
    main()
