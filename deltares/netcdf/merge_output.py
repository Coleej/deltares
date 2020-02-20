import sys
from pathlib import Path

from netCDF4 import Dataset
from pandas import to_timedelta
from xarray import concat, open_dataset


def init_merged_dataset(toplevel_output, output_fn, model_type):
    """TODO: Docstring for init_merged_dataset.

    :toplevel_output: TODO
    :output_fn: TODO
    :model_type: TODO
    :returns: TODO

    """
    initial_output = toplevel_output
    initial_output = Dataset(initial_output)


def enumerate_output(toplevel_output, model_type, model_name, output_type):
    """TODO: Docstring for enumerate_output.

    :toplevel_output: TODO
    :model_type: TODO
    :output_type: TODO
    :returns: TODO

    """

    if model_type == "xbeach":
        model_type = "XB"
    elif model_type == "delft3d":
        model_type = "D3D"
    else:
        print("please enter model_type type: xbeach or delft3d")
        sys.exit()

    glob_expr = f"{model_type}_*/{output_type}*{model_name}.nc"
    output_datas = toplevel_output.glob(glob_expr)

    return list(output_datas)


def add_xb_time_coords(xb_ds, t0):
    """TODO: Docstring for add_xb_time_coords.

    :xb_ds: TODO
    :t0: TODO
    :returns: TODO

    """
    try:
        gtime_steps = xb_ds.globaltime.values
        globaltime_coords = t0 + to_timedelta(gtime_steps, 'seconds')
        xb_ds.coords["globaltime"] = globaltime_coords
    except AttributeError:
        pass

    try:
        ptime_steps = xb_ds.pointtime.values
        pointtime_coords = t0 + to_timedelta(ptime_steps, 'seconds')
        xb_ds.coords["pointtime"] = pointtime_coords
    except AttributeError:
        pass

    try:
        mtime_steps = xb_ds.meantime.values
        meantime_coords = t0 + to_timedelta(mtime_steps, 'seconds')
        xb_ds.coords["meantime"] = meantime_coords
    except AttributeError:
        pass

    return xb_ds


def concate_xb_output(output_datas, coupling_t0s):
    """TODO: Docstring for concate_xb_output.

    :output_dirs: TODO
    :coupling_t0: TODO
    :returns: TODO

    """
    xb_data = []

    for t0, output_ds in zip(coupling_t0s, output_datas):
        xb_ds = open_dataset(output_ds)
        xb_ds = add_xb_time_coords(xb_ds, t0)
        xb_data.append(xb_ds)

        continue

    return concat(xb_data)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        output_name = sys.argv[1]
        toplevel_output = Path(sys.argv[2])
    else:
        output_name = sys.argv[1]
        toplevel_output = Path.cwd()
        pass

    output_fn = toplevel_output / output_name
    merged_dataset = Dataset(output_name, "w", format="NETCDF4")
