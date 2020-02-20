import cartopy.crs as ccrs
from matplotlib.pyplot import subplots


def format_nc_name(name):
    """convert netCDF name to regular string

    :name: TODO
    :returns: TODO

    """
    name = name[name != b' ']
    return ''.join([b.decode('utf-8') for b in list(name.data)])


def point_ts(ds, var, point, ax):
    """TODO: Docstring for point_ts.

    :ds: TODO
    :var: TODO
    :point: TODO
    :: TODO
    :returns: TODO

    """
    var = f"point_{var}"

    line = ds[var][:, point].plot(ax=ax, lw=1.5, color="b")

    ax.set_xlabel("")

    return line


def field_variable(ds, var, time, idx=None):
    """TODO: Docstring for field_variable.

    :ds: TODO
    :var: TODO
    :time: TODO
    :idx: TODO
    :returns: TODO

    """

    try:
        ds = ds.rename({'globalx': 'x', 'globaly': 'y'})
    except ValueError:
        pass

    if idx is not None:
        try:
            data = ds[var][idx, :, :]
        except IndexError as e:
            print(e)
            raise
    else:
        try:
            data = ds[var].isel(time=time)
        except IndexError as e:
            print(e)
            raise

    try:
        x = ds.x.values
        y = ds.y.values

        xmin = x[x != 0].min()
        xmax = x[x != 0].max()

        ymin = y[y != 0].min()
        ymax = y[y != 0].max()

        xc = (xmax + xmin) / 2
        yc = (ymax + ymin) / 2
    except AttributeError as e:
        print("Coordinates are not labeled (x, y)")
        print(e)
        pass

    fig, ax = subplots(
        figsize=(24, 9), subplot_kw={"projection": ccrs.TransverseMercator(xc, yc)}
    )

    data.where(data.x != 0).plot.contourf(
        ax=ax,
        transform=ccrs.TransverseMercator(xc, yc),
        x="x",
        y="y",
        add_colorbar=True,
        levels=25,
    )

    return fig, ax
