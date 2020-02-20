import pandas as pd
from numpy import array, sqrt, zeros, zeros_like

from netCDF4 import Dataset, chartostring, num2date


def get_grdpt_data(model_data, var, M, N, t, time=True):
    """TODO: Docstring for get_grdpt_data.

    :model_data: TODO
    :var: TODO
    :M: TODO
    :N: TODO
    :t: TODO
    :time: TODO
    :returns: TODO

    """
    output = zeros(len(model_data))
    times = []

    for i, nc in enumerate(model_data):
        data = Dataset(nc)
        output[i] = data[var][t, N, M]

        if time:
            times.append(num2date(data["time"][t]), data["time"].units)

        if time:
            return output, array(times)
        else:
            return output


def distance(x, y):
    """returns linear distance between cells for coords x and y"""

    s = zeros_like(x)

    for i in range(1, len(x)):
        s[i] = sqrt((x[i] - x[0]) ** 2 + (y[i] - y[0]) ** 2)

    return s


def station_list(dataset, xr=False):
    """convert character array to list of station"""

    chars = dataset["station_id"][:, :]
    strings = list(chartostring(chars))

    return [station_id.strip() for station_id in strings]


def xb_time_vectors(dataset, t0):
    """extract datetimes from netCDF dataset.

    arguments:
    dataset --- netCDF dataset
    t0      --- datetime for beginning of simulation
    """

    time_types = [
            "globaltime",
            "pointtime",
            "meantime",
            "tidetime",
            "windtime"
    ]
    datetimes = {}

    for time_type in time_types:

        try:
            time_unit = dataset[time_type].units
            times = pd.to_timedelta(dataset[time_type][:], unit=time_unit)
            datetimes[time_type] = t0 + times

        except IndexError:
            datetimes[time_type] = None

    return datetimes
