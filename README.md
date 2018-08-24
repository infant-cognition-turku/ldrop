# ldrop
Data recording sensor api and gui.

### What is ldrop?
ldrop is a more open version of drop that does not require any predefined
structure for the experiment. ldrop is aiming to be a library which provides 
user a sensor-API to be easily used with their own scripts.

### System requirements
ldrop is not platform dependend by nature. However we use Linux because python
is easiest to use on Linux.

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