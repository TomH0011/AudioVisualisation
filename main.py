import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave
import sys


def retreiveFile(filename):
    # Keep it low or memory will go boom (advise not higher than 4096)
    chunk = 2048

    try:
        # Opening the I/O
        # 'rb' means to read-only
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()

        # True in this case means to play and not record I believe
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        plt.ion()  # Keep it interactive as you won't be able to statically redraw the plot for each frame
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)
        ax.set_title("Sound Wave")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Amplitude")
        ax.set_xlim(0, chunk / wf.getframerate())  # Set initial x-axis limits
        ax.set_ylim(0, 2 ** 15 - 1)  # Set y-axis limits for 16-bit audio

        try:
            data = wf.readframes(chunk)
            total_frames_played = 0

            while data:
                stream.write(data)

                # Convert the data to numpy array for plotting
                signal = np.frombuffer(data, dtype="int16")

                # Update the x-axis to reflect the time elapsed
                time = np.linspace(total_frames_played / wf.getframerate(),
                                   (total_frames_played + len(signal)) / wf.getframerate(),
                                   len(signal))

                # Update the plot with new data instead of redrawing the plot otherwise it will be very choppy
                line.set_xdata(time)
                line.set_ydata(signal)
                ax.set_xlim(time[0], time[-1])  # Dynamically adjust x-axis

                # Redraw the plot
                plt.pause(0.01)  # Small pause to allow the plot to update

                total_frames_played += len(signal)

                data = wf.readframes(chunk)

            plt.draw()
        except KeyboardInterrupt:
            print("Playback interrupted.")
        except Exception as e:
            print(f"An error occurred: {e}")

        stream.close()
        p.terminate()
        plt.ioff()
        plt.show()
    except FileNotFoundError as e:
        (print("you may have an issue with the file name"))


# This is just an example
# Download a wav file or convert to a wav file and copy the path as the parameter
if __name__ == "__main__":
    retreiveFile("D:\\Google downloads\\showreel-music-promo-advertising-opener-vlog-background-intro-theme-261601.wav")

# Issues currently, It's VERY loud Another is when amplitudes start peaking the speed of frames being read drops
# leading to choppy audio and slow graph drawing Maybe solve via multi threading, have 1 core play sound and another
# draw??
