# This was a dumb idea 

After seeing Bad Apple!! run on everything from graphing calculators to smart toasters, a thought occurred to me: what if we went in the *opposite* direction? What if we ran it on the worst, most ridiculously low-resolution display possible?

So, I took that as a personal challenge.

I present to you: the full shadow art PV, subjected to the glorious, flickering torment of a tiny 8x8 LED matrix. That's 64 entire pixels of pure, unadulterated danmaku.

---

### The Final Result: A Spectacle of Light and Shadow

Behold, the fruits of my obsession. It's beautiful. It's cursed. It's Bad Apple!!

**[INSERT A GIF OR VIDEO OF YOUR PROJECT RUNNING HERE]**

![](placeholder_for_your_image.jpg)

---

## ✨ How This Incident Was Resolved (The Tech Stuff)

This isn't just a simple video player. Oh no. To cram 2008 onto a $4 microcontroller, some... *creative liberties* were taken.

* **Brute Force Overclocking:** The Raspberry Pi Pico's CPU has been respectfully encouraged to run at 250 MHz, far beyond its usual 133 MHz. Cause Marisa would do the same for no real reason whatsoever
* **Binary Soul-Streaming:** The entire video is converted into a raw binary file of pixel data. The Pico reads this file directly from its flash memory, one frame at a time, so it never runs out of RAM. It's like a digital grimoire of images.
* **Pre-Rotated :** The frames are pre-rotated 90 degrees on a PC before being sent to the Pico, to save precious CPU cycles for what really matters: displaying the animation. I did this for my specific setup, you may not need it in yours 
* **Watchdog of the Hakurei Shrine:** A watchdog timer is implemented. If the code ever freezes (perhaps from witnessing something it shouldn't have), the Pico automatically reboots itself.
---

## 🛠️ What You'll Need to Recreate This 8K display technology : 

### Hardware
* A **Raspberry Pi Pico** (The heart of the spell)
* An **8x8 LED Matrix Display** (The vessel)
* A **Pushbutton** (The trigger)
* Some jumper wires and a breadboard

### Software
* A PC with **Python** installed.
* **Thonny IDE** for communicating with the Pico.
* The Python libraries `opencv-python` and `Pillow`. Install them with:
    ```bash
    pip install opencv-python Pillow
    ```

---

## 📜 The Incantation (Setup Guide)

### Step 1: Wire the Components

Connect everything according to the ancient texts (or this diagram). This project uses the standard hardware SPI pins, so the wiring is crucial!

| 8x8 Matrix Pin | Pico Physical Pin | Pico GPIO Pin |
| :--- | :--- | :--- |
| **DIN** | Pin 25 | **GP19** |
| **CLK** | Pin 24 | **GP18** |
| **CS** | Pin 22 | **GP17** |
| **VCC** | Pin 40 | **VBUS (5V)** |
| **GND** | Pin 38 | **GND** |

### Step 2: Prepare the Frames on Your PC

1.  Download the original Bad Apple!! video (or any video you want to subject to this process).
2.  Run the `video_converter_rotated.py` script on your PC. It will process the video and create a file named `frames.bin`. This is your animation data, pre-rotated and ready for the Pico.

### Step 3: Upload to the Pico

1.  Connect your Pico to your computer and open Thonny.
2.  Upload the following files to the Pico's root directory:
    * `main.py`
    * `max7219.py`
    * `frames.bin` (the file you just created)

3.  Run `main.py` from Thonny, and the magic will begin!

---

## 🎮 Controls

* **Short Press:** Play or Pause the animation.
* **Long Press (2 seconds):** Restart the animation from the beginning.
* **At the End:** When the video finishes, it will display a replay icon. Press the button once to loop it.

---

## 🌟 Future Work & Potential Incidents

The current method works great, but the ultimate challenge would be to **stream the video directly from a PC in real-time**.

This would involve a more complex setup:
1.  A PC-side application (likely in C++ for performance) that processes video from a file or camera on the fly.
2.  This application would send the 8x8 frame data over the USB-Serial connection.
3.  The Pico's code would need to be modified to listen for this incoming serial data, buffer it, and display it, likely using both CPU cores to keep things from lagging.

It's a tricky incident to resolve, but definitely a cool direction for this project to go!

---

If you thought this project was cool, please consider giving it a ⭐ on GitHub! It's greatly appreciated.
