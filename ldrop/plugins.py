"""Plugin support classes."""
from yapsy.PluginFileLocator import PluginFileLocator
from pkg_resources import iter_entry_points
import os.path


class LdropPluginLocator(PluginFileLocator):
    """ldrop plugin locator."""

    def __init__(self):
        """Constructor."""
        super(LdropPluginLocator, self).__init__()

    def locatePlugins(self):
        """Locate plugins."""
        # First get plugins from the superclass.
        base = super(LdropPluginLocator, self).locatePlugins()

        # Iterate through entry point functions to find plugins
        entrypoints = \
            [(e.load())() for e in iter_entry_points(group='drop.plugin')]

        # Get candidate infofile and file paths for yapsy
        candidate_infofile_paths, candidate_file_paths = \
            zip(*entrypoints) if len(entrypoints) > 0 else ([], [])

        # Construct plugininfo objects for yapsy
        plugininfos = [self.gatherCorePluginInfo(
            os.path.dirname(p), os.path.basename(p))[0] for p in
            candidate_infofile_paths]

        # Convert plugin information to "3-tuple in list" understood by yapsy
        ep_plugins = zip(candidate_infofile_paths,
                         candidate_file_paths,
                         plugininfos)

        # Combine found plugins and the count of plugins with the ones returned
        # from superclass.
        return (base[0] + ep_plugins), (base[1] + len(ep_plugins))
