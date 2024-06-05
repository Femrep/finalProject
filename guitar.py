import numpy as np
import pyaudio
from PyQt5.QtCore import pyqtSignal, QObject

class NoteDetector(QObject):
    note_detected = pyqtSignal(tuple)  # Signal to emit the detected note position

    NOTE_MIN = 40       # E2
    NOTE_MAX = 88       # E6
    FSAMP = 48000       # Sampling frequency in Hz
    FRAME_SIZE = 2048   # How many samples per frame?
    FRAMES_PER_FFT = 16 # FFT takes average across how many frames?

    SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
    FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT

    note_played =[ 
        [330.63, 353.23, 373.99, 394.00, 417.30, 443.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25],
        [246.94, 261.63, 277.18, 293.66, 311.13],
        [196.00, 207.65, 220.00, 233.08, 246.94],
        [146.83, 155.56, 164.81, 174.61, 185.00, 196.00],
        [110.00, 116.54, 123.47, 130.81, 138.59, 146.83],
    ]

    def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
    def number_to_freq(self,n): return 440 * 2.0**((n-69)/12.0)

    def note_to_fftbin(self,n): return self.number_to_freq(n)/self.FREQ_STEP

    def __init__(self):
        super().__init__()
        self.buf = np.zeros(self.SAMPLES_PER_FFT, dtype=np.float32)
        self.num_frames = 0

        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                             channels=1,
                                             rate=self.FSAMP,
                                             input=True,
                                             frames_per_buffer=self.FRAME_SIZE)
        self.stream.start_stream()

        self.window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, self.SAMPLES_PER_FFT, False)))

        self.imin = max(0, int(np.floor(self.note_to_fftbin(self.NOTE_MIN - 1))))
        self.imax = min(self.SAMPLES_PER_FFT, int(np.ceil(self.note_to_fftbin(self.NOTE_MAX + 1))))

    def frequency_to_position(self, freq):
        for string, notes in enumerate(self.note_played):
            for fret, note_freq in enumerate(notes):
                if abs(note_freq - freq) < 1.0:  # Allow a small error margin
                    return (string+1, fret)
        return None

    def detect_notes(self):
        try:
            while self.stream.is_active():
                self.buf[:-self.FRAME_SIZE] = self.buf[self.FRAME_SIZE:]
                self.buf[-self.FRAME_SIZE:] = np.frombuffer(self.stream.read(self.FRAME_SIZE), np.int16)

                fft = np.fft.rfft(self.buf * self.window)
                fft -= self.noise_profile
                freq = (np.abs(fft[self.imin:self.imax]).argmax() + self.imin) * self.FREQ_STEP
                
                # Calculate the dB value
                
               
                position = self.frequency_to_position(freq)
                if position:
                    self.note_detected.emit(position)  # Emit the signal with the detected position
                   
        except IOError as e:
            print(f"Error reading from stream: {e}")
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.stream.stop_stream()
            self.stream.close()
