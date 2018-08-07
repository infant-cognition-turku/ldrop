# ldrop
Data recording sensor api and gui.

### What is ldrop?
ldrop is a more open version of drop that does not require any predefined structure for the experiment.
ldrop is aiming to be a library which gives the user a sensor-API to be easily used with their own scripts.

### How to use ldrop?
Probably API design is not final.
```
import Drop
exp = MyExperiment()
ldrop = Drop.DropController()
ldrop.input_parameters("myexp", exp.on_play_callback, exp.on_stop_callback, exp.on_continue_callback)
ldrop.start_gui()
```
