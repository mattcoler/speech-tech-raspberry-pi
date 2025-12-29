# Unit 1: Hardware setup and first audio program

⏱️ **Time:** 90 minutes  
🎯 **Goal:** Get your Raspberry Pi running and record your first audio

## Learning objectives

By the end of this unit, you will:
- Set up Raspberry Pi with SSH access (no monitor needed)
- Understand the audio hardware pathway
- Install Python audio libraries
- Record and play back audio using Python

## Prerequisites checklist

Before starting, make sure you have:
- [ ] Raspberry Pi 5 with power supply
- [ ] MicroSD card (32GB+) with USB-C card reader
- [ ] USB audio device (microphone + headphones or combo)
- [ ] Laptop with WiFi
- [ ] Your WiFi network name and password

---

## Part 1: Understanding the basics (10 minutes)

### What is SSH?

SSH (Secure Shell) is a way to control one computer from another using text commands. Think of it like remote desktop, but using the command line instead of a graphical interface.

**Why we use SSH:**
- No need for extra keyboard or monitor for the Pi
- Work comfortably from your laptop
- Easy to copy and paste commands
- This is how professionals manage servers

### What is the command line?

The command line (or terminal) is a text-based interface for controlling your computer.

**Basic command structure:**
```
command -option argument
```

**Example:**
```bash
ls -la /home/pi
```
- `ls`: list files (the command)
- `-la`: options (long format, show all)
- `/home/pi`: which folder (the argument)

Don't worry if this feels unfamiliar - we'll practice together!

---

## Part 2: Raspberry Pi setup (30 minutes)

### Step 1: Download Raspberry Pi Imager

1. Go to: https://www.raspberrypi.com/software/
2. Download for your operating system (Mac/Windows/Linux)
3. Install and open it

### Step 2: Prepare the SD card

1. Insert your microSD card using the USB-C reader
2. In Raspberry Pi Imager:
   - **Device:** Raspberry Pi 5
   - **OS:** Raspberry Pi OS (64-bit)
   - **Storage:** Your SD card

⚠️ **Warning:** This will erase everything on the SD card!

### Step 3: Configure settings (very important!)

Click the **gear icon** ⚙️ (bottom right) and configure:
```
Hostname: raspberrypi
Enable SSH: ✅ YES (use password authentication)
Username: pi
Password: [choose something memorable]
Configure WiFi: ✅ YES
  SSID: [your network name]
  Password: [your WiFi password]
Locale settings:
  Timezone: [your timezone]
  Keyboard layout: [your keyboard]
```

Click **Save**, then **Write**. This takes 5-10 minutes.

### Step 4: First boot

1. Remove SD card from your computer
2. Insert into Raspberry Pi (slot on underside)
3. Connect power supply
4. Wait 60 seconds (green LED will blink)

### Step 5: Connect via SSH

**Find your Pi on the network:**
```bash
ping raspberrypi.local
```

If this works, you'll see:
```
64 bytes from raspberrypi.local (192.168.0.195): icmp_seq=0 time=5.123 ms
```

Press Ctrl+C to stop.

**Connect:**
```bash
ssh pi@raspberrypi.local
```

First time you'll see a security warning:
```
The authenticity of host 'raspberrypi.local' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

Enter your password (characters won't show - this is normal).

**Success!** You should see:
```
pi@raspberrypi:~ $
```

### ✅ Checkpoint 1: Verify connection

Run these commands:
```bash
# Check Python version
python3 --version

# Check current directory
pwd

# List files
ls -la

# Check disk space
df -h
```

**Expected:**
- Python 3.11 or newer
- Current directory: `/home/pi`
- At least 20GB free space

<details>
<summary>❌ Troubleshooting: Can't connect</summary>

**Problem:** `ping raspberrypi.local` doesn't work

**Solutions:**
1. Wait another minute (first boot is slow)
2. Check Pi's LED is blinking
3. Find IP on your router's device list
4. Use IP instead: `ssh pi@192.168.0.195`
5. Re-image SD card with correct WiFi settings

**Problem:** Connection refused

**Solutions:**
1. Make sure SSH was enabled in settings
2. Re-image the SD card
3. Double-check WiFi password was correct
</details>

---

## Part 3: Understanding audio hardware (15 minutes)

### The audio pipeline
```
Microphone → USB sound card → Linux (ALSA) → Python (PyAudio)
```

**ALSA** (Advanced Linux Sound Architecture): The system that connects audio hardware to software. Think of it as the traffic controller for audio.

### Check audio devices

**Plug in your USB audio device** (microphone/headphones).

**List playback devices:**
```bash
aplay -l
```

**List recording devices:**
```bash
arecord -l
```

**Example output:**
```
card 2: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

**Understanding this:**
- `card 2`: Card number (like a shelf number)
- `device 0`: Device on that card
- We reference this as `hw:2,0`

### Test audio playback
```bash
# Play a test tone (440 Hz, 2 seconds)
speaker-test -t sine -f 440 -c 2 -l 1
```

You should hear a tone for about 2 seconds.

### Test audio recording
```bash
# Record 5 seconds
arecord -d 5 -f cd test.wav

# Play it back
aplay test.wav
```

Say something while recording. Do you hear yourself?

### ✅ Checkpoint 2: Audio working

- [ ] Heard the test tone
- [ ] Recorded and played back your voice
- [ ] Voice is clear (not too quiet or distorted)

<details>
<summary>❌ Troubleshooting: No sound</summary>

**Playback issues:**
```bash
# Open audio mixer
alsamixer
```
- Press F6 to select your device
- Use arrow keys to adjust volume
- Press M to unmute (look for "MM" - means muted)
- Press Esc to exit

**Recording issues:**
- Check microphone is not muted in `alsamixer`
- Increase capture volume (up arrow)
- Try speaking louder
- Check USB device is properly connected
</details>

