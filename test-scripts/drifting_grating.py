"""
brain_observatory_stimulus.py
"""
# Import required modules
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
from psychopy import monitors, visual
import os

# Define monitor settings 
dist = 15.0
wid = 52.0

# Create a monitor object 
monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

# Create display window
window = Window(fullscr=True,
                # monitor= 'Gamma1.Luminance50',          # MS 
                monitor = monitor,
                screen=1,
                warp=Warp.Spherical,
                )



path = os.path.dirname(os.path.abspath(__file__))

# with open(path + r"\TestSequenceBWN.txt") as f:
with open(path + r"\TestSequenceRamp.txt") as f:
    Color = f.readlines()
    Color = [x.split(',') for x in Color]   
    Color = [x for x in Color if len(x) > 1]
    Color = [[y.strip() for y in x] for x in Color]
    ## remove empty strings
    Color = [[y for y in x if y] for x in Color]
    ## convert to float
    Color = [[float(y) for y in x] for x in Color]


# Load the stimulus from file 
dg = Stimulus(visual.GratingStim(window,
                    pos=(0, 0),
                    units='deg',
                    tex="sqr",
                    size=(250, 250),
                    mask="None",
                    texRes=256,
                    sf=0.1,
                    ),
    sweep_params={
               'Contrast': ([0.8], 0),
               'TF': ([4.0], 1),
               'SF': ([0.04], 2),
               'Ori': ([45], 3),
               },
    sweep_length=2.0,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs=15,
    shuffle=False,
    save_sweep_table=True,
    # kframes = 1200,
    )

# Define rhe display sequence for the stimulus 
part1s = 0
dg_ds = [(part1s+0, part1s+600)]
dg.set_display_sequence(dg_ds)

# Define additional parameters for the stimulus presentation 
# kwargs
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

# W7DT12722

# Create SweepStim instance with the loaded stimulus and parameters 
ss = SweepStim(window,
               stimuli=[dg],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )

# run the stimulus presentation
ss.run()

