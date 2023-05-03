"""
brain_observatory_stimulus.py
"""

################# Parameters #################
FPS = 30
testmode = True
SessionDuration = 120
TimeDilation = 1
MAXRPT = 32
SPATIALFREQ = [0.02, 0.04, 0.08]
ORIENTATIONS = [0, 90]
PHASES = [0, 90]
DRIFTRATES = [12, 24]
NCOND = len(SPATIALFREQ)*len(PHASES)*len(ORIENTATIONS)
##############################################

# PART 3 DRIFTING GRATINGS
# Loop over grating parameters and then within parameter condition,
# modulate contrast according to values in stimulus, one per video frame
# where -1 encodes changing the grating phase by -dr degrees, and +1
# encodes changing the phase by +dr degrees, compared to the phase of
# previous video frame. At 30fps dr=12 corresponds to 1Hz temporal
# frequency drift if it were shifting in a constant direction
# Thus instead of saving the contrast of each frame to the data file, we
# should save the spatial phase of each frame

# The following line of code starts from ph=0 and *changes* the
# phase by RepeatStim(t)*dr every video frame; the MATLAB
# function wrapTo360 then maps values below 0 or above 360
# degrees to their equivalent in the 360 degree circle.
# ph=wrapTo360(cumsum(RepeatStim*dr));

def wrapTo360(x):
    return np.mod(x, 360)


# Import necessary libraries
from psychopy import monitors, visual
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
import os
import time
import numpy as np

# read Contrast information from comma separated file
path = os.path.dirname(os.path.abspath(__file__))

with open(path + r"\RepeatStim1.txt") as f:
    Phase = f.readlines()
    Phase = [x.split(',') for x in Phase]   
    Phase = [x for x in Phase if len(x) > 1]
    Phase = [[y.strip() for y in x] for x in Phase]
    ## remove empty strings
    Phase = [[y for y in x if y] for x in Phase]
    ## convert to float
    Phase = [[float(y) for y in x] for x in Phase]
    Phase = Phase[0]


### convert phase according to drift rate and warp to 360 degrees

phase = 0
for i in range(len(Phase)):
    phase += Phase[i]*DRIFTRATES[0]
    Phase[i] = wrapTo360(phase)
Phase = [x/360 for x in Phase]

print(Phase)


# Get path of current file
path = os.path.dirname(os.path.abspath(__file__))

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
                # warp=Warp.Spherical,
                )

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
               'Contrast': ([1], 0),
               'SF': ([0.02], 1),
               'Ori': ([0], 2),
            #    'Phase': (Phase, 3),
                'Phase': (Phase, 3),
            #    'TF': ([1], 4),
    },
    sweep_length=0.1,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs=1,
    shuffle=False,
    save_sweep_table=True,
    kframes=4,
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

