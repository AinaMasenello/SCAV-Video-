import subprocess
import json


def cut_video(input_file, output_file, start_time=14, duration=9):
        # Cut video using ffmpeg
        subprocess.run([
            'ffmpeg',
            '-ss', str(start_time),  # Start time
            '-i', input_file,  # Input file
            '-t', str(duration),  # Duration to cut
            '-c', 'copy',
            output_file  # Output file
        ])

class VideoProcessor:
    def __init__(self, input_file):
        self.input_file = input_file

    def extract_macroblocks_motion_vectors(self, output_file):
        # Extract macroblocks and motion vectors using ffmpeg
        subprocess.run([
            'ffmpeg',
            '-hide_banner',
            '-flags2', '+export_mvs',
            '-i', self.input_file,
            '-vf', 'codecview=mv=pf+bf+bb',
            '-an',
            output_file
        ])
        
    def export_audio_mp3_mono(self, output_file, duration=50):
    # Export BBB(50s) audio as MP3 mono track
        subprocess.run([
            'ffmpeg',
            '-ss', '0',  # Start time at 0
            '-i', self.input_file,  # Input file
            '-t', str(duration),  # Duration to extract audio
            '-vn',  # Disable video
            '-ac', '1',  # Mono audio
            '-codec:a', 'libmp3lame',
            '-q:a', '4',  # Lower quality for smaller size
            output_file  # Output file
        ])

    def export_audio_mp3_stereo_lowbitrate(self, output_file, duration=50):
        # Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        subprocess.run([
            'ffmpeg',
            '-ss', '0',  # Start time at 0
            '-i', self.input_file,  # Input file
            '-t', str(duration),  # Duration to extract audio
            '-vn',  # Disable video
            '-codec:a', 'libmp3lame',
            '-q:a', '6',  # Lower quality for smaller size
            output_file  # Output file
        ])

    def export_audio_aac(self, output_file, duration=50):
        # Export BBB(50s) audio in AAC codec
        subprocess.run([
            'ffmpeg',
            '-ss', '0',  # Start time at 0
            '-i', self.input_file,  # Input file
            '-t', str(duration),  # Duration to extract audio
            '-vn',  # Disable video
            '-c:a', 'aac',
            '-b:a', '128k',  # AAC bitrate
            output_file  # Output file
        ])

    def package_into_mp4(self, output_file, audio_mono, audio_stereo, audio_aac, video_duration=50):
        # Package everything in a .mp4 with ffmpeg
        subprocess.run([
            'ffmpeg',
            '-i', audio_mono,  # MP3 mono track
            '-i', audio_stereo,  # MP3 stereo with lower bitrate
            '-i', audio_aac,  # AAC audio
            '-i', self.input_file,  # Input video
            '-map', '0:a', '-map', '1:a', '-map', '2:a', '-map', '3:v',  # Map audio and video streams
            '-c:v', 'copy',  # Copy video codec
            '-c:a', 'aac',  # AAC codec for output audio
            '-b:a', '192k',  # AAC bitrate
            '-shortest',  # Finish encoding when the shortest stream ends
            output_file  # Output file
        ])
        
    def get_track_count(self):
        ffprobe_command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=nb_streams',
            '-of', 'default=nokey=1:noprint_wrappers=1',
            self.input_file
        ]

        try:
            ffprobe_output = subprocess.check_output(ffprobe_command, stderr=subprocess.STDOUT, text=True)
            track_count = int(ffprobe_output.strip())
            return track_count
        except subprocess.CalledProcessError as e:
            print(f"FFprobe error: {e}")
            return None

#Ex 1:

input_video = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB.mp4'
output_cut_video = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_cut.mp4'
output_with_macroblocks = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_macroblocks.mp4'

video_processor = VideoProcessor(output_cut_video)

# Cut 9 seconds from the video
cut_video(input_video, output_cut_video, start_time=14, duration=9)

# Extract macroblocks and motion vectors from the cut video
video_processor.extract_macroblocks_motion_vectors(output_with_macroblocks)


#Ex 2:

output_cut_video50 = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_50s.mp4'
output_audio_mono = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_audio_mono.mp3'
output_audio_stereo = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_audio_stereo.mp3'
output_audio_aac = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_audio_aac.aac'
output_packaged_mp4 = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/S2/BBB_packaged.mp4'

video_processor = VideoProcessor(output_cut_video50)

# Cut BBB into a 50-second video
cut_video(input_video, output_cut_video50, start_time=0, duration=50)

# Export BBB(50s) audio as MP3 mono track
video_processor.export_audio_mp3_mono(output_audio_mono)

# Export BBB(50s) audio in MP3 stereo w/ lower bitrate
video_processor.export_audio_mp3_stereo_lowbitrate(output_audio_stereo)

# Export BBB(50s) audio in AAC codec
video_processor.export_audio_aac(output_audio_aac)

# Package everything in a .mp4 with ffmpeg
video_processor.package_into_mp4(output_packaged_mp4, output_audio_mono, output_audio_stereo, output_audio_aac)


#Ex 3:

video_processor = VideoProcessor(output_packaged_mp4)
# Get the number of tracks in the MP4 container
num_tracks = video_processor.get_track_count()

if num_tracks is not None:
    print(f'The MP4 container contains {num_tracks} tracks.')
else:
    print('Error: Failed to retrieve track count.')

#Ex 6:

from semi2_ex6 import generate_video_with_histogram
input_video = 'BBB.mp4'  # Replace with your video file path
output_video_histogram = 'video_histogram.mp4'
generate_video_with_histogram(input_video, output_video_histogram)

#Ex 5:

from semi2_ex4 import SubtitleProcessor
subtitle_link = 'https://www.opensubtitles.com/download/3AA9CB07E90FD4A8833581AC8FB661449FE42DE1799E2068320D0CC5D79DCEE6F68A08B44D283192E431CB6BF5901FD9FA9F788BE0894EB231729AE7F9E1BE35AC513D7A8A2BFA564C3AED6D1603A81DF75C110EE28FCFF09DF0B6B81B18CAB4D73316BC1925B1901836300B23331723B538C30CF2004FB81F11F4F52AD08083C6BFC3C37AC2CC389FA61EA5C94EF1654584005E26A4F8C083D0AAFC95D942CFA1422479D3BFFA944167816B29FC99A52961732EDE3D689B36446FBD19D8EF59610DD68D07B5BDA51B6CC2E84B3F7E67D9BCB6759CF59D9CB955A3F0111A7F665DC240751C4DF2F58706B1B545C51AE2/subfile/big_buck_bunny.eng.srt'  # Replace with your subtitle download link
output_video_with_subtitles = 'video_with_subtitles_inheritance.mp4'

subtitle_processor = SubtitleProcessor(input_video, subtitle_link)
subtitle_processor.integrate_subtitles(output_video_with_subtitles)

