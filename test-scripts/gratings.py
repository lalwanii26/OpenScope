"""
gratings.py
"""

# Import necessary libraries
from camstim import Stimulus, SweepStim
from camstim import Foraging
from camstim import Window, Warp
import time
import datetime
import os
from psychopy import monitors, visual

# Define monitor parameters
dist = 15.0
wid = 52.0

# create a monitor
monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

# Create display window
window = Window(fullscr=True,
                # monitor= 'Gamma1.Luminance50',          # MS
                monitor = monitor,
                screen=1,
                warp=Warp.Spherical,)

#flashes
fl250_ds = [(0, 1200)]
# static
part2s  = 1200
sg_ds = [(part2s+0, part2s+480), (part2s+1800, part2s+2280), (part2s+3210, part2s+3750)]

# Get path of current file
path = os.path.dirname(os.path.abspath(__file__))

# fl250 = Stimulus.from_file(fl250_path, window)
# read color information from comma separated file
with open(path + r"\TestSequenceBWN.txt") as f:
    Color = f.readlines()
    Color = [x.split(',') for x in Color]
    Color = [x for x in Color if len(x) > 1]
    Color = [[y.strip() for y in x] for x in Color]
    # remove empty strings
    Color = [[y for y in x if y] for x in Color]
    # convert to float
    Color = [[float(y) for y in x] for x in Color]

# load our stimuli
# FFF implemented as a grating with fixed sf=0, ori=0, and ph=0
# contrast is updated every video frame according to the loaded stimulus sequence
fl250 = Stimulus(visual.GratingStim(window,
                    pos=(0, 0),
                    units='deg',
                    size=(300, 300),
                    mask="None",
                    texRes=256,
                    sf=0,
                    ),

    # a dictionary that specifies the parameter values
    # that will be swept or varied over time during the presentation of the stimulus
    sweep_params={
                # wokrs similarly like for loops
                # for a fixed contrast value, color is updated every video frame
               'Contrast': ([1], 0),
               'Color':(Color[0], 1)
               },
    sweep_length=0.1,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    # the number of times the entire stimulus sequence will be repeated
    runs=32,
    shuffle=False,
    save_sweep_table=True,
    )

# Standing (static) Grating with fixed sf, ori, and ph
# contrast is updated every video frame according to the loaded stimulus sequence
sg = Stimulus(visual.GratingStim(window,
                    pos=(0, 0),
                    units='deg',
                    size=(250, 250),
                    mask="None",
                    texRes=256,
                    sf=0.1,
                    ),

    # a dictionary that specifies the parameter values
    # that will be swept or varied over time during the presentation of the stimulus
    sweep_params={
                # wokrs similarly like for loops
                # for a fixed contrast value, color is updated every video frame
               'Contrast': ([1], 0),
               'Color': (Color[0],1),
               'SF': ([0.01], 2),
               'Ori': ([0.0], 3),
               'Phase': ([0], 4),
               },
    sweep_length=0.25,
    start_time=0.0,
    blank_length=0.0,
    blank_sweeps=0,
    # the number of times the entire stimulus sequence will be repeated
    runs=32,
    shuffle=False,
    save_sweep_table=True,
    kframes = 1,
    )

# ghg
# Define display sequence
fl250.set_display_sequence(fl250_ds)
sg.set_display_sequence(sg_ds)

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
               stimuli=[fl250, sg],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )

# add in foraging so we can track wheel, potentially give rewards, etc
f = Foraging(window=window,
            auto_update=False,
            params=params,
            nidaq_tasks={'digital_input': ss.di,
                         'digital_output': ss.do,})  #share di and do with SS
ss.add_item(f, "foraging")

# Run the SweepStim instance
ss.run()