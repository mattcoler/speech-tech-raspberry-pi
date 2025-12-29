# Unit 2: Python audio basics

**Time needed:** Approximately 90 minutes

In Unit 1, you recorded and played back audio using pyaudio. But what's actually happening under the hood? In this unit, you'll learn that audio is just numbers, and once you understand that, you can do interesting things with those numbers.

## What you'll learn

By the end of this unit, you'll be able to:
- Explain how audio is stored as numbers in your computer
- Use numpy arrays to work with audio data
- Adjust the volume of audio recordings
- Build a simple audio recorder with volume control

## Prerequisites

Before starting this unit, you should have:
- Completed Unit 1 (Raspberry Pi setup and first audio program)
- Successfully run hello_audio.py and heard yourself recorded
- SSH access to your Raspberry Pi

## The big idea: audio is just numbers

When you speak into a microphone, your voice creates vibrations in the air. The microphone converts these vibrations into electrical signals, and your computer converts those signals into numbers. Lots and lots of numbers.

Here's the surprising part: that's all digital audio is. A long list of numbers representing the air pressure at thousands of moments per second.

When you recorded yourself saying "hello" in Unit 1, your Raspberry Pi created approximately 160,000 numbers (5 seconds times 32,000 numbers per second). Each number represents how much the microphone's sensor moved at one tiny instant in time.

## Setting up

First, let's create a new folder for Unit 2's code.

Connect to your Pi via SSH:

    ssh pi@192.168.0.195

Create the unit 2 folder:

    mkdir ~/unit-02-audio-basics
    cd ~/unit-02-audio-basics

Install numpy (we need this for working with arrays):

    pip3 install numpy --break-system-packages

You'll see some installation messages. Wait until you see "Successfully installed numpy" and get your command prompt back.

**What's numpy?** Numpy is a Python library that makes working with large lists of numbers very fast. Instead of regular Python lists, numpy gives us "arrays" which are optimized for numerical calculations. When you're working with 160,000 audio samples, this speed difference really matters.

## Part 1: Seeing audio as numbers

Let's write a program that shows you what audio data actually looks like.

Create a new file:

    nano audio_as_numbers.py

Copy this code into nano:

    import pyaudio
    import numpy as np

    # Audio settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 32000
    CHUNK = 1024
    RECORD_SECONDS = 2

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording for 2 seconds...")
    print("Say something!")

    # Record audio
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert the raw audio data to a numpy array
    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Show some statistics
    print(f"\nAudio statistics:")
    print(f"Total number of samples: {len(audio_array)}")
    print(f"Recording duration: {len(audio_array) / RATE:.2f} seconds")
    print(f"Minimum value: {audio_array.min()}")
    print(f"Maximum value: {audio_array.max()}")
    print(f"\nFirst 10 samples: {audio_array[:10]}")
    print(f"Last 10 samples: {audio_array[-10:]}")

    # Calculate average loudness
    average_loudness = np.abs(audio_array).mean()
    print(f"\nAverage loudness: {average_loudness:.2f}")

Save and exit nano (press Ctrl+O, then Enter, then Ctrl+X).

Run the program:

    python3 audio_as_numbers.py

When you see "Say something!", speak clearly into your microphone for about 2 seconds. You'll see output like this:

    Recording for 2 seconds...
    Say something!
    Recording finished.

    Audio statistics:
    Total number of samples: 64000
    Recording duration: 2.00 seconds
    Minimum value: -1247
    Maximum value: 1523
    First 10 samples: [-12  15  -8   3  45 -67  89 -34  12  -5]
    Last 10 samples: [  2  -3   1   4  -2   1  -1   0   1  -2]

    Average loudness: 245.67

**What this tells you:**
- Your 2-second recording has 64,000 samples (32,000 per second)
- Each sample is a number, typically between -32,768 and +32,767
- Positive numbers mean the microphone moved one direction
- Negative numbers mean it moved the other direction
- Larger absolute values mean louder sounds
- The average loudness tells you how energetic the recording was overall

