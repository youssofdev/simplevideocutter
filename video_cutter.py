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
    min_clip_duration = int(input("Enter the minimum clip duration in seconds (default is 4 seconds): ") or 4)
    max_clip_duration = int(input("Enter the maximum clip duration in seconds (default is 7 seconds): ") or 7)
    return min_clip_duration, max_clip_duration

def cut_video(input_file, output_folder='default', target_duration=10*60, min_clip_duration=4, max_clip_duration=7, clips_to_keep=1):
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
    
    # Calculate the total number of clips needed
    num_clips_needed = int(target_duration / min_clip_duration)
    
    # Calculate the total number of clips in the original video
    num_original_clips = int(total_duration / min_clip_duration)
    
    # Calculate the number of clips to delete
    num_clips_to_delete = num_original_clips - num_clips_needed
    
    # Initialize variables
    clips = []
    current_time = 0
    
    # Initialize tqdm for progress bar
    progress_bar = tqdm(total=num_clips_needed, desc="Editing Video", unit=" clip")
    
    while current_time < total_duration:
        # Generate a random clip duration between min_clip_duration and max_clip_duration
        clip_duration = random.uniform(min_clip_duration, max_clip_duration)
        
        # Calculate the end time of the clip
        end_time = min(current_time + clip_duration, total_duration)
        
        # Create a subclip
        subclip = video.subclip(current_time, end_time)
        
        # Add the subclip to the list
        clips.append(subclip)
        
        # Update current_time
        current_time = end_time
        
        # Update progress bar
        progress_bar.update(1)
    
    # Close the progress bar
    progress_bar.close()
    
    # Delete the specified number of clips to meet the target duration
    for _ in range(num_clips_to_delete):
        del clips[random.randint(0, len(clips) - 1)]
    
    # Merge the clips to create one video
    final_video = mp.concatenate_videoclips(clips, method="compose")
    
    # Write the final video to the output file
    final_video.write_videofile(output_filename, codec="libx264")
    
    # Display a completion message
    print("\nVideo editing completed!")

if __name__ == "__main__":
    input_file = input("Enter the path to the input video (mp4): ")
    output_folder = get_output_folder()
    min_clip_duration, max_clip_duration = get_clip_settings()
    
    print("Editing video...")
    
    # Measure the time taken for video editing
    start_time = time.time()
    
    cut_video(input_file, output_folder=output_folder, min_clip_duration=min_clip_duration, max_clip_duration=max_clip_duration)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
