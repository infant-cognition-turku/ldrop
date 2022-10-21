# ldrop
Data recording sensor api and gui.

ldrop gui for experiment control                                          |  stimuli & sensors (e.g., eye tracking)
:------------------------------------------------------------------------:|:-------------------------:
<img src="https://github.com/infant-cognition-turku/ldrop/blob/master/gui.png" width="200"> | <img src="https://github.com/infant-cognition-turku/ldrop/blob/master/vis2.gif" width="200">

### What is ldrop?
ldrop is an open-source platform for projects that aim to a present stimuli on computer screen and collect time-locked data from sensors (such as an eye tracker)during the task. ldrop is designed to be open source and modular platform to easily add new modules such as recording devices. ldrop has been so far used to collect moment-by-moment gaze data from children during picture viewing in various settings.

The figure below shows a setup using ldrop to collected eye tracking data from children in rural areas of Sierra Leone (Leppänen et al., 2022). One of the beneficial features of ldrop when used with an eye tracker is near real-time visualization of the distance of the observer's eyes from the sensor (see animation on the right). This has helped in positioning young children at a correct distance and angle with respect to the eye tracking system.

Leppänen, J. M., Butcher, J. W., Godbout, C., Stephenson, K., Hendrixson, D. T., Griswold, S., Rogers, B. L., Webb, P., Koroma, A. S., & Manary, M. J. (2022). Assessing infant cognition in field settings using eye-tracking: a pilot cohort trial in Sierra Leone. BMJ open, 12(2), e049783. https://doi.org/10.1136/bmjopen-2021-049783


### System requirements
ldrop is not platform dependend by nature. However we use Linux because python
is easiest to use on Linux.

### Install instructions
run the following commands:
```
sudo apt-get install python-pip
sudo apt-get install git
sudo apt-get install python-gtk2
pip install git+https://github.com/infant-cognition-tampere/ldrop.git
```

### How to use ldrop?
[API design not final]
```
import Ldrop

# create instance of your experiment class (suggested to inherit
# from pyee EventEmitter)
exp = MyExperiment()

# create instance of drop controller
ldrop = Ldrop.DropController()

# set parameters and callbacks for the controller to control experiment
ldrop.set_experiment_id("myexp")
ldrop.set_callbacks(exp.on_play, exp.on_stop, exp.on_continue, exp.on_data)

# ldrop to listen events emitted by experiment
ldrop.add_model(exp)

# add a sensor to record data during experiment run
ldrop.add_sensor('null')

# enable graphical user interface (optional)
ldrop.enable_gui()

# start drop mainloop
ldrop.run()
```

### API
Signals between ldrop components are transported through pyee.EventEmitter.emit().

#### Signals listened by ldrop controller
- "tag" - sends a tag to all connected sensors with timestamp now [dict]
- "start_recording" - begins recording on all connected sensors [savesubdir, savefilestr]
- "stop_recording" - ends recording on all connected sensors and saves recorded data []
- "query" - invoke a popup question to user [msg, title, (option1, gtk.response, ...), [callback1, ...], [parameter1(/None), ...]]
- "log_message" - appends a string on possible GUI log [str]

#### Callbacks required on experiment-file
- on_play - is run when play-button is pressed, Play_callback will run automatically on start if on no gui-mode
- on_stop - is run when stop-button is pressed
- on_continue - is run when continue-button is pressed
- on_data - is run when a data packet arrives from any sensor

### Example experiment structure
Dependencies and instructions here are specific to certain ICL experiments.

![Alt text](readme_pic1.png?raw=true "Ldrop example experiment structure")