---

## Part 4: Install Python libraries (10 minutes)

### Update system
```bash
# Update package list
sudo apt update

# Upgrade packages (optional, takes 5-10 min)
sudo apt upgrade -y
```

**What is `sudo`?** It means "do this as administrator" (like running as admin on Windows).

### Install audio libraries
```bash
sudo apt install -y portaudio19-dev python3-pyaudio
```

**What we installed:**
- `portaudio19-dev`: Low-level audio library
- `python3-pyaudio`: Python interface to PortAudio

### Verify installation
```bash
python3 -c "import pyaudio; print(pyaudio.__version__)"
```

Expected: `0.2.11` (or similar)

### Test device detection

Create a test script:
```bash
nano list_devices.py
```

Paste this code:
```python
import pyaudio

# Create PyAudio object
p = pyaudio.PyAudio()

# Get number of audio devices
print(f"Number of audio devices: {p.get_device_count()}")

# List all devices
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"\nDevice {i}: {info['name']}")
    print(f"  Max input channels: {info['maxInputChannels']}")
    print(f"  Max output channels: {info['maxOutputChannels']}")

p.terminate()
```

Save: Ctrl+O, Enter, Ctrl+X

Run it:
```bash
python3 list_devices.py
```

**Look for:**
- Device with `maxInputChannels > 0` (can record)
- Device with `maxOutputChannels > 0` (can play)
- Note the device numbers

### ✅ Checkpoint 3: Python ready

- [ ] PyAudio imports without error
- [ ] Script shows your USB device
- [ ] Device has both input and output channels

---

## Part 5: Your first audio program (25 minutes)

### Understanding audio streams

An **audio stream** is like a water hose:
- Data flows continuously (not all at once)
- We read small chunks repeatedly
- This enables real-time processing

**Why streams?**
- Recording 5 seconds all at once = too much memory
- Instead: grab small pieces (chunks) continuously
- Same concept as Netflix video streaming

### The complete program

See the complete code in [`hello_audio.py`](./hello_audio.py) in this folder.

### Understanding the code

**Part 1: Setup**
```python
CHUNK = 1024          # How many samples to grab at once
FORMAT = pyaudio.paInt16  # 16-bit audio (numbers from -32768 to 32767)
CHANNELS = 1          # Mono (1 channel)
RATE = 44100          # 44100 samples per second (CD quality)
RECORD_SECONDS = 5
```

**Part 2: Recording loop**
```python
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
```

**The math:** 44100 / 1024 × 5 = ~215 iterations

**Part 3: Saving**
```python
wf = wave.open(OUTPUT_FILENAME, 'wb')  # 'wb' = write binary
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
```

**Part 4: Playback**
```python
data = wf.readframes(CHUNK)
while data:
    stream.write(data)
    data = wf.readframes(CHUNK)
```

### Run the program
```bash
python3 hello_audio.py
```

**Expected behavior:**
1. Prints "Recording..."
2. Records for 5 seconds (start talking!)
3. Prints "Recording finished"
4. Prints "Saving to recording.wav..."
5. Prints "Playing back recording..."
6. You hear your voice
7. Prints "Playback finished"

### Verify it worked
```bash
# Check file exists and size
ls -lh recording.wav

# Should be around 800KB for 5 seconds

# Play it again
aplay recording.wav
```

### ✅ Final checkpoint

- [ ] Program runs without errors
- [ ] You recorded your voice
- [ ] Playback sounds like you
- [ ] File `recording.wav` exists

<details>
<summary>❌ Troubleshooting: Common errors</summary>

**Error:** `IOError: Invalid sample rate`  
**Solution:** Your device doesn't support 44100 Hz. Change `RATE = 48000` in the code.

**Error:** `OSError: Device unavailable`  
**Solution:** Another program is using the device. Close other programs and try again.

**Problem:** Recording is silent  
**Solutions:**
1. Check microphone not muted: `alsamixer`
2. Increase recording volume (capture)
3. Verify device number: run `list_devices.py`
4. Speak louder and closer to mic

**Problem:** Recording sounds distorted  
**Solutions:**
1. Reduce input volume in `alsamixer`
2. Move further from microphone
3. Try `CHANNELS = 2` for stereo
</details>

---

## Exercises

Try modifying the program:

1. **Longer recording**: Change `RECORD_SECONDS = 10`
2. **Stereo**: Change `CHANNELS = 2`
3. **Lower quality**: Change `RATE = 16000` (can you hear the difference?)
4. **Add countdown**: Print "3... 2... 1... Go!" before recording

Example countdown:
```python
import time

print("Recording in...")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)
print("Go!")
```

---

## What you learned

✅ Topics covered:
- SSH and remote control
- Command line basics
- Audio hardware detection
- Python audio streams
- Recording and playback
- WAV file format
- Basic troubleshooting

✅ Skills gained:
- Set up Raspberry Pi headlessly
- Navigate Linux command line
- Install Python libraries
- Write and run Python scripts
- Debug audio issues

---

## Next steps

Great job! You now have:
- Working Raspberry Pi with SSH
- Python audio environment
- Your first audio program

**Next:** [Unit 2: Python audio basics →](../unit-02-audio-basics/)

In Unit 2, you'll learn:
- Working with audio as numbers
- Numpy arrays for audio processing
- Visualizing waveforms
- Building a voice memo app

---

## Quick reference

**Connect to Pi:**
```bash
ssh pi@raspberrypi.local
```

**Check audio devices:**
```bash
arecord -l    # recording devices
aplay -l      # playback devices
```

**Test audio:**
```bash
arecord -d 5 test.wav && aplay test.wav
```

**Run program:**
```bash
python3 hello_audio.py
```
