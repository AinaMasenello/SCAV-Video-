import subprocess
import os
import requests

class SubtitleProcessor:
    def __init__(self, video_file, subtitle_url):
        self.video_file = video_file
        self.subtitle_url = subtitle_url

    def download_subtitles(self):
        # Download subtitles
        response = requests.get(self.subtitle_url)
        if response.status_code == 200:
            subtitle_file = 'subtitle.srt'
            with open(subtitle_file, 'wb') as file:
                file.write(response.content)
            return subtitle_file
        else:
            print('Failed to download subtitles.')
            return None

    def integrate_subtitles(self, output_file):
        # Download subtitles
        subtitle_file = self.download_subtitles()
        if subtitle_file:
            # Integrate subtitles into the video using FFmpeg
            subprocess.run([
                'ffmpeg',
                '-i', self.video_file,
                '-vf', f"subtitles={subtitle_file}",
                '-c:a', 'copy',
                output_file
            ])
            os.remove(subtitle_file)  # Remove downloaded subtitle file after processing

# Ex 4:

input_video = 'BBB.mp4'  # Replace with your video file path
subtitle_link = 'https://www.opensubtitles.com/download/813CC8487AFDAC6E7B90F52225A78F11900640E04D38972AD23EDD8C5A6429C51890988AEBBB4C8AEFAB2D2C86A0F64318481482037824128FFA8B9C3F2791440FDE016FF4EB25A47B3C923E2582227EB49D05EC5938AF39F27FCB1823C61F1FC1B57CB367AF473B0D431EF5BBC4D05F90FAAB33D7D569C510A882CA2AA039AADE195A4FA218FCEB4D38FE86C5ECA4951ED4B64A0442B0B5024EFE3C5513424CA8453226CE923F54788B3A45F262C74F01665AB31B22D299427FC61E145535F258B752B5DEEE9C489B06A235DA0B7B75B9F229E54983FD352C55656CA85BB5AC06E5390CF324ACD9D89C0120DF0D9A7E/subfile/big_buck_bunny.eng.srt'  # Replace with your subtitle download link
output_video_with_subtitles = 'video_with_subtitles.mp4'

subtitle_processor = SubtitleProcessor(input_video, subtitle_link)

# Integrate subtitles into the video
subtitle_processor.integrate_subtitles(output_video_with_subtitles)
