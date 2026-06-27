from pygame import *
from sounddevice import *

fs = 44100
chunk = 1024
width, height = 800, 400

init()

screen = display.set_mode((width, height))
display.set_caption("Audio Visualizer")
clock = time.Clock()

data = [0.0] * chunk

def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)    
    data = [
        sample * (height // 2) for sample in indata[:, 0].tolist()
    ]
    stream = InputStream(callback=audio_callback, channels=1,
                          samplerate=fs, blocksize=chunk, dtype='float32')
    stream.start()

    run = True
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False

        screen.fill((0, 0, 0))
        points = []

        for i, sample in enumerate(data):
            x = int(i * (width / chunk))
            y = int((height // 2) - sample)
            points.append((x, y))

        if len(points) > 1:
            draw.lines(screen, (0, 255, 0), False, points, 2)

        display.update()
        clock.tick(60)
    stream.stop()
    quit()