import subprocess
import json
import sys

#EX 1:

def convert_video_mp2(input_video, output_video):
    info_command = f"ffmpeg -i {input_video} {output_video}"
    subprocess.run(info_command, shell=True, check=True)

input_video = "/Users/ainamasenello/Documents/GitHub/SCAV-Video-/P2/Big_Buck_Bunny_1080_10s_30MB.mp4"
output_video = "/Users/ainamasenello/Documents/GitHub/SCAV-Video-/P2/BBB.mpg"
convert_video_mp2(input_video, output_video)
    
#EX 2:

def modify_resolution(input_video, output_video2, new_resolution):
    # Run FFmpeg to modify the resolution
    modification_command = f"ffmpeg -i {input_video} -vf 'scale={new_resolution}' -c:a copy {output_video2}"
    subprocess.run(modification_command, shell=True)

output_video2 = "/Users/ainamasenello/Documents/GitHub/SCAV-Video-/P2/BBB_resized.mp4"
modify_resolution(input_video, output_video2, '854x480')

#EX 3:

def change_chroma_subsampling(input_video, output_video3, chroma_subsampling):
    # Run FFmpeg to change the chroma subsampling
    modification_command = f"ffmpeg -i {input_video} -c:v libx264 -pix_fmt {chroma_subsampling} -c:a copy {output_video3}"
    subprocess.run(modification_command, shell=True)

output_video3 = "/Users/ainamasenello/Documents/GitHub/SCAV-Video-/P2/BBB_chroma_subsampling.mp4"
change_chroma_subsampling(input_video, output_video3, "yuv420p")

#EX 4:

def get_video_info(input_video):
    # Run FFprobe to get video information
    info_command = f"ffprobe -v quiet -print_format json -show_streams -select_streams v:0 {input_video}"
    info_output = subprocess.check_output(info_command, shell=True).decode('utf-8')

    video_data = json.loads(info_output)

    if 'streams' in video_data and len(video_data['streams']) > 0:
        video_stream = video_data['streams'][0]
        print(f"Video Information for {input_video}:")
        print(f"Resolution: {video_stream['width']}x{video_stream['height']}")
        print(f"Duration: {video_stream['duration']} seconds")
        print(f"Bitrate: {video_stream['bit_rate']} bps")
        print(f"Video Codec: {video_stream['codec_name']}")
        print(f"Frame Rate: {eval(video_stream['avg_frame_rate'])} fps")
    else:
        print(f"No video stream information found in {input_video}")

get_video_info(input_video)

#EX 5:

sys.path.append('/Users/ainamasenello/Documents/GitHub/SCAV-Video-/P1')
import rgb_yuv
rgb_values = (0, 128, 0)
yuv_values = rgb_yuv.translate_rgb_yuv(*rgb_values)
print("RGB to YUV:", yuv_values)

