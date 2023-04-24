"""
brain_observatory_stimulus.py
"""
from camstim import Stimulus, SweepStim
from camstim import Foraging
from camstim import Window, Warp
import time
import datetime
import os
from psychopy import monitors, visual

dist = 15.0
# wid = 52.0
wid = 32.0

# create a monitor
monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

# Create display window
window = Window(fullscr=True,
                # monitor= 'Gamma1.Luminance50',          # MS 
                monitor = monitor,
                screen=1,
                # warp=Warp.Spherical,
                )

# sg_path = 		r"C:\Users\ITSloaner\Downloads\openscope-glo-stim-main\openscope-glo-stim-main\stim_files\static_gratings.stim"

part2s  = 0
sg_ds = [(part2s+0, part2s+480), (part2s+1800, part2s+2280), (part2s+3210, part2s+3750)]

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

sg = Stimulus(visual.GratingStim(window,
                    pos=(0, 0),
                    units='deg',
                    size=(250, 250),
                    mask="None",
                    texRes=256,
                    sf=0.1,
                    ),
    sweep_params={
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
    runs=50,
    shuffle=False,
    save_sweep_table=True,
    )


sg.set_display_sequence(sg_ds)


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

# Create SweepStim instance
ss = SweepStim(window,
               stimuli=[sg],
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

# run it
ss.run()

