
import camstim
from camstim import Stimulus, SweepStim, Foraging, Window, Warp
from psychopy import monitors, visual
import os
import time
import numpy as np
import logging
import sys
import argparse
import yaml

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

def get_stimulus_sequence(window, SESSION_PARAMS_data_folder):

    ################# Parameters #################
    FPS = 30
    testmode = True
    SessionDuration = 120 ## not used if testmode is True
    MAXRPT = 32
    SPATIALFREQ = [0.02, 0.04, 0.08]
    ORIENTATIONS = [0, 90]
    PHASES = [0, 90]
    DRIFTRATES = [12, 24]
    NCOND = len(SPATIALFREQ)*len(PHASES)*len(ORIENTATIONS)
    DRIFT_NCOND = len(SPATIALFREQ)*len(ORIENTATIONS)*len(DRIFTRATES)
    ADD_FLASHES = True
    ADD_STATIC = True
    ADD_DRIFT = True
    ##############################################

    if testmode:
        Nrepeats = 1 # number of time the repeated sequences repeat
    else:
        Nrepeats = int(max([1, round(MAXRPT*SessionDuration/(120))]))

    logging.info("NCOND: %d", NCOND)
    logging.info("DRIFT_NCOND: %d", DRIFT_NCOND)
    logging.info("Nrepeats: %d", Nrepeats)

    # Read in the stimulus sequence
    UniqueStim =  read_file(os.path.join(SESSION_PARAMS_data_folder, 
                                             "UniqueStim1.txt"))
    RepeatStim =  read_file(os.path.join(SESSION_PARAMS_data_folder, 
                                             "RepeatStim1.txt"))
    UniqueStim2 =  read_file(os.path.join(SESSION_PARAMS_data_folder, 
                                              "UniqueStim2.txt"))
    RepeatStim2 =  read_file(os.path.join(SESSION_PARAMS_data_folder, 
                                              "RepeatStim2.txt"))

    # Calculate duration of each stimulus
    DurationFFF = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS) /60
    DurationGR =  (NCOND*Nrepeats*len(RepeatStim)/FPS) /60
    TotalScriptDuration=2*(DurationFFF+DurationGR) #in minutes

    Contrast = UniqueStim + Nrepeats*RepeatStim + UniqueStim2 + Nrepeats*RepeatStim2

    logging.info("DurationFFF: %f min", DurationFFF)
    logging.info("DurationGR: %f min", DurationGR, "min")
    logging.info("TotalScriptDuration: %f min", TotalScriptDuration)

    flash_time = (2*len(UniqueStim)/FPS + Nrepeats*len(RepeatStim)/FPS)
    sg_time = (NCOND*Nrepeats*len(RepeatStim)/FPS)
    dg_time = (DRIFT_NCOND*Nrepeats*len(RepeatStim)/FPS)
    current_start_time = 0

    all_stim = []

    if ADD_FLASHES:
        fl_ds = [(current_start_time, current_start_time+flash_time)] 

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
        fl.set_display_sequence(fl_ds)

        current_start_time = current_start_time+flash_time

        all_stim.append(fl)

    if ADD_STATIC:
        Contrast = RepeatStim2 

        sg_ds = [(current_start_time, current_start_time+sg_time)]  ## calculate total time

        # Standing (static) Grating with fixed sf, ori, and ph
        # contrast is updated every video frame according to the loaded stimulus sequence
        sg = Stimulus(visual.GratingStim(window,
                            pos=(0, 0),
                            units='deg',
                            tex="sqr",
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
                    'SF': (SPATIALFREQ, 0),
                    'Ori': (ORIENTATIONS, 1),
                    'Phase': (PHASES, 2),
                    'Contrast': (Contrast, 3),
                    },
            sweep_length=1.0/FPS,
            start_time=0.0,
            blank_length=0.0,
            blank_sweeps=0,
            runs=1,
            shuffle=False,
            save_sweep_table=False,
            )
        sg.set_display_sequence(sg_ds)

        current_start_time = current_start_time+sg_time

        all_stim.append(sg)

    if ADD_DRIFT:
        Phase = RepeatStim 

        dg_ds = [(current_start_time, current_start_time+dg_time)]  ## calculate total time

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
        dg.set_display_sequence(dg_ds)

        all_stim.append(dg)

    return all_stim


if __name__ == "__main__":
    parser = argparse.ArgumentParser("mtrain")
    parser.add_argument("json_path", nargs="?", type=str, default="")

    args, _ = parser.parse_known_args() # <- this ensures that we ignore other arguments that might be needed by camstim
    
    # logging.info args
    if args.json_path == "":
        logging.warning("No json path provided, using default parameters. THIS IS NOT THE EXPECTED BEHAVIOR FOR PRODUCTION RUNS")
        json_params = {}
    else:
        with open(args.json_path, 'r') as f:
            # we use the yaml package here because the json package loads as unicode, which prevents using the keys as parameters later
            json_params = yaml.load(f)
            logging.info("Loaded json parameters from mtrain")
            # end of mtrain part

    dist = 15.0
    wid = 52.0

    # mtrain should be providing : a path to a network folder or a local folder with the entire repo pulled
    SESSION_PARAMS_data_folder = json_params.get('data_folder', os.path.dirname(os.path.abspath(__file__)))

    # mtrain should be providing : Gamma1.Luminance50
    monitor_name = json_params.get('monitor_name', "testMonitor")

    # create a monitor
    if monitor_name == 'testMonitor':
        monitor = monitors.Monitor(monitor_name, distance=dist, width=wid)
    else:
        monitor = monitor_name
        
    # Create display window
    window = Window(fullscr=True, # Will return an error due to default size. Ignore.
                    monitor=monitor,  # Will be set to a gamma calibrated profile by MPE
                    screen=0,
                    warp=Warp.Spherical
                    )

    sequence_stim = get_stimulus_sequence(window, SESSION_PARAMS_data_folder)

    ss = SweepStim(window,
                    stimuli=sequence_stim,
                    pre_blank_sec=0,
                    post_blank_sec=0,
                    params={},
                    )

    # add in foraging so we can track wheel, potentially give rewards, etc
    f = Foraging(window = window,
                    auto_update = False,
                    params= {}
                    )
    
    ss.add_item(f, "foraging")

    # Run the SweepStim instance
    t = time.localtime()
    ss.run()
    logging.info("total time: %f", t - time.localtime())