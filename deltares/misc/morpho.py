import matplotlib.pyplot as plt
from pandas import Series
from xarray import DataArray, concat

from ..netcdf.results import distance


# IO
def write_results_csv(fn, df, profile):
    """ write csv results to pass to Brian """
    try:
        out_columns = ["distance", "x_coord", "y_coord", profile]
        df.loc[:, out_columns].to_csv(fn, index_label="point_id")

        return 0
    except FileNotFoundError:
        raise


# analysis
def get_shoreline(ds, MHW):
    """ locate index of shoreline """
    N = len(ds)

    for i in range(N - 1):
        z0 = ds[i]
        zf = ds[i + 1]

        if z0 <= MHW and zf > MHW:
            return i

    pass


def get_backbarrier(ser, shoreline_idx, MHW):
    """ locate index of back barrier transition """
    ser = ser[shoreline_idx + 1:].copy()
    N = len(ser)

    for i in range(N - 1):
        z0 = ser[i]
        zf = ser[i + 1]

        if z0 > MHW and zf < MHW:
            # the first (i + 1) makes the index correct for ser
            # the next grabs the next point in the pair

            return (i + 1) + shoreline_idx + 1
    pass


def get_dune_crest(transect, shr_idx, bb_idx):
    """ locate index of dune crest """

    return transect[shr_idx:bb_idx].argmax() + shr_idx


def backbarrier_ecotones(backbarrier, profile, new_key, MHW, MLW):
    """ map different Manning's n based on elevation """

    # map emergent wetlands
    backbarrier[new_key] = 0.05

    # map (subtidal) open water
    backbarrier[new_key].where(backbarrier[profile] > MLW, 0.022, inplace=True)
    return backbarrier


def apply_map(df, profile, time, MHW, MLW, backbar_override=None):
    """ apply Mannings n map """

    shoreline_idx = get_shoreline(df[profile], MHW)
    backbarrier_idx = get_backbarrier(df[profile], shoreline_idx, MHW)

    if backbar_override is not None:
        backbarrier_idx = backbar_override

    new_key = f"{time}_mannings_n"
    df[new_key] = Series(0, index=df.index)

    # map open water ( n = 0.022)
    df.loc[:shoreline_idx, new_key] = 0.022

    # map unconsolidated shore ( n = 0.03 )
    df.loc[shoreline_idx:backbarrier_idx, new_key] = 0.03

    # map backbarrier ecotones
    backbarrier_ecotones(df.loc[backbarrier_idx:], profile, new_key, MHW, MLW)

    return


def align_w_shore(profile, MHW, d=None):
    """TODO: Docstring for align_w_shore.

    :profile: xarray
    :MHW: TODO
    :returns: TODO

    """
    if d is not None:
        coords = {"distance": d, "time": profile.globaltime.values}
        data = profile.values
        return DataArray(data, coords, dims=["distance"]), d
    else:
        d = distance(profile.globalx, profile.globaly)
        shr = get_shoreline(profile, MHW)
        shr_pos = d[shr]
        coords = {"distance": d - shr_pos, "time": profile.globaltime.values}
        data = profile.values
        return DataArray(data, coords, dims=["distance"]), d - shr_pos


def align_data(profile, d):
    """TODO: Docstring for align_data.

    :profile: TODO
    :d: TODO
    :returns: TODO

    """
    coords = {"distance": d, "time": profile.globaltime.values}
    data = profile.values
    return DataArray(data, coords, dims=["distance"])


def concat_aligned_profiles(ds, nys, new_axis, var='zb', MHW=0.25, t=-1):
    """put aligned profiles into multi-dimensional DataSet

    :ds: TODO
    :nys: TODO
    :new_axis: TODO
    :returns: TODO

    """
    profiles = []
    for ny in nys:
        profile = ds[var][t, ny, :]
        aligned_profile, _ = align_w_shore(
                profile, MHW).interp(distance=new_axis)
        profiles.append(aligned_profile)
        pass
    return concat(profiles, 'y')


# ploting
def plot_profiles(df, ax, profiles, kwargs):
    df.plot(x="distance", ax=ax, y=profiles, **kwargs)
    ax.set_xlim([6600, 7450])
    ax.set_ylim([-4, 3])
    ax.invert_xaxis()
    ax.set_ylabel("elevation (m)")
    ax.set_xlabel("cross-shore distance")
    ax.grid(alpha=0.5)
    pass


def plot_dune(df, profiles):
    fig, ax = plt.subplots()
    df.plot(x="distance", y=profiles, ax=ax, color="k")
    ax.set_xlim([6600, 7450])
    ax.set_ylim([-4, 3])
    ax.invert_xaxis()
    ax.set_ylabel("elevation (m)")
    ax.set_xlabel("cross-shore distance")
    ax.grid(alpha=0.5)

    return fig, ax


def plot_mannings(ax, df, profile, mannings_n):
    """ simply twin axis and plot mannings n next to profile elevation """
    ax2 = ax.twinx()

    df.plot(x="distance", y=profile, color="k", ax=ax, label="topography")
    df.plot(x="distance", y=mannings_n, color="r", ax=ax2, label="roughness")

    ax.set_ylabel("elevation (m)")
    ax.legend(loc=2)
    ax.set_xlim(6500, 7750)
    ax.set_ylim(-4, 4)
    ax.invert_xaxis()

    ax2.set_ylabel("Mannings n")
    ax2.spines["right"].set_color("red")
    ax2.tick_params(axis="y", colors="red")
    ax2.yaxis.label.set_color("red")

    plt.sca(ax)

    return (ax, ax2)
