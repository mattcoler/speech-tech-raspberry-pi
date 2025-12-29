# Glossary

Technical terms explained for beginners.

---

## A

### ALSA (Advanced Linux Sound Architecture)
The Linux system that manages audio hardware. Acts as a bridge between physical audio devices (microphones, speakers) and software that wants to use them. Think of it as the traffic controller for audio.

### Amplitude
How "loud" an audio signal is at any given moment. In digital audio, represented as numbers (e.g., from -32768 to +32767 for 16-bit audio).

### API (Application Programming Interface)
A set of functions that let programs talk to each other or to hardware. PyAudio is an API for working with audio.

---

## B

### Bit depth
How many bits are used to store each audio sample. Common values:
- 8-bit: 256 possible values (low quality)
- 16-bit: 65,536 possible values (CD quality)
- 24-bit: 16.7 million possible values (professional)

Higher bit depth = more detail and dynamic range.

### Buffer
A temporary storage area for data. In audio, we use buffers to hold chunks of audio samples before processing them.

---

## C

### Channel
An independent stream of audio. 
- Mono: 1 channel
- Stereo: 2 channels (left and right)
- Surround: 5.1 channels (6 total), 7.1 channels (8 total)

### Chunk
A small piece of audio data read from or written to a stream. Typically 512, 1024, or 2048 samples. Smaller chunks = lower latency but more CPU usage.

### Command line
A text-based interface for controlling a computer. Also called: terminal, shell, console, or bash.

---

## D

### dB (Decibel)
A unit for measuring sound intensity (volume). 
- 0 dB: Threshold of human hearing
- 60 dB: Normal conversation
- 120 dB: Threshold of pain
- Each +10 dB is roughly twice as loud to human ears

### Digital audio
Audio represented as numbers (samples) rather than continuous analog signals. Allows computers to store, process, and reproduce sound.

---

## F

### Format (audio)
How audio data is stored. Examples:
- WAV: Uncompressed, high quality, large files
- MP3: Compressed, smaller files, some quality loss
- FLAC: Compressed without quality loss

### Frame
In audio, usually refers to one sample from all channels. In stereo, 1 frame = 2 samples (left + right).

### Frequency
How many times per second a sound wave repeats. Measured in Hertz (Hz).
- 20 Hz: Lowest sound humans can hear
- 440 Hz: Musical note A
- 20,000 Hz: Highest sound young humans can hear

---

## H

### Hertz (Hz)
Unit of frequency meaning "cycles per second." 440 Hz = 440 vibrations per second.

---

## I

### IP address
A number that identifies a device on a network. Format: `192.168.0.195` (four numbers from 0-255). Like a phone number for computers.

---

## L

### Latency
The delay between an action and its result. In audio:
- Input latency: time between sound occurring and computer receiving it
- Output latency: time between computer processing and hearing result
- Lower latency = more responsive but requires more CPU

### .local domain
A special address that works on local networks. `raspberrypi.local` automatically finds your Pi without knowing its IP address.

---

## M

### Mono
Audio with one channel. All sound comes from one source (no left/right separation).

---

## P

### Port
A number that specifies which program should receive network data. SSH uses port 22.

### PyAudio
A Python library that provides an interface to PortAudio, making it easy to record and play audio in Python programs.

---

## R

### Rate (sample rate)
How many audio samples are captured per second. Measured in Hz.
- 8000 Hz: Phone quality
- 16000 Hz: Basic speech recognition
- 44100 Hz: CD quality
- 48000 Hz: Professional video
- 96000 Hz: High-end audio production

Higher rate = better quality but larger files.

---

## S

### Sample
A single measurement of audio at one point in time. Digital audio is thousands of samples per second.

### Sample rate
See "Rate" above.

### SSH (Secure Shell)
A protocol for securely controlling one computer from another over a network. Uses encryption to protect your password and commands.

### Stereo
Audio with two channels (left and right), creating a sense of space and direction.

### Stream
A continuous flow of data. In audio, we process streams in small chunks rather than loading entire files into memory.

---

## T

### Terminal
See "Command line."

---

## U

### USB (Universal Serial Bus)
A standard for connecting devices to computers. Most audio devices connect via USB.

---

## W

### WAV (Waveform Audio File Format)
An audio file format that stores uncompressed audio data. Large files but perfect quality.

### Waveform
A visual representation of audio, showing amplitude over time. Looks like a wavy line.

---

## Technical command terms

### `apt`
Package manager for Debian/Ubuntu/Raspberry Pi OS. Used to install software.

### `cd`
"Change directory" - navigate to different folders.

### `ls`
"List" - show files in current directory.

### `nano`
A simple text editor for the command line.

### `ping`
Send a signal to check if a device is reachable on the network.

### `pwd`
"Print working directory" - show current folder location.

### `sudo`
"Substitute user do" - run a command as administrator. Required for system-level changes.

### `ssh`
Command to connect to another computer securely.

---

## Need more help?

- Can't find a term? Open a GitHub issue
- Want more detail? Check the unit READMEs
- Still confused? Ask in GitHub Discussions
