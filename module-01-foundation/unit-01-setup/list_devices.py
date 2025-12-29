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

4. Commit message: `Add list_devices.py - utility to detect audio devices`

5. Click **"Commit changes"**

---

## Next: Create the glossary

1. Click **"Add file"** → **"Create new file"**

2. In the filename box, type:
```
   resources/glossary.md
