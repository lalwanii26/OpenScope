"""
brain_observatory_stimulus.py
"""

# import necessary libraries 
from psychopy import visual
from camstim import Stimulus, SweepStim
from camstim import Foraging
from camstim import Window, Warp
import time
import datetime

from psychopy import monitors, visual

# Define distance and width parameters for monitor
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


# Define file paths for stimuli   
fl250_path =	r"C:\Users\ITSloaner\Downloads\openscope-glo-stim-main\openscope-glo-stim-main\stim_files\flash_250ms.stim" #
dg_path = 		r"C:\Users\ITSloaner\Downloads\openscope-glo-stim-main\openscope-glo-stim-main\stim_files\drifting_gratings.stim"
sg_path = 		r"C:\Users\ITSloaner\Downloads\openscope-glo-stim-main\openscope-glo-stim-main\stim_files\static_gratings.stim"
ns_path = 		r"C:\Users\ITSloaner\Downloads\openscope-glo-stim-main\openscope-glo-stim-main\stim_files\natural_scenes.stim"


# g20 = Stimulus.from_file(g20_path, window) 
# fl250 = Stimulus.from_file(fl250_path, window) 

# dg = Stimulus.from_file(dg_path, window) 
# nm1 = Stimulus.from_file(nm1_path, window)
# nm3 = Stimulus.from_file(nm3_path, window)

# ns = Stimulus.from_file(ns_path, window)
sg = Stimulus.from_file(sg_path, window)
# nm1 = Stimulus.from_file(nm1_path, window)

# RF mapping / flashes
# g20_ds = [(0, 1200)]
# fl250_ds = [(1200, 1500)]
# fl250_ds = [(0, 1200)]
# part1s = fl250_ds[0][1] # end of part 1


# dg_ds = [(part1s+0, part1s+600),(part1s+1590, part1s+2190), (part1s+3120, part1s+3810)]
# part2s = dg_ds[2][1] # end of part 2

# nm3_ds = [(part1s+630, part1s+1230), (part1s+2490, part1s+3090)]
# nm1_ds = [(part1s+1260, part1s+1560), (part2s+2310, part2s+2610) ]

# ns_ds = [(part2s+510, part2s+990), (part2s+1290, part2s+1770), (part2s+2640, part2s+3180)]
part2s  = 0
sg_ds = [(part2s+0, part2s+480), (part2s+1800, part2s+2280), (part2s+3210, part2s+3750)]


# g20.set_display_sequence(g20_ds)
# fl250.set_display_sequence(fl250_ds)
# dg.set_display_sequence(dg_ds)
# nm3.set_display_sequence(nm3_ds)
# nm1.set_display_sequence(nm1_ds)
# ns.set_display_sequence(ns_ds)

# load our stimuli from the file path
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
            #    stimuli=[g20, fl250, dg, ns, sg],
            #    stimuli=[g20, fl250, dg, ns, sg],
                # stimuli=[fl250],
            #    stimuli=[dg, ns, sg],
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