**Why are the numbers between -32,768 and 32,767?** We're using 16-bit audio (paInt16). A 16-bit number can store 2 to the power of 16 equals 65,536 different values. Since we need both positive and negative values (sound moves in two directions), we split this range in half: -32,768 to +32,767.

**Checkpoint:** Run the program a few times, trying different things. Speak loudly versus quietly. Say nothing (stay silent). Clap your hands. Notice how the minimum, maximum, and average loudness values change based on how loud you are.

## Part 2: Controlling volume

Now that you understand audio is numbers, here's something cool: to make audio louder or quieter, you just multiply all the numbers by some factor.

- Multiply by 2.0 equals twice as loud
- Multiply by 0.5 equals half as loud
- Multiply by 0.0 equals silence

Let's build a program that demonstrates this.

Create a new file:

    nano volume_control.py

Copy this code:

    import pyaudio
    import numpy as np

    # Audio settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 32000
    CHUNK = 1024
    RECORD_SECONDS = 3

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Record audio
    print("Recording for 3 seconds...")
    print("Speak at your normal volume.")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    print("Recording finished.\n")

    # Convert to numpy array
    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate original loudness
    original_loudness = np.abs(audio_array).mean()
    print(f"Original average loudness: {original_loudness:.2f}")

    # Play original
    print("\nPlaying ORIGINAL recording...")
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True
    )
    stream.write(audio_array.tobytes())
    stream.stop_stream()
    stream.close()

    # Create quieter version (50% volume)
    quiet_array = (audio_array * 0.5).astype(np.int16)
    quiet_loudness = np.abs(quiet_array).mean()
    print(f"\nQuiet version loudness: {quiet_loudness:.2f}")
    print("Playing QUIET version (50% volume)...")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True
    )
    stream.write(quiet_array.tobytes())
    stream.stop_stream()
    stream.close()

    # Create louder version (150% volume)
    loud_array = (audio_array * 1.5).astype(np.int16)
    loud_loudness = np.abs(loud_array).mean()
    print(f"\nLoud version loudness: {loud_loudness:.2f}")
    print("Playing LOUD version (150% volume)...")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True
    )
    stream.write(loud_array.tobytes())
    stream.stop_stream()
    stream.close()

    audio.terminate()
    print("\nDone! Notice how the loudness values changed.")

Save and exit (Ctrl+O, Enter, Ctrl+X).

Run it:

    python3 volume_control.py

You'll hear three playbacks:
1. Your original recording
2. A quieter version (50% volume)
3. A louder version (150% volume)

**Key insight:** By multiplying the audio array by different numbers, we changed the volume. This is fundamentally how volume controls work in audio software.

**Why the astype part?** When we multiply by 0.5 or 1.5, numpy gives us floating-point numbers (numbers with decimals). But pyaudio needs 16-bit integers to play audio. The `.astype(np.int16)` converts the floating-point array back to integers. This is like rounding 1.7 to 2, except it handles the conversion for all 64,000 numbers at once.

## Part 3: Simple recorder with volume control

Now let's combine what you've learned into a simple practical tool: a recorder that lets you choose the volume when you play back.

Create the recorder:

    nano simple_recorder.py

