from psychopy import visual, core, event
from pyee import EventEmitter
#import feedparser
import random
import os
import time
from ldrop import Ldrop
import glib

class Experiment(EventEmitter):
    def __init__(self):

        # run the superclass constructor
        EventEmitter.__init__(self)

        # constructor
        self.win = None
        self.draw_queue = []

    def start_experiment(self):
        self.paused = False

        # parameters
        self.rounds = 4
        self.round = 1
        self.stimulus_display_time = 5000
        waittime = 0.5 #s
        self.images = ["heart.png"]

        # create a window object
        self.res = [1024,768]
        win = visual.Window(self.res, monitor="testMonitor", units="norm")
        self.win = win

        glib.idle_add(self.trial_start)
        glib.idle_add(self.draw)

    def trial_start(self):

        if self.paused:
            glib.timeout_add(100, self.trial_start)        
            return
        self.draw_queue = []

        self.emit('tag', {"tag":"trial start"})
            
        x = 0
        y = 0

        # place for the new off-stimulus
        while (0.3 > abs(x) or 0.3 > abs(y)):
            x = random.random()*1.6 -0.8
            y = random.random()*1.4 -0.7

        if len(self.images) >0:
            random.shuffle(self.images)
            stm = visual.ImageStim(win=self.win,
                                   image=self.images[0],
                                   pos=(x,y), size=0.4)
            stm.draw()
            self.emit('tag', {"tag":"image", "info":self.images[0],
                              "loc":[x,y]})

            self.draw_queue.append(stm)

        self.round += 1

        if self.round <= self.rounds:
            glib.timeout_add(self.stimulus_display_time, self.trial_start)
        else:
            self.quit()

    def draw(self):

        # draw screen
        for i in self.draw_queue:
            i.draw()

        if self.win is None:
            # loop quits by itself when window is closed
            return

        self.win.flip()
        glib.timeout_add(50, self.draw)

    def on_data(self, dp):
        if self.win is not None:
            eye = visual.Circle(self.win, pos=(dp["x"]*2-1, -(dp["y"]*2-1)),
                                fillColor=[0.5,0.5,0.5], size=0.05, lineWidth=1.5)
            eye.draw()

    def on_stop(self):
        self.paused = True

    def on_continue(self):
        self.paused = False

    def quit(self):
        print("QUIT")
        # cleanup
        self.win.close()

        #TODO: is this good solution to fade out draw-loop like this?
        self.win = None

#       core.quit() seems to kill glib mainloop and pygtk-app
#        core.quit()

# start running here
exp = Experiment()

# create ldrop controller-instance
ldrop = Ldrop.Controller()

# use setter-functions to set details of the experiment
ldrop.set_experiment_id("test")
ldrop.set_callbacks(exp.start_experiment, exp.on_stop,
                      exp.on_continue, exp.on_data)

# make a subscription to experiment instance on ldrop to receive tags
#exp.tag_callback = ldrop.on_tag
ldrop.add_model(exp)

# autoadd mouse sensor if you have the sensor-module available
ldrop.add_sensor('mouse')

# enable sensor-gui (optional)
ldrop.enable_gui()

# starts blocking
ldrop.run()