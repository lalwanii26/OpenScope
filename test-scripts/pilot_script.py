"""
pilot_script.py
"""
################# Parameters #################
FPS = 30
testmode=True
SessionDuration=120
TimeDilation = 1
MAXRPT = 32
SPATIALFREQ = [0.02, 0.04, 0.08]
ORIENTATIONS = [0, 90]
PHASES = [0, 90]
DRIFTRATES = [12, 24]
NCOND = len(SPATIALFREQ)*len(PHASES)*len(ORIENTATIONS)
##############################################
# Import necessary libraries
from psychopy import monitors, visual
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
import os
import time
import numpy as np
# read color information from comma separated file
def read_file(path):
    with open(path) as f:
        Color = f.readlines()
        Color = [x.split(',') for x in Color]
        Color = [x for x in Color if len(x) > 1]
        Color = [[y.strip() for y in x] for x in Color]
        # remove empty strings
        Color = [[y for y in x if y] for x in Color]
        # convert to float
        Color = [[float(y) for y in x] for x in Color]
        return Color[0]
# Get path of current file
path = os.path.dirname(os.path.abspath(__file__))
# k_frames = int(screenHz/FPS)  ## 4 for 30 Hz
# k_frames = 1  ## 4 for 30 Hz
if testmode:
    Nrepeats = 1 # number of time the repeated sequences repeat
else:
    Nrepeats = int(max([1, round(MAXRPT*SessionDuration/(120*TimeDilation))]))
print("NCOND: ", NCOND)
print("Nrepeats: ", Nrepeats)
BaseUniqueStim =  read_file(path +  r"\UniqueStim1.txt")
BaseRepeatStim =  read_file(path + r"\RepeatStim1.txt")
BaseUniqueStim2 =  read_file(path + r"\UniqueStim2.txt")
BaseRepeatStim2 =  read_file(path + r"\RepeatStim2.txt")
# Apply time dilation to the vectors
UniqueStim=[]
UniqueStim2=[]
RepeatStim=[]
RepeatStim2=[]
RepeatStim = np.repeat(BaseRepeatStim, TimeDilation).tolist()
RepeatStim2 = np.repeat(BaseRepeatStim2, TimeDilation).tolist()
UniqueStim = np.repeat(BaseUniqueStim, TimeDilation).tolist()
UniqueStim2 = np.repeat(BaseUniqueStim2, TimeDilation).tolist()
# Calculate duration of each stimulus
DurationFFF = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS) /60
DurationGR =  (NCOND*Nrepeats*len(RepeatStim)/FPS) /60
TotalScriptDuration=2*(DurationFFF+DurationGR) #in minutes
Color = UniqueStim + Nrepeats*RepeatStim + UniqueStim2 + Nrepeats*RepeatStim2
print(len(Color))
print("DurationFFF: ", DurationFFF, "min")
print("DurationGR: ", DurationGR, "min")
print("TotalScriptDuration: ", TotalScriptDuration, "min")
# flash_time = 8*(2*len(UniqueStim)+ Nrepeats*len(RepeatStim))/(2*FPS)
flash_time = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS)
sg_time = 8*(NCOND*Nrepeats*len(RepeatStim))/(2*FPS)
print("flash_time: ", flash_time, "s")
print("sg_time: ", sg_time, "s")
fl_ds = [(0, flash_time)] ##base script assumes 60fps
# flash_time = 0
sg_ds = [(flash_time+0, flash_time+sg_time)]  ## Get calclulate total time
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
                # for a fixed contrast value, color is updated every video frame
               'Contrast': ([1], 0),
               'Color':(Color, 1)
               },
    sweep_length=1, ## unused
    start_time=0.0,
    blank_length=0,
    blank_sweeps=0,
    runs = 1,
    shuffle=False,
    save_sweep_table=False,
    kframes = 1,
    )
Color = np.repeat(BaseRepeatStim, TimeDilation).tolist()
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
               'SF': (SPATIALFREQ, 1),
               'Ori': (ORIENTATIONS, 2),
               'Phase': (PHASES, 3),
               'Color': (Color,4),
               },
    sweep_length=0.25,
    start_time=0.0,
    blank_length=0.0,
    blank_sweeps=0,
    # the number of times the entire stimulus sequence will be repeated
    runs=1,
    shuffle=False,
    # fps = 30,
    save_sweep_table=False,
    kframes = 1,
    )
# ghg
# Define display sequence
fl.set_display_sequence(fl_ds)
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
               stimuli=[fl,sg],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )
# Run the SweepStim instance
t = time.localtime()
ss.run()
print("total time: ", t - time.localtime())