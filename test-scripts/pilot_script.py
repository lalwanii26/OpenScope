"""
pilot_script.py
"""

################# Parameters #################
FPS = 30
testmode = True
SessionDuration = 120 ## not used if testmode is True
TimeDilation = 1
MAXRPT = 32
SPATIALFREQ = [0.02, 0.04, 0.08]
ORIENTATIONS = [0, 90]
PHASES = [0, 90]
DRIFTRATES = [12, 24]
NCOND = len(SPATIALFREQ)*len(PHASES)*len(ORIENTATIONS)
DRIFT_NCOND = len(SPATIALFREQ)*len(ORIENTATIONS)*len(DRIFTRATES)
##############################################

# Define monitor parameters
dist = 15.0
wid = 52.0

# Import necessary libraries
from psychopy import monitors, visual
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
import os
import time
import numpy as np

def drift2Phase(Phase, drift):
    phase = 0
    for i in range(len(Phase)):
        phase += Phase[i]*drift
        Phase[i] = np.mod(phase, 360)
    Phase = [x/360 for x in Phase]
    return Phase

# read Contrast information from comma separated file
def read_file(path):
    with open(path) as f:
        Contrast = f.readlines()
        Contrast = [x.split(',') for x in Contrast]
        Contrast = [x for x in Contrast if len(x) > 1]
        Contrast = [[y.strip() for y in x] for x in Contrast]
        # remove empty strings
        Contrast = [[y for y in x if y] for x in Contrast]
        Contrast = [[float(y) for y in x] for x in Contrast]
        return Contrast[0]

# Get path of current file
path = os.path.dirname(os.path.abspath(__file__))

if testmode:
    Nrepeats = 1 # number of time the repeated sequences repeat
else:
    Nrepeats = int(max([1, round(MAXRPT*SessionDuration/(120*TimeDilation))]))

print("NCOND: ", NCOND)
print("DRIFT_NCOND: ", DRIFT_NCOND)
print("Nrepeats: ", Nrepeats)

BaseUniqueStim =  read_file(path +  r"\UniqueStim1.txt")
BaseRepeatStim =  read_file(path + r"\RepeatStim1.txt")
BaseUniqueStim2 =  read_file(path + r"\UniqueStim2.txt")
BaseRepeatStim2 =  read_file(path + r"\RepeatStim2.txt")

UniqueStim, UniqueStim2, RepeatStim, RepeatStim2 = [], [], [], []

RepeatStim = np.repeat(BaseRepeatStim, TimeDilation).tolist()
RepeatStim2 = np.repeat(BaseRepeatStim2, TimeDilation).tolist()
UniqueStim = np.repeat(BaseUniqueStim, TimeDilation).tolist()
UniqueStim2 = np.repeat(BaseUniqueStim2, TimeDilation).tolist()

# Calculate duration of each stimulus
DurationFFF = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS) /60
DurationGR =  (NCOND*Nrepeats*len(RepeatStim)/FPS) /60
TotalScriptDuration=2*(DurationFFF+DurationGR) #in minutes

Contrast = UniqueStim + Nrepeats*RepeatStim + UniqueStim2 + Nrepeats*RepeatStim2

print("DurationFFF: ", DurationFFF, "min")
print("DurationGR: ", DurationGR, "min")
print("TotalScriptDuration: ", TotalScriptDuration, "min")

flash_time = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS)
sg_time = (NCOND*Nrepeats*len(RepeatStim)/FPS)
dg_time = (DRIFT_NCOND*Nrepeats*len(RepeatStim)/FPS)

fl_ds = [(0, flash_time)] 
sg_ds = [(flash_time+0, flash_time+sg_time)]  ## Get calclulate total time
dg_ds = [(flash_time+sg_time+0, flash_time+sg_time+dg_time)]  ## Get calclulate total time

# # create a monitor
monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

# Create display window
window = Window(fullscr=True,
                # monitor= 'Gamma1.Luminance50',          # MS
                monitor = monitor,
                screen=1,
                # warp=Warp.Spherical,
)

# load FF stimuli
# FFF implemented as a grating with fixed sf=0, ori=0, and ph=0
# contrast is updated every video frame according to the loaded stimulus sequence
fl = Stimulus(visual.GratingStim(window,
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
                # for a fixed contrast value, Contrast is updated every video frame
               'Contrast': ([1], 0),
               'Color':(Contrast, 1)
               },
    sweep_length=1.0/FPS,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs = 1,
    shuffle=False,
    save_sweep_table=False,
    )

Contrast = np.repeat(BaseRepeatStim, TimeDilation).tolist()

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
                # for a fixed contrast value, Contrast is updated every video frame
               'Contrast': ([1], 0),
               'SF': (SPATIALFREQ, 1),
               'Ori': (ORIENTATIONS, 2),
               'Phase': (PHASES, 3),
               'Color': (Contrast, 4),
               },
    sweep_length=1.0/FPS,
    start_time=0.0,
    blank_length=0.0,
    blank_sweeps=0,
    runs=1,
    shuffle=False,
    save_sweep_table=False,
    )


Phase = np.repeat(BaseRepeatStim, TimeDilation).tolist()
phases = []
for drift in DRIFTRATES:
    phases += drift2Phase(Phase, drift)


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
               'SF': (SPATIALFREQ, 1),
               'Ori': (ORIENTATIONS, 2),
                'Phase': (phases, 3),
    },
    sweep_length=1.0/FPS,
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs=1,
    shuffle=False,
    save_sweep_table=True,
    )


# Define display sequence
fl.set_display_sequence(fl_ds)
sg.set_display_sequence(sg_ds)
dg.set_display_sequence(dg_ds)

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
               stimuli=[fl, sg, dg],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )

# Run the SweepStim instance
t = time.localtime()
ss.run()
print("total time: ", t - time.localtime())