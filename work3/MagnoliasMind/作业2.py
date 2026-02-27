import matplotlib.pyplot as plt
import numpy as np

def logi(x,L=1,k=1,x0=0):
    return L/(1+np.exp(-k*(x-x0)))

x = np.linspace(-6, 6, 400)
y = logi(x)
plt.figure(figsize=(12,12))

plt.subplot(2,2,1)
plt.plot(x,y,label = f'L=1,k=1,x0=0',linewidth = 2)
plt.legend()

plt.subplot(2,2,2)
for L in [0.5,1,1.5,2]:
    y = logi(x,L=L)
    plt.plot(x,y,label = f'L={L},k=1,x0=0',linewidth = 2)
plt.legend()

plt.subplot(2,2,3)
for k in [0.5,1,1.5,2]:
    y = logi(x,L=1,k=k)
    plt.plot(x,y,label = f'L=1,k={k},x0=0',linewidth = 2)
plt.legend()

plt.subplot(2,2,4)
for x0 in [-1,0,1,2]:
    y = logi(x,L=1,k=1,x0 = x0)
    plt.plot(x,y,label = f'L=1,k=1,x0={x0}',linewidth = 2)
plt.legend()

plt.tight_layout()
plt.show()