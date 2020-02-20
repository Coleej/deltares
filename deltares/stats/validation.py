import matplotlib.pyplot as plt
from numpy import nanmean, nanstd, nanvar, sqrt, nansum


# some stats
def bias(obs, mod):
    """retuns bias (mean error) of model results given observations"""

    return nanmean(mod - obs)


def rel_bias(obs, mod):
    """calculate bias normalized by observations"""

    return nanmean(mod / obs) - 1


def rmse(obs, mod):
    """returns RMSE of model results given observations"""
    arg = (mod - obs) ** 2

    return sqrt(nanmean(arg))


def rel_rmse(obs, mod):
    """returns RMSE of model results given observations"""
    arg = ((mod - obs) / obs) ** 2

    return sqrt(nanmean(arg))

def mse_norm(obs, mod):
    """calculate the mean-square-error nomalized by the variance

    :obs: TODO
    :mod: TODO
    :returns: TODO

    """
    mse = nanmean((obs - mod) ** 2)

    return mse / nanvar(obs)


def SI(obs, mod):
    """compute scatter index"""
    sigma = nanstd(mod - obs)

    return sigma / nanmean(abs(obs))


def skill(obs, mod):
    """returns skill of model output

    arguments:
    obs -- the observed data (elvation change) of lenth n
    mod -- the modeled data of lenth n

    notes:
    skill = 1  -->  perfect simulation
    skill = 0  -->  no better than no change
    skill < 0  -->  worse than no change
    """

    if len(obs) != len(mod):
        print("observation data and model output need to be the same length")

        return

    num = nansum((obs - mod) ** 2)
    denom = nansum(obs ** 2)

    return 1 - (num / denom)


def one2one(obs, mod, unit='', label=None, ax=None, stats=True, l45=True):
    """scatter plot with 1-to-1 line and bias window

    :obs: TODO
    :mod: TODO
    :returns: TODO

    """

    if ax is None:
        fig, ax = plt.subplots()
        pass

    lims = (min(list(obs) + list(mod)), max(list(obs) + list(mod)))
    s = ax.plot(
        obs,
        mod,
        ls="none",
        marker="o",
        ms=5,
        label=label
    )

    if l45:
        ax.plot(
            lims,
            lims,
            ls="--",
            color="k",
            lw=2
        )

    opts = {
        "horizontalalignment": "center",
        "verticalalignment": "center",
        "transform": ax.transAxes,
        "fontsize": "small",
    }

    statistics = {
            'bias': bias(obs, mod),
            'rel_bias': rel_bias(obs, mod),
            'rmse': rmse(obs, mod),
            'rel_rmse': rel_rmse(obs, mod),
            'SI': SI(obs, mod)
    }
    if stats:
        ax.text(0.2, 0.9, f"bias={bias(obs, mod):.2f}{unit}", **opts)
        ax.text(0.2, 0.8, f"rmse={rmse(obs, mod):.2f}{unit}", **opts)
        ax.text(0.175, 0.7, f"SI={SI(obs, mod):.2f}", **opts)

    return ax, s, statistics


def norm_time_series(ser1, ser2):
    """normalize (resample) ser1 based on ser2's index

    :ser1: TODO
    :ser2: TODO
    :returns: TODO

    """
    ser1_idx = ser1.index
    new_idx = ser2.index

    return (
        ser1.reindex(ser1_idx.union(new_idx))
        .interpolate("index", limit=2, limit_area="inside")
        .reindex(new_idx)
        .dropna()
    )
