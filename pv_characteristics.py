#!/usr/bin/env python

# http://plasticphotovoltaics.com/lc/characterization/lc-measure.html

import sys
import numpy
import scipy.optimize
import scipy.interpolate
import matplotlib.pyplot

# Datafile name, csv
# first col: Voltage
# second col: Current
# first row: Header
# delimiter: semicolon
datafile = sys.argv[1]

data = numpy.genfromtxt(datafile, unpack=True, delimiter=";", skip_header=1)
print data

v = data[0]
c = -1*data[1]
c2 = data[1]**2 # squared to find root for Voc
p = v * c

fv = scipy.interpolate.interp1d(v, c, kind='cubic')
fv2 = scipy.interpolate.interp1d(v, c2, kind='cubic')
fp = scipy.interpolate.interp1d(v, p, kind='cubic')

voltage = numpy.linspace(v[0], v[-1], 50)
current = fv(voltage)
power   = fp(voltage)

# Opencircuit Voltage
Voc = scipy.optimize.fmin(lambda x: fv2(x), v[-1]/2)
# Shortcircuit Current
Isc = fv(0)
# Pmax Voltage
Vpmax = scipy.optimize.fmin(lambda x: -fp(x), 0)
# Pmax Current
Ipmax = fv(Vpmax)
# Pmax
Pmax = Ipmax * Vpmax
# Fill Factor
FF = (Ipmax*Vpmax) / (Isc*Voc)

print '--------------------------'
print 'PV Characteristics'
print '--------------------------'
print 'Data: ', datafile 
print '--------------------------'
print 'Voc:  ', Voc
print 'Isc:  ', Isc
print 'Pmax: ', Pmax
print 'Vpmax:', Vpmax
print 'Ipmax:', Ipmax
print 'FF:   ', FF
print '--------------------------'

matplotlib.pyplot.title("PV Characteristics")

matplotlib.pyplot.plot(v,c,'o', voltage, current, '-', voltage, power, '--')
matplotlib.pyplot.plot(0, Isc,'ro')
matplotlib.pyplot.plot(Voc, 0,'ro')
matplotlib.pyplot.plot(Vpmax, Ipmax,'ro')
matplotlib.pyplot.plot(Vpmax, Pmax,'ro')

matplotlib.pyplot.axhline(0)
matplotlib.pyplot.axvline(0)
matplotlib.pyplot.grid()
matplotlib.pyplot.xlabel('Voltage [V]')
matplotlib.pyplot.ylabel('Current [A], Power [W]')

matplotlib.pyplot.show()


