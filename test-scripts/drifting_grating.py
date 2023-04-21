"""
brain_observatory_stimulus.py
"""
# Import required modules
from camstim import Stimulus, SweepStim
from camstim import Window, Warp
from psychopy import monitors
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
                warp=Warp.Spherical,)

## get path of current file
# Define the path to stimulus files 
path = os.path.dirname(os.path.abspath(__file__))
dg_path = path + r"\..\stim_files\drifting_gratings.stim"

# Load the stimulus from file 
dg = Stimulus.from_file(dg_path, window) 


# Define rhe display sequence for the stimulus 
part1s = 0
dg_ds = [(part1s+0, part1s+600),(part1s+1590, part1s+2190), (part1s+3120, part1s+3810)]
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

