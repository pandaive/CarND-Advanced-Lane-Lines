import sys
from track_lines import TrackLines
from moviepy.editor import VideoFileClip

def main(input_filename, output_filename, n_frames):
    print('Hello Panda!')
    
    track = TrackLines(n_frames)
    out_clip = 'videos/' + output_filename
    clip = VideoFileClip('videos/' + input_filename)
    #clip = clip.subclip(39, 45)
    processed_clip = clip.fl_image(track.process_image)
    processed_clip.write_videofile(out_clip, audio=False)
    print("Output saved in " + out_clip)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))