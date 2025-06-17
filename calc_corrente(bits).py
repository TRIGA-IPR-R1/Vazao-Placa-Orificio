print("####################################################")
print("####################################################")
print("####                                             ###")
print("####    Cálculo da corrente em função do valor   ###")
print("####      lido pelo ADC do PLC do sistema de     ###")
print("####  aquisição de dados do reator TRIGA IPR-R1  ###")
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


'''
De acordo com o a configuração do PLC para essa porta:
4mA  = bit 0
20mA = bit 8192
'''

def calc_corrente(bits,a=16/8192,b=4):
    return bits*a+b


## Cálculos
bits = []
corrente_calculada = []
for bit in range(0,8191):
    bits.append(bit)
    corrente_calculada.append(calc_corrente(bit))



# Plotando os gráficos
plt.figure(figsize=(12, 6))
plt.plot(bits, corrente_calculada, linewidth=3, color="red",   label="Calculada")
plt.xlabel('Bits')
plt.ylabel('Corrente (mA)')
plt.legend()
plt.title('Corrente em função dos bits do ADC')
plt.grid(True)
plt.tight_layout()
plt.show()
