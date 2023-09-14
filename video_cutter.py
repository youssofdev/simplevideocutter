import moviepy.editor as mp
import os
import random

def cut_video(input_file, output_folder='default', target_duration=10*60, clip_duration=5, clips_to_keep=1):
    # Load the video
    video = mp.VideoFileClip(input_file)
    
    # Remove audio
    video = video.set_audio(None)
    
    # Get the video duration
    total_duration = video.duration
    
    # Use the default output folder if specified
    if output_folder.lower() == 'default':
        output_folder = os.path.join(os.path.expanduser("~"), 'Videos', 'Captures', 'Output')
    
    # Ensure the output folder exists, create it if necessary
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate a random output filename
    output_filename = os.path.join(output_folder, 'output.mp4')
    
    # Calculate the total number of clips needed
    num_clips_needed = int(target_duration / clip_duration)
    
    # Calculate the total number of clips in the original video
    num_original_clips = int(total_duration / clip_duration)
    
    # Calculate the number of clips to delete
    num_clips_to_delete = num_original_clips - num_clips_needed
    
    # Initialize variables
    clips = []
    current_time = 0
    
    while current_time < total_duration:
        # Calculate the end time of the clip
        end_time = min(current_time + clip_duration, total_duration)
        
        # Create a subclip
        subclip = video.subclip(current_time, end_time)
        
        # Add the subclip to the list
        clips.append(subclip)
        
        # Update current_time
        current_time = end_time
    
    # Delete the specified number of clips to meet the target duration
    for _ in range(num_clips_to_delete):
        del clips[random.randint(0, len(clips) - 1)]
    
    # Merge the clips to create one video
    final_video = mp.concatenate_videoclips(clips, method="compose")
    
    # Write the final video to the output file
    final_video.write_videofile(output_filename, codec="libx264")

if __name__ == "__main__":
    input_file = input("Enter the path to the input video (mp4): ")
    output_folder = input("Enter the path to the output folder or type 'default' for default folder: ")
    cut_video(input_file, output_folder=output_folder)
