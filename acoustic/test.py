import numpy as np
import matplotlib.pyplot as plt
t = np.arange(0, 1, 0.01)
f = 1
phase_init = 0
sinx = np.sin( 2* np.pi *f * t + phase_init)
time_shift = int(f/4/0.01)
cosx = np.roll(sinx, -time_shift)
# cosx = np.cos( 2* np.pi *f * t + phase_init)
mag =  (sinx**2 + cosx**2) ** 0.5
pha = np.arctan2(sinx, cosx)
plt.subplot(3, 1, 1)
plt.plot(sinx)
plt.plot(cosx)
plt.subplot(3, 1, 2)
plt.plot(mag)
plt.subplot(3, 1, 3)
plt.plot(pha)
plt.show()