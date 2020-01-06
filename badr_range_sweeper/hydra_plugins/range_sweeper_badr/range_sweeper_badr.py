# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import itertools
import logging
import re
import glob

from hydra._internal.config_search_path import ConfigSearchPath

# TODO: Move Plugins class outside of hydra._internal
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin, Sweeper

log = logging.getLogger(__name__)


class RangeSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleSweeper plugin to be discovered
    and used once the ExampleSweeper plugin is installed
    """

    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-range-sweeper-badr", "pkg://hydra_plugins.range_sweeper_badr.conf"
        )


class RangeSweeper(Sweeper):
    def __init__(self):
        self.config = None
        self.launcher = None
        self.job_results = None

    def setup(self, config, config_loader, task_function):
        self.config = config
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments):
        log.info("RangeSweeper sweeping")
        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))

        src_lists = []
        for s in arguments:
            key, value = s.split("=")
            gl = re.match(r'glob\((.+)\)', s)
            if ',' in value:
                possible_values=value.split(',')
            elif ':' in value:
                possible_values=range(*[int(v) for v in value.split(':')])
            elif gl:
                possible_values=list(glob.glob(gl[1], recursive=True))
            else:
                possible_values=[value]
            src_lists.append(["{}={}".format(key, val) for val in possible_values])

        batch = list(itertools.product(*src_lists))

        returns = [self.launcher.launch(batch)]
        return returns
