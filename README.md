# ldrop
Data recording sensor api and gui.

### What is ldrop?
ldrop is a more open version of drop that does not require any predefined
structure for the experiment. ldrop is aiming to be a library which provides 
user a sensor-API to be easily used with their own scripts.

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

# Signals listened by ldrop controller
"tag" - sends a tag to all connected sensors with timestamp now [dict]
"start_recording" - begins recording on all connected sensors [savesubdir, savefilestr]
"stop_recording" - ends recording on all connected sensors and saves recorded data []
"query" - invoke a popup question to user [msg, title, (option1, gtk.response, ...), [callback1, ...], [parameter1(/None), ...]]
"log_message" - appends a string on possible GUI log [str]

# Callbacks required on experiment-file
on_play - is run when play-button is pressed, Play_callback will run automatically on start if on no gui-mode
on_stop - is run when stop-button is pressed
on_continue - is run when continue-button is pressed
on_data - is run when a data packet arrives from any sensor

### Example experiment structure
Dependencies and instructions here are specific to certain ICL experiments.

![Alt text](readme_pic1.png?raw=true "Ldrop example experiment structure")
