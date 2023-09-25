import moviepy.editor as mp
import os
import random
from tqdm import tqdm
import time

def get_output_folder():
    default_folder = os.path.join(os.path.expanduser("~"), 'Videos', 'Captures', 'Output')
    user_folder = input(f"Enter the path to the output folder or press Enter to use the default ({default_folder}): ")
    return user_folder if user_folder.strip() else default_folder

def get_clip_settings():
    min_clip_duration = int(input("Enter the minimum clip duration in seconds (default is 3 seconds): ") or 3)
    max_clip_duration = int(input("Enter the maximum clip duration in seconds (default is 7 seconds): ") or 7)
    return min_clip_duration, max_clip_duration

def get_target_duration():
    target_duration_minutes = int(input("Enter the target video length in minutes (default is 10 minutes): ") or 10)
    return target_duration_minutes * 60  # Convert to seconds

def cut_video(input_file, output_folder='default', min_clip_duration=3, max_clip_duration=7, target_duration=600, flip_horizontal=False):
    # Load the video
    video = mp.VideoFileClip(input_file)
    
    # Remove audio
    video = video.set_audio(None)
    
    # Get the video duration
    total_duration = video.duration
    
    # Use the default output folder if specified
    if output_folder.lower() == 'default':
        output_folder = get_output_folder()
    
    # Ensure the output folder exists, create it if necessary
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate a random output filename
    output_filename = os.path.join(output_folder, 'output.mp4')
    
    # Initialize variables
    clips = []
    current_time = 0
    
    # Initialize tqdm for progress bar
    progress_bar = tqdm(total=target_duration, desc="Editing Video", unit=" sec")
    
    while current_time < target_duration:
        # Generate a random clip duration between min_clip_duration and max_clip_duration
        clip_duration = random.randint(min_clip_duration, max_clip_duration)
        
        # Calculate the end time of the clip
        end_time = min(current_time + clip_duration, target_duration)
        
        # Create a subclip
        subclip = video.subclip(current_time, end_time)
        
        # Add the subclip to the list
        clips.append(subclip)
        
        # Update current_time
        current_time = end_time
        
        # Update progress bar
        progress_bar.update(clip_duration)
    
    # Close the progress bar
    progress_bar.close()
    
    # Delete the majority of clips to create the summary
    num_clips_to_keep = len(clips) // 6  # Keep 1 clip for every 6 clips
    if num_clips_to_keep == 0:
        num_clips_to_keep = 1  # Keep at least 1 clip
    clips_to_delete = len(clips) - num_clips_to_keep
    
    if clips_to_delete > 0:
        for _ in range(clips_to_delete):
            del clips[random.randint(0, len(clips) - 1)]
    
    # Merge the clips to create one video
    final_video = mp.concatenate_videoclips(clips, method="compose")
    
    if flip_horizontal:
        # Flip the video horizontally
        final_video = final_video.fx(mp.vfx.mirror_x)
    
    # Write the final video to the output file
    final_video.write_videofile(output_filename, codec="libx264")
    
    # Display a completion message
    print("\nVideo editing completed!")

if __name__ == "__main__":
    input_file = input("Enter the path to the input video (mp4): ")
    output_folder = get_output_folder()
    min_clip_duration, max_clip_duration = get_clip_settings()
    target_duration = get_target_duration()
    
    flip_option = input("Do you want to flip the video horizontally? (yes/no): ").lower()
    flip_horizontal = flip_option == "yes"
    
    print("Editing video...")
    
    # Measure the time taken for video editing
    start_time = time.time()
    
    cut_video(input_file, output_folder=output_folder, min_clip_duration=min_clip_duration, max_clip_duration=max_clip_duration, target_duration=target_duration, flip_horizontal=flip_horizontal)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
