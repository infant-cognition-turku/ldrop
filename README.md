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
import Drop
exp = MyExperiment()
ldrop = LDrop.DropController()
ldrop.set_experiment_id("myexp")
ldrop.set_callbacks(exp.on_play, exp.on_stop, exp.on_continue, exp.on_data)
exp.tag_callback = ldrop.on_tag
ldrop.enable_gui()
ldrop.run()
```