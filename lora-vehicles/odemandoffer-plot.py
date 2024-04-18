import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definizione delle equazioni differenziali
def model(y, t, k, c):
    P, V = y
    dPdt = k * V * (1 - P)
    dVdt = - (V - c / (P + k * V * (1 - P)) )
    #print ( P, " ", dPdt, " ", V, " ", dVdt, " ", P * V, " \n")
    return [dPdt, dVdt]

# Condizioni iniziali
P0 = 0.1  # Percentuale iniziale di lora-based vehicles
V0 = 1  # Valore iniziale del profitto pro capite

# Parametri del modello
k = 0.1  # Costante che regola l'incentivo per nuovi utenti di istallare dispasitivi LoRa sui veicoli
c = P0 * V0

# Intervallo temporale
t = np.linspace(0, 10, 100)

# Risoluzione numerica delle equazioni differenziali
y0 = [P0, V0]
y = odeint(model, y0, t, args=(k,c))

# Plot del risultato
plt.plot(t, y[:, 0], label='Percentuale di veicoli LoRa')
plt.plot(t, y[:, 1], label='Profitto pro capite')
plt.xlabel('Tempo')
plt.ylabel('Valore')
plt.title('Variazione della percentuale di veicoli LoRa')
plt.legend()
plt.grid()
plt.show()
