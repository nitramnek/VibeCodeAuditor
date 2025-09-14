#!/usr/bin/env python3
"""
Watch the logs in real-time
"""
import time
import subprocess
import sys

def watch_logs():
    """Watch logs in real-time"""
    print("👀 Watching logs... Upload a file to see debug output")
    print("Press Ctrl+C to stop")
    print("="*50)
    
    try:
        # Use tail -f to follow the log file
        process = subprocess.Popen(
            ['tail', '-f', 'logs/vibeauditor.log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        for line in process.stdout:
            print(line.strip())
            
    except KeyboardInterrupt:
        print("\\n👋 Stopped watching logs")
        process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    watch_logs()