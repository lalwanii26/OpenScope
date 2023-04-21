"""
brain_observatory_stimulus.py
"""

# Import necessary libraries 
from psychopy import monitors, visual
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
import os

# Define monitor parameters 
dist = 15.0
wid = 52.0

# # create a monitor
monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

# Create display window
window = Window(fullscr=True,
                # monitor= 'Gamma1.Luminance50',          # MS 
                monitor = monitor,
                screen=1,
                warp=Warp.Spherical,)


## Get path of current file
path = os.path.dirname(os.path.abspath(__file__))

# fl250 = Stimulus.from_file(fl250_path, window) 

## read color information from comma separated file
with open(path + r"\TestSequenceBWN.txt") as f:
    Color = f.readlines()
    Color = [x.split(',') for x in Color]   
    Color = [x for x in Color if len(x) > 1]
    Color = [[y.strip() for y in x] for x in Color]
    ## remove empty strings
    Color = [[y for y in x if y] for x in Color]
    ## convert to float
    Color = [[int(y) for y in x] for x in Color]

# Create a stimulus using a grating with varying color sweeps 
fl250 = Stimulus(visual.GratingStim(window,
                    pos=(0, 0),
                    units='deg',
                    size=(300, 300),
                    mask="None",
                    texRes=256,
                    sf=0,
                    ),
    sweep_params={
               'Contrast': ([1], 0),
               'Color':(Color[0], 1)
               },
    sweep_length=0.1,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs=75,
    shuffle=False,
    save_sweep_table=True,
    )


# ghg
# Define display sequence 
fl250_ds = [(0, 1200)]
fl250.set_display_sequence(fl250_ds)

# kwargs
# Set keyword argumets for SweepStim instance 
params = {
    'syncpulse': True,
    'syncpulseport': 1,
    'syncpulselines': [4, 7],  # frame, start/stop
    'trigger_delay_sec': 0.0,
    'bgcolor': (-1,-1,-1),
    'eyetracker': False,
    'eyetrackerip': "W7DT12722",
    'eyetrackerport': 1000,
    'syncsqr': True,
    'syncsqrloc': (0,0), 
    'syncsqrfreq': 60,
    'syncsqrsize': (100,100),
    'showmouse': True
}


# Create SweepStim instance
ss = SweepStim(window,
               stimuli=[fl250],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )

# Run the SweepStim instance
ss.run()
