print("####################################################")
print("####################################################")
print("####                                             ###")
print("####   Cálculo da vazão em função da corrente    ###")
print("####    do sensor de pressão diferencial da      ###")
print("####  placa de orifício do reator TRIGA IPR-R1   ###")
print("####                                             ###")
print("####                                             ###")
print("####     Autor: Thalles Oliveira Campagnani      ###")
print("####                                             ###")
print("####                                             ###")
print("####################################################")
print("####################################################")
print("")
print("")


import numpy as np
import matplotlib.pyplot as plt
def calc_vazao_aproximado(bits,a=20/8191,b=0, c=18.69762797471173, d=-74.1111240972653, e = 2.417):
    res = e * np.sqrt((bits*a+b)*c+d)
    if res > 0:
        return res
    else:
        return 0

bits_entrada = []
pressao_calculada = []
delta_1b = []

for bit in np.arange(0, 8191, 1):
    bits_entrada.append(bit)
    pressao_calculada.append(calc_vazao_aproximado(bit))
    delta_1b.append(calc_vazao_aproximado(bit+1)-calc_vazao_aproximado(bit))
    
    
    
# Plotando os gráficos
plt.figure(figsize=(12, 6))
plt.plot(bits_entrada, pressao_calculada, linewidth=3, color="red", marker='s', markerfacecolor='lightcoral', markersize=4,  label="Calculada")
#plt.plot(bits_entrada, delta_1b, linewidth=3, color="green",   label="delta")
plt.xlabel('Leitura PLC (bits)')
plt.ylabel('Vazão (m³/h)')
plt.legend()
plt.title('Vazão em função da corrente')
plt.grid(True)
plt.tight_layout()
plt.show()


