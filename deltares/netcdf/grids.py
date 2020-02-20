# code to work with netcdf output
# the layout of netcdf output 2D arrays is:
#    .---------------------/ /----------------------.
#    :           :                    :             :
#    :  (1, 1)   :                    :   (1, m)    :
#    :           :                    :             :
#    .--------------------/ /-----------------------.
#    :           :                    :             :
#    :           :                    :             :
#    :           :                    :             :
#    =           =                    =             =
#    :           :                    :             :
#    :  (n, 1)   :                    :   (n, m)    :
#    :           :                    :             :
#    .--------------------/ /-----------------------.
#   where n is the number of y grid center points
#   where m is the number of x grids center


class Grid:

    """Holds arrays for grid coordinates and administration as attributes.
    The basic idea is to have a collection of attributes for grid manipulation,
    operations on the grid, and referencing.
    """

    def __init__(self, dataset):
        """create grid attributes"""
        self.cell_center_x = dataset['globalx'][:, :]
        self.cell_center_y = dataset['globaly'][:, :]

    def get_coords(self, m, n):
        """return specific coordinates at (n, m)

        :m: 2 dim array of integer indices **IN THE GRID's ADMINISTRATION**
        :n: 2 dim array of integer indecies
        :returns: a tuple of arrays with dimension of m and n
        """

        # put in grid administation indicies. m=1 the zeroth index in python
        m -= 1
        n -= 1

        x = self.cell_center_x[n, m]
        y = self.cell_center_y[n, m]

        return (x, y)

    def get_column(self, m):
        """return mth column

        :n: row index **IN THE GRID's ADMINISTRATION**
        :returns: tuple of coordinate arrays

        """
        m -= 1

        x = self.cell_center_x[:, m]
        y = self.cell_center_y[:, m]

        return (x, y)

    def get_row(self, n):
        """return nth row

        :n: row index **IN THE GRID's ADMINISTRATION**
        :returns: tuple of coordinate arrays

        """
        n -= 1

        x = self.cell_center_x[n, :]
        y = self.cell_center_y[n, :]

        return (x, y)
