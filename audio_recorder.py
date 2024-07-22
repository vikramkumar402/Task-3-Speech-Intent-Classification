import pyaudio
import wave
import os

def record_audio(filename, duration=5, sample_rate=16000, channels=1, chunk=1024):
    """
    Record audio from the microphone and save it as a WAV file.
    
    :param filename: Name of the output WAV file
    :param duration: Duration of the recording in seconds
    :param sample_rate: Sample rate of the audio
    :param channels: Number of audio channels (1 for mono, 2 for stereo)
    :param chunk: Number of frames per buffer
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved as {filename}")

# Main execution
if __name__ == "__main__":
    output_directory = "recorded_audio"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    while True:
        input("Press Enter to start recording (or 'q' to quit)...")
        if input().lower() == 'q':
            break

        filename = os.path.join(output_directory, f"recorded_audio_{len(os.listdir(output_directory)) + 1}.wav")
        record_audio(filename)

    print("Recording session ended.")