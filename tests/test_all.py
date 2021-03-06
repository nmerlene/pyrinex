#!/usr/bin/env python
"""
Self-test file, registration case
for OBS RINEX reader
"""
import xarray
import tempfile
from numpy.testing import run_module_suite
#
from pathlib import Path
from pyrinex import readrinex, rinexobs, rinexnav
#
rdir = Path(__file__).parent

# %% RINEX 2


def test_convenience():
    truth = xarray.open_dataset(rdir/'test2all.nc', group='OBS')

    obs, nav = readrinex(rdir/'demo.10o')
    assert obs.equals(truth)

# %%
    print('loading NetCDF4 file')
    truth = xarray.open_dataset(rdir/'test2all.nc', group='NAV')
    obs, nav = readrinex(rdir/'demo.10n')

    assert nav.equals(truth)


def test_obs2_allsat():
    """
    ./ReadRinex.py tests/demo.10o -o tests/test2all.nc
    ./ReadRinex.py tests/demo.10n -o tests/test2all.nc
    """
    print('loading NetCDF4 file')
    truth = xarray.open_dataset(rdir/'test2all.nc', group='OBS')
    print('loaded.')
# %% test reading all satellites
    for u in (None, 'm', 'all', ' ', '', ['G', 'R', 'S']):
        print('use', u)
        obs = rinexobs(rdir/'demo.10o', use=u)
        assert obs.equals(truth)

# %% test read .nc
    print('load NetCDF via API')
    obs = rinexobs(rdir/'test2all.nc')
    print('testing equality with truth')
    assert obs.equals(truth)

# %% test write .nc
    print('testing with temp file')
    with tempfile.TemporaryDirectory() as d:
        obs = rinexobs(rdir/'demo.10o', ofn=Path(d)/'testout.nc')


def test_obs2_onesat():
    """./ReadRinex.py tests/demo.10o -u G -o tests/test2G.nc"""

    truth = xarray.open_dataset(rdir/'test2G.nc', group='OBS')

    for u in ('G', ['G']):
        obs = rinexobs(rdir/'demo.10o', use=u)
        assert obs.equals(truth)


def test_obs2_multisat():
    """./ReadRinex.py tests/demo.10o -u G R -o tests/test2GR.nc"""

    truth = xarray.open_dataset(rdir/'test2GR.nc', group='OBS')

    obs = rinexobs(rdir/'demo.10o', use=('G', 'R'))
    assert obs.equals(truth)


def test_nav2():
    truth = xarray.open_dataset(rdir/'test2all.nc', group='NAV')
    nav = rinexnav(rdir/'demo.10n')

    assert nav.equals(truth)
# %% RINEX 3 OBS


def test_obs3_onesat():
    """
    ./ReadRinex.py tests/demo3.10o  -u G -o tests/test3G.nc
    """

    truth = xarray.open_dataset(rdir/'test3G.nc', group='OBS')

    for u in ('G', ['G']):
        obs = rinexobs(rdir/'demo3.10o', use=u)
        assert obs.equals(truth)


def test_obs3_multisat():
    """
    ./ReadRinex.py tests/demo3.10o  -u G R -o tests/test3GR.nc
    """
    use = ('G', 'R')

    obs = rinexobs(rdir/'demo3.10o', use=use)
    truth = xarray.open_dataset(rdir/'test3GR.nc', group='OBS')

    assert obs.equals(truth)


def test_obs3_allsat():
    """
    ./ReadRinex.py tests/demo3.10o -o tests/test3all.nc
    """

    obs = rinexobs(rdir/'demo3.10o')
    truth = rinexobs(rdir/'test3all.nc', group='OBS')

    assert obs.equals(truth)
# %% RINEX 3 NAV


def test_nav3sbas():
    """./ReadRinex.py tests/demo3.10n -o tests/test3sbas.nc"""
    truth = xarray.open_dataset(rdir/'test3sbas.nc', group='NAV')
    nav = rinexnav(rdir/'demo3.10n')

    assert nav.equals(truth)


def test_nav3gps():
    """./ReadRinex.py tests/demo.17n -o tests/test3gps.nc"""
    truth = xarray.open_dataset(rdir/'test3gps.nc', group='NAV')
    nav = rinexnav(rdir/'demo.17n')

    assert nav.equals(truth)


def test_nav3galileo():
    """
    ./ReadRinex.py tests/galileo3.15n -o tests/test3galileo.nc
    """
    truth = xarray.open_dataset(rdir/'test3galileo.nc', group='NAV')
    nav = rinexnav(rdir/'galileo3.15n')

    assert nav.equals(truth)


if __name__ == '__main__':
    run_module_suite()
