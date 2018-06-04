import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import rc
from amuse.lab import *
from amuse.plot import *
from amuse import io
from prepare_figure import single_frame
from distinct_colours import get_distinct
from amuse.units.optparse import OptionParser


def main(filename, radius, snapshot, min_mass, max_mass):
    stars = io.read_set_from_file(filename, 'hdf5', close_file=True)
    stars = stars[np.sqrt(stars.x**2 + stars.y**2 + stars.z**2) < radius]

path = 'temp2/2500/fast/0/'
timerange = range(100000, 1200000, 100000)
steps = len(timerange)
colors = get_distinct(steps)

N = 99
num_bins = 100
bin_edges = 0
size_limit_au = 100.
radius_limit = 1000.

x_label = 'x (AU)'
y_label = 'y (AU)$'
fig = plt.figure()
#fig, ax = plt.subplots(3, 3)
#fig, axs = plt.subplots(3, 3, facecolor='w', edgecolor='k')

axs = []

steps = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000, 1750000, 2000000]

#1
for i in range(len(steps)):
	r_path = path + str(steps[i]) + '.hdf5'
	print(r_path)
	low_x, low_y, low_z = [], [], []
	high_x, high_y, high_z = [], [], []
	e = io.read_set_from_file(r_path, 'hdf5')
	x = e.x.value_in(units.parsec)
	y = e.y.value_in(units.parsec)
	z = e.z.value_in(units.parsec)
	radius = e.radius.value_in(units.AU)

	j = 0

	while j < 2500:
		r = radius[j]

		if r < radius_limit:
			low_x.append(x[j])
			low_y.append(y[j])
			low_z.append(z[j])
		else:
			high_x.append(x[j])
			high_y.append(y[j])
			high_z.append(z[j])

		j += 1

	low_x = np.array(low_x)
	low_y = np.array(low_y)
	low_z = np.array(low_z)
	high_x = np.array(high_x)
	high_y = np.array(high_y)
	high_z = np.array(high_z)

	#fig.add_subplot(3, 3, i + 1, xlim=(-5, 5), ylim=(-5, 5))
	#plt.plot(low_x, low_y, 'bo', label=str(len(radius)))
	#plt.plot(high_x, high_y, 'ro')
	#print(i, len(low_x)+len(high_x))

	axs.append(fig.add_subplot(3, 3, i + 1, projection='3d'))
	axs[i].plot(low_x, low_y, low_z, 'bo')
	axs[i].plot(high_x, high_y, high_z, 'ro', label=str(len(radius)))
	axs[i].set_xlim([-5, 5])
	axs[i].set_ylim([-5, 5])

plt.legend(loc='lower right', prop={'size': 6})
plt.show()


def new_option_parser():
    result = OptionParser()
    result.add_option("-f",
                      dest="filename", default="proto_solar_cluster.hdf5",
                      help="input filename [%default]")
    result.add_option("-R", unit=units.parsec,
                      dest="radius", type="float", default=100 | units.parsec,
                      help="cluster radius to plot (pc) [%default]")
    result.add_option("-t", unit=units.Gyr,
                      dest="snapshot", type="float", default=4.6 | units.Gyr,
                      help="snapshot to plot (Myr) [%default]")
    result.add_option("-m", unit=units.MSun,
                      dest="min_mass", type="float", default=0.1,
                      help="Minimum stellar mass to plot (MSun) [%default]")
    result.add_option("-M", unit=units.MSun,
                      dest="max_mass", type="float", default=100,
                      help="Maximum stellar mass to plot (Msun) [%default]")
    return result


if __name__ in ('__main__', '__plot__'):
    o, arguments = new_option_parser().parse_args()
    main(**o.__dict__)