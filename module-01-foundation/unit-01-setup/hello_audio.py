import pyaudio
import wave

# Audio recording parameters
CHUNK = 1024          # Number of frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1          # Mono audio
RATE = 44100          # Sample rate (CD quality)
RECORD_SECONDS = 5    # How long to record
OUTPUT_FILENAME = "recording.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open recording stream
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("Recording...")
frames = []  # Will store audio data here

# Record for specified number of seconds
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished")
stream.stop_stream()
stream.close()

# Save recording to WAV file
print(f"Saving to {OUTPUT_FILENAME}...")
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
print("File saved")

# Play back the recording
print("Playing back recording...")
wf = wave.open(OUTPUT_FILENAME, 'rb')

stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True
)

# Read and play data in chunks
data = wf.readframes(CHUNK)
while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
wf.close()
p.terminate()
print("Playback finished")
