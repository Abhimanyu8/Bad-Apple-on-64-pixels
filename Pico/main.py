import machine
import utime
from max7219 import Matrix8x8

# --- Overclocking ---
machine.freq(250000000)

# --- Pin Configuration ---
led_onboard = machine.Pin(25, machine.Pin.OUT)
spi = machine.SPI(0, baudrate=10000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19))
cs = machine.Pin(17, machine.Pin.OUT)
button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

# --- Global Variables & State ---
is_paused = True
video_finished = False # New state to track if the video has ended

# --- Animation & Display ---
# Initialize with the standard driver, providing 1 for the number of matrices
display = Matrix8x8(spi, cs, 1)
display.brightness(2)

# --- Constants for Streamed Data ---
# Make sure to upload the 'frames.bin' file
FRAMES_FILE = "frames.bin"
FRAME_SIZE_BYTES = 8

FRAME_RATE = 30
FRAME_DELAY_MS = 1000 // FRAME_RATE

# --- Main Animation Loop (Single Core) ---
def play_animation():
    """Main core for displaying video frames from a binary file."""
    global is_paused, video_finished
    
    print("Starting animation. Press to play/pause. Long press (2s) to restart.")
    
    # !! Caution !! Icons are pre-rotated 90 degrees clockwise
    pause_icon = bytes([0x00, 0x66, 0x66, 0x00, 0x00, 0x66, 0x66, 0x00])
    replay_icon = bytes([0x3C, 0x42, 0x99, 0x99, 0x99, 0x81, 0x42, 0x3C]) # Replay symbol

    # --- Watchdog Timer for 24/7 Stability ---
    wdt = machine.WDT(timeout=2000)
    
    try:
        with open(FRAMES_FILE, "rb") as frames_file:
            while True:
                wdt.feed() # Feed the watchdog to prevent a reboot
                
                # --- Button Handling Logic ---
                if button.value() == 0:
                    press_start_time = utime.ticks_ms()
                    utime.sleep_ms(50) # Debounce

                    while button.value() == 0:
                        utime.sleep_ms(10)
                    
                    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)

                    if video_finished: # If video is over, any press is a replay
                        print("Button pressed. Replaying video.")
                        frames_file.seek(0)
                        video_finished = False
                        is_paused = False # Start playing immediately
                        continue
                    elif press_duration >= 2000: # Long press during playback
                        print("Long press detected. Restarting animation.")
                        frames_file.seek(0)
                        is_paused = False
                        continue
                    else: # Short press during playback
                        is_paused = not is_paused
                        print(f"State changed: Paused = {is_paused}")

                led_onboard.toggle()

                # --- State Handling ---
                if video_finished:
                    for i in range(FRAME_SIZE_BYTES):
                        display.buffer[i] = replay_icon[i]
                    display.show()
                    utime.sleep_ms(100)
                    continue
                
                if is_paused:
                    for i in range(FRAME_SIZE_BYTES):
                        display.buffer[i] = pause_icon[i]
                    display.show()
                    utime.sleep_ms(100)
                    continue

                # --- Frame Drawing ---
                start_time = utime.ticks_ms()
                
                frame_data = frames_file.read(FRAME_SIZE_BYTES)
                if not frame_data:
                    print("End of video. Press button to replay.")
                    video_finished = True
                    continue

                for i in range(FRAME_SIZE_BYTES):
                    display.buffer[i] = frame_data[i]
                display.show()
                
                time_taken = utime.ticks_diff(utime.ticks_ms(), start_time)
                sleep_duration = FRAME_DELAY_MS - time_taken
                
                if sleep_duration > 0:
                    utime.sleep_ms(sleep_duration)

    except OSError as e:
        print(f"Error: Could not open {FRAMES_FILE}. Is it uploaded? {e}")
    
    print("Animation finished.")
    display.fill(0)
    display.show()
    led_onboard.off()

# --- Main Execution ---
if __name__ == "__main__":
    play_animation()