Copy this code:

    import pyaudio
    import numpy as np

    # Audio settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 32000
    CHUNK = 1024

    print("Simple Audio Recorder with Volume Control")
    print("=" * 50)

    # Get recording duration
    while True:
        try:
            duration = int(input("\nHow many seconds to record? (1-10): "))
            if 1 <= duration <= 10:
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")

    # Record
    audio = pyaudio.PyAudio()

    print(f"\nRecording for {duration} seconds...")
    print("Speak now!")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    print("Recording finished!")

    # Convert to numpy array
    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate loudness
    loudness = np.abs(audio_array).mean()
    print(f"Average loudness: {loudness:.2f}")

    # Playback loop
    while True:
        print("\n" + "=" * 50)
        print("What would you like to do?")
        print("1. Play at normal volume")
        print("2. Play quieter (50%)")
        print("3. Play louder (150%)")
        print("4. Play at custom volume")
        print("5. Quit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            play_array = audio_array
            print("\nPlaying at 100% volume...")
        
        elif choice == '2':
            play_array = (audio_array * 0.5).astype(np.int16)
            print("\nPlaying at 50% volume...")
        
        elif choice == '3':
            play_array = (audio_array * 1.5).astype(np.int16)
            print("\nPlaying at 150% volume...")
        
        elif choice == '4':
            while True:
                try:
                    volume = float(input("Enter volume multiplier (0.1 to 3.0): "))
                    if 0.1 <= volume <= 3.0:
                        break
                    print("Please enter a number between 0.1 and 3.0")
                except ValueError:
                    print("Please enter a valid number")
            
            play_array = (audio_array * volume).astype(np.int16)
            print(f"\nPlaying at {volume * 100:.0f}% volume...")
        
        elif choice == '5':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
            continue
        
        # Play the audio
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True
        )
        stream.write(play_array.tobytes())
        stream.stop_stream()
        stream.close()
        
        print("Playback finished.")

    audio.terminate()

Save and exit (Ctrl+O, Enter, Ctrl+X).

Run your recorder:

    python3 simple_recorder.py

**Try these things:**
1. Record a 5-second message
2. Play it back at normal volume (option 1)
3. Play it quieter (option 2)
4. Play it louder (option 3)
5. Try the custom volume option (option 4) with different values

**What this program demonstrates:**
- Recording audio and storing it in memory
- Processing audio by multiplying arrays
- Playing back the same recording at different volumes
- Building an interactive command-line interface
- Using a loop to let users repeat actions

## What you've learned

Take a moment to appreciate what you can now do:

1. **Understand audio data:** You know that audio is stored as arrays of numbers, with each number representing the air pressure at one moment
2. **Work with numpy:** You can create arrays, do math on them, and convert them for playback
3. **Control volume:** By multiplying arrays, you can make audio louder or quieter
4. **Build applications:** You combined all these skills to create a working audio recorder with volume control

These are fundamental skills for any speech technology work. Every speech recognition system, audio editor, or voice assistant builds on these same concepts.

## Troubleshooting

**Problem: I get "No module named 'numpy'" error**

Install numpy:

    pip3 install numpy --break-system-packages

If that fails, try:

    sudo apt-get update
    sudo apt-get install python3-numpy

**Problem: The playback sounds distorted when I make it louder**

You've hit "clipping." When you multiply by a large number (like 2.0 or higher), some values exceed 32,767 (the maximum for 16-bit audio). These get clipped back to 32,767, which causes distortion.

Try using smaller multipliers, like 1.2 or 1.5 instead of 2.0 or higher.

**Problem: My recordings have background noise**

That's normal! All microphones pick up some background noise. Some things you can try:
- Record in a quieter room
- Speak closer to the microphone
- Use a lower volume multiplier when playing back

## Exercises

Ready to practice? Try these challenges:

**Exercise 1: Half-speed playback**

Modify volume_control.py to play audio at half speed. Hint: you'll need to change the RATE parameter when playing back.

**Exercise 2: Reverse playback**

Create a program that records audio and plays it backwards. Hint: numpy arrays can be reversed with `array[::-1]`.

**Exercise 3: Show the numbers**

Modify simple_recorder.py to also show the minimum and maximum values in the recording, not just the average loudness.

## What's next

In Unit 3, you'll learn about **speech recognition fundamentals**. You'll use your recording skills to capture speech and then transcribe it to text using recognition libraries. This is where we start getting into actual speech technology!

Before moving on, make sure you:
- Understand that audio is stored as arrays of numbers
- Can manipulate audio by doing math on arrays
- Have successfully run the simple recorder program
- Feel comfortable with the numpy array concepts

---

**Navigation:**
- Previous: [Unit 1: Setting up your Raspberry Pi](../unit-01-setup/README.md)
- Next: [Unit 3: Speech recognition fundamentals](../unit-03-speech-recognition/README.md)
- [Back to Module 1](../README.md)
- [Course Home](../../README.md)
