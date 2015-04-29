import qpoint as qp
import numpy as np
import healpy as hp

# initialize, maybe change a few options from their defaults
Q = qp.QPoint(accuracy='low', fast_math=True, mean_aber=True,
              num_threads=4)

print 'simulate pointing'

# dumb simulation
n = 100000
ctime = 1418662800. + np.arange(n)/100.
az = 100. + 40.*np.sin(2*np.pi*np.arange(n)/4000.)
el = 32. + 10.*np.mod(np.arange(n,dtype=float),500000.)/500000.
el = np.floor(el/0.1)*0.1
pitch = None # np.zeros_like(ctime)
roll = None # np.zeros_like(ctime)
lat = -77.6*np.ones_like(ctime)
lon = 165.7 - np.arange(n)*3/850000.

# step waveplate twice a day...
lmst = Q.lmst(ctime, lon)
hwp = np.ones_like(lmst)
hwp[lmst<=12] = 22.5
hwp[lmst>12] = 45.0
q_hwp = Q.hwp_quat(hwp)

# calculate boresight quaternions
q_bore = Q.azel2bore(az, el, pitch, roll, lon, lat, ctime)

# detector offset in degrees
delta_az = 1.0
delta_el = -1.0
delta_psi = 22.5

q_off = Q.det_offset(delta_az, delta_el, delta_psi)

# calculate detector pointing
ra, dec, sin2psi, cos2psi = Q.bore2radec(q_off, ctime, q_bore, q_hwp=q_hwp)

# calculate healpix pixel numbers
pix, sin2psi, cos2psi = Q.bore2pix(q_off, ctime, q_bore, q_hwp=q_hwp)

print ra.min(), ra.max()
print dec.min(), dec.max()
print pix.min(), pix.max()
