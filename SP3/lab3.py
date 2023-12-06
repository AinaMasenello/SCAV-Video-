import subprocess

def convert_video(input_file, output_file, resolution):
    cmd = [
        'ffmpeg', '-i', input_file,
        '-vf', f'scale={resolution}', '-c:a', 'copy', output_file
    ]
    subprocess.run(cmd)

# Replace 'input_video.mp4' with your video file name
input_video = 'BBB.mp4'

# Define output file names for different resolutions
resolutions = {
    '1280x720': 'output_720p.mp4',
    '640x480': 'output_480p.mp4',
    '360x240': 'output_360x240.mp4',
    '160x120': 'output_160x120.mp4'
}

# Convert to different resolutions
for resolution, output_file in resolutions.items():
    convert_video(input_video, output_file, resolution)
    
#EX 1:

import os

class VideoConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_to_vp8(self, output_file):
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'libvpx',
            '-b:v', '1M',
            output_file
        ]
        subprocess.run(command)

    def convert_to_vp9(self, output_file):
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'libvpx-vp9',
            '-b:v', '2M',
            output_file
        ]
        subprocess.run(command)

    def convert_to_h265(self, output_file):
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'libx265',
            '-crf', '28',
            output_file
        ]
        subprocess.run(command)

    def convert_to_av1(self, output_file):
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'libaom-av1',
            '-aom-params', 'lossless=1',
            output_file
        ]
        subprocess.run(command)

    def convert_to_all_formats(self, output_folder):
        base_filename = os.path.splitext(os.path.basename(self.input_file))[0]
        
        self.convert_to_vp8(os.path.join(output_folder, base_filename + '_vp8.webm'))
        self.convert_to_vp9(os.path.join(output_folder, base_filename + '_vp9.webm'))
        self.convert_to_h265(os.path.join(output_folder, base_filename + '_h265.mp4'))
        self.convert_to_av1(os.path.join(output_folder, base_filename + '_av1.mp4'))

# Example usage:
input_video = 'output_720p.mp4'
output_directory = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/SP3'

converter = VideoConverter(input_video)
converter.convert_to_all_formats(output_directory)

# EX 2:

def create_comparison_video(video1_path, video2_path, output_path):
    command = [
        'ffmpeg',
        '-i', video1_path,
        '-i', video2_path,
        '-filter_complex', '[0:v][1:v]scale2ref=iw:ih[vid1][vid2];[vid1]scale=iw/2:ih/2[left];[vid2]scale=iw/2:ih/2[right];[left][right]hstack',
        output_path
    ]
    subprocess.run(command)

# Example usage:
video1 = 'output_720p_vp8.webm'
video2 = 'output_720p_vp9.webm'
output_video = 'comparison_video.webm'

create_comparison_video(video1, video2, output_video)
# In the comparison video we can see that the quality of both videos is very similar but a little better for the vp9.