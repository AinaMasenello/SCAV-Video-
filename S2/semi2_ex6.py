import os
import subprocess

def generate_video_with_histogram(input_file, output_file):
    # Generate a video with YUV histogram using FFmpeg
    subprocess.run([
        'ffmpeg',
        '-hide_banner',
        '-i', input_file,
        '-vf', 'split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay',
        output_file
    ])