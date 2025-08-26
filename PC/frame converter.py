import cv2
import numpy as np
from PIL import Image
import os

# --- Configuration ---
OUTPUT_VIDEO_FILE = "bad_apple_8x8_preview.mp4"
OUTPUT_IMAGE_FOLDER = "bad_apple_8x8_frames"
FRAME_RATE = 30  # Match the target frame rate of the Pico project

# The final viewable size of the 8x8 video/images
OUTPUT_WIDTH = 480
OUTPUT_HEIGHT = 480

def get_video_filename():
    """Prompts the user for a video file and validates it."""
    while True:
        filename = input("Enter the name of the video file (e.g., my_video.mp4): ")
        if os.path.exists(filename):
            return filename
        print(f"Error: File '{filename}' not found. Please make sure it's in the same folder as the script.")

def get_user_choice():
    """Prompts the user to select an export format."""
    while True:
        print("\nSelect an export option:")
        print("  1: Export as video only (.mp4)")
        print("  2: Export as images only (.png sequence)")
        print("  3: Export as both video and images")
        choice = input("Enter your choice (1/2/3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    """
    Main function to process the video and create an 8x8 preview version.
    """
    video_source = get_video_filename()
    export_choice = get_user_choice()
    
    export_video = export_choice in ['1', '3']
    export_images = export_choice in ['2', '3']

    print(f"Opening video file: {video_source}")
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # --- Setup based on user choice ---
    if export_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(OUTPUT_VIDEO_FILE, fourcc, FRAME_RATE, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        print(f"Will export video to: {OUTPUT_VIDEO_FILE}")

    if export_images:
        if not os.path.exists(OUTPUT_IMAGE_FOLDER):
            os.makedirs(OUTPUT_IMAGE_FOLDER)
        print(f"Will export image frames to: ./{OUTPUT_IMAGE_FOLDER}/")

    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break # End of video

        # --- Process the frame to 8x8 monochrome ---
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_pil = img_pil.resize((8, 8), Image.LANCZOS)
        img_pil = img_pil.convert('1', dither=Image.FLOYDSTEINBERG)
        
        # --- Scale up for viewing ---
        processed_frame_np = np.array(img_pil).astype(np.uint8) * 255
        scaled_frame = cv2.resize(processed_frame_np, (OUTPUT_WIDTH, OUTPUT_HEIGHT), interpolation=cv2.INTER_NEAREST)
        
        # --- Save the frame based on user choice ---
        if export_video:
            output_frame_bgr = cv2.cvtColor(scaled_frame, cv2.COLOR_GRAY2BGR)
            out_video.write(output_frame_bgr)
        
        if export_images:
            # Save the scaled-up grayscale frame directly
            image_filename = os.path.join(OUTPUT_IMAGE_FOLDER, f"frame_{frame_count:05d}.png")
            cv2.imwrite(image_filename, scaled_frame)
        
        frame_count += 1
        print(f"Processing frame {frame_count}...")

    # Release everything when the job is done
    cap.release()
    if export_video:
        out_video.release()
    cv2.destroyAllWindows()

    print("\nConversion complete!")
    if export_video:
        print(f"Preview video saved as {OUTPUT_VIDEO_FILE}")
    if export_images:
        print(f"Image frames saved in ./{OUTPUT_IMAGE_FOLDER}/")

if __name__ == "__main__":
    main()
