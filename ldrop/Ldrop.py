"""DropController-class."""

import sys
import os
import time
import glib
import utils
from pyee import EventEmitter
from LdropPygtkView import LDPV
from yapsy.PluginManager import PluginManager
from plugins import DropPluginLocator


class Controller(EventEmitter):
    """Main controller of the class. Views+ui separated to different files."""

    def __init__(self):
        """Constructor."""
        # run the superclass constructor
        EventEmitter.__init__(self)

        # Model initialization code
        self.sensors = []
        self.tags = []

        # define important directories for external (not program code) files
        homedir = os.environ["HOME"]
        ldrop_home = os.path.join(homedir, "Documents", "ldrop_data")
        self.rootdir = ldrop_home
        self.plugindir = os.path.join(ldrop_home, "plugins")
        self.dependenciesdir = os.path.join(ldrop_home, "dependencies")
        self.savedir = os.path.join(ldrop_home, "recordings")

        # check that saving, experiment etc directories are present
        utils.dircheck(self.savedir)
        utils.dircheck(self.plugindir)
        utils.dircheck(self.dependenciesdir)

        # put the plugins-directory and dependenciesdir to python path
        sys.path.append(self.plugindir)
        sys.path.append(self.dependenciesdir)

        # temporary? keyboard-contigency list
        self.keyboard_contigency = []

        # initialize plugin manager
        self.pluginmanager = PluginManager(plugin_locator=DropPluginLocator())
        self.pluginmanager.setPluginPlaces([self.plugindir])
        self.pluginmanager.collectPlugins()
        self.gui = []

        self.experiment_id = None
        self.play_callback = None
        self.stop_callback = None
        self.continue_callback = None
        self.data_callback = None

        self.participant_id = ""

        # TESTING glib mainloop on ldrop (moved from gui)
        glib.timeout_add(50, self.on_refresh)

    def run(self):
        """Initialize controller start mainloop."""
        # if no gui to control experiment is present, just start running the
        # experiment
        if len(self.gui) == 0 and self.play_callback is not None:
            self.play()

        self.ml = glib.MainLoop()
        self.ml.run()

    def on_refresh(self):
        """Refresher loop callback."""
        # here refreshment loop functions
        glib.timeout_add(50, self.on_refresh)

    def set_experiment_id(self, expid):
        """Experiment id-setter."""
        self.experiment_id = expid

    def set_callbacks(self, play_callback, stop_callback,
                      continue_callback, data_callback):
        """Experiment side callback-setter."""
        self.play_callback = play_callback
        self.stop_callback = stop_callback
        self.continue_callback = continue_callback
        self.data_callback = data_callback

    def enable_gui(self):
        """Initialize pygtk-view to be run when mainloop starts."""
        self.gui.append(LDPV(self, self.savedir))

    def close_gui(self):
        """Clear gui reference."""
        self.gui = []

        # run in what condition
        self.close()

    def add_sensor(self, sensor_name):
        """Callback for Add sensor -button."""
        # TODO: Improve APIs for plugins
        plugin_info = self.pluginmanager.getPluginByName(sensor_name)

        if plugin_info is None:
            print("Plugin " + sensor_name + " not found")
        else:
            plugin_info.plugin_object.get_sensor(self.rootdir,
                                                 self.savedir,
                                                 self.on_sensor_created,
                                                 self.on_sensor_error)

    def get_sensors(self):
        """Return list of connected sensors."""
        return self.sensors

    def get_sensor_plugins(self):
        """Return list of available sensors."""
        plugins = self.pluginmanager.getAllPlugins()
        sensornames = []
        for p in plugins:
            sensornames.append(p.name)

        return sensornames

    def on_sensor_error(self, msg):
        """Sensor error-handler."""
        self.emit("error", msg)

    def on_sensor_created(self, shandle):
        """Callback for sensor initialization."""
        self.sensors.append(shandle)

#        for g in self.gui:
#            g.add_sensor(shandle)
        self.emit("sensorcount_changed")

        # add model to hear calls from sensors, such as data_condition met
        self.add_model(shandle)

    def sensor_action(self, sensor_id, action_id):
        """Perform action that is listed on sensors control elements."""
        for sensor in self.sensors:
            if sensor.get_sensor_id() == sensor_id:
                sensor.action(action_id)

    def remove_sensor(self, sensor_id):
        """Disconnect the sensor with the provided sensor_id."""
        for sensor in self.sensors:
            if sensor.get_sensor_id() == sensor_id:
                sensor.disconnect()
                self.sensors.remove(sensor)
        self.emit("sensorcount_changed")

    def set_participant_id(self, pid):
        """Method for setting participant_id."""
        self.participant_id = pid

    def get_participant_id(self):
        """Return participant_id."""
        return self.participant_id

    def play(self):
        """Start the experiment."""
        # TODO: possibly change the "pipeline" of the drop-involvement in exp
        glib.idle_add(self.play_callback)

    def continue_experiment(self):
        """Callback for continuebutton click."""
        for sensor in self.sensors:
            sensor.clear_data_conditions()

        if self.continue_callback is not None:
            self.continue_callback()

    def stop(self):
        """Callback for stopbutton click."""
        self.stop_callback()

    def add_model(self, model):
        """Add a model to listen for."""
        model.on("tag", self.on_tag)
        model.on("data", self.on_data)

    def timestamp(self):
        """Return a local timestamp in microsecond accuracy."""
        return time.time()

    def on_tag(self, tag):
        """
        Send a tag to all sensors.

        Tag might not come instantly here so the
        timestamp is taken in advance. The sensor must sync itself with the
        computer. Tag consists of:
        id = string, identifier of the tag
        timestamp = timestamp in ms of the localtime clock
        secondary_id = string, defines "start", "end", or "impulse", as a start
        of perioid, end of it or single impulse
        misc = other possible information (depends on the sensor how to use)
        """
        for sensor in self.sensors:
            # send a copy of the dict to each sensor
            sensor.tag(tag.copy())

#        self.tags.append(tag)
        self.emit("log_update", tag.copy())

    def on_keypress(self, keyname):
        """Callback for keypress."""
        if keyname in self.keyboard_contigency:
            self.keyboard_contigency = []
            self.emit("continue")
            tag = {"id": keyname, "secondary_id": "keypress",
                   "timestamp": self.timestamp()}
            self.on_tag("tag", tag)

    def on_experiment_completed(self):
        """Callback for experiment finished."""
        # clear view references
        for r in self.sensors:
            self.exp_view.remove_model(r)
        # self.exp_view = None

    def on_data(self, dp):
        """Callback for data-signal."""
        if self.data_callback is not None:
            glib.idle_add(self.data_callback, dp)

    def start_collecting_data(self, section_id):
        """Function starts data collection on all sensors."""
        for sensor in self.sensors:
            sensor.start_recording(self.savedir, self.participant_id,
                                   self.experiment_id, section_id)

    def stop_collecting_data(self, callback):
        """Stop data collection on all sensors and run callback."""
        for sensor in self.sensors:
            sensor.stop_recording()
        glib.idle_add(callback)

    def close(self):
        """Method that closes the drop controller."""
        # disconnect all the sensors from the host
        for sensor in self.sensors:
            sensor.stop_recording()
            sensor.disconnect()

        self.remove_all_listeners()

        self.ml.quit()
        print("ldrop mainloop closed.")

    def __del__(self):
        """Destructor."""
        print("ldrop instance closed.")


def main():
    """Main function for running drop."""
    DropController()
