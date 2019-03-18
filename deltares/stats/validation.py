from numpy import nanmean, sqrt, isnan
from scipy.stats import linregress


def bias(obs, mod):
    """retuns bias (mean error) of model results given observations"""
    return nanmean(mod - obs)


def rmse(obs, mod):
    """returns RMSE of model results given observations"""
    arg = (mod - obs)**2
    return sqrt(nanmean(arg))


def r2(obs, mod):
    """simple wrapper around scipy.stats.linregress to return r-squared"""
    inan = isnan(obs) | isnan(mod)
    _, _, r_val, _, _ = linregress(obs[~inan], mod[~inan])
    return r_val**2
