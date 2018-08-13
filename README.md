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
ldrop = Drop.DropController()
ldrop.input_parameters("myexp", exp.on_play_callback, exp.on_stop_callback, exp.on_continue_callback)
ldrop.start_gui()
```
