# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra_plugins.range_sweeper_badr import RangeSweeper

from hydra._internal.plugins import Plugins
from hydra.plugins import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


def test_discovery():
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert RangeSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


def test_launched_jobs(sweep_runner):  # noqa: F811
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=["hydra/sweeper=range", "hydra/launcher=basic", "foo=1,2", "bar=1:3"],
        strict=True,
    )
    with sweep:
        job_ret = sweep.returns[0]
        assert len(job_ret) == 4
        assert job_ret[0].overrides == ["foo=1", "bar=1"]
        assert job_ret[0].cfg == {"foo": 1, "bar": 1}
        assert job_ret[1].overrides == ["foo=1", "bar=2"]
        assert job_ret[1].cfg == {"foo": 1, "bar": 2}
        assert job_ret[2].overrides == ["foo=2", "bar=1"]
        assert job_ret[2].cfg == {"foo": 2, "bar": 1}
        assert job_ret[3].overrides == ["foo=2", "bar=2"]
        assert job_ret[3].cfg == {"foo": 2, "bar": 2}

def test_glob_jobs(sweep_runner):  # noqa: F811
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=["hydra/sweeper=range", "hydra/launcher=basic", "foo=glob(*)"],
        strict=True,
    )
    with sweep:
        job_ret = sweep.returns[0]
        print(job_ret)
