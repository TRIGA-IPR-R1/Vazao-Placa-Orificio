print("####################################################")
print("####################################################")
print("####                                             ###")
print("####    Cálculo pressão diferencial da placa     ###")
print("####    de orifício em função da corrente do     ###")
print("####  sensor de pressão do reator TRIGA IPR-R1   ###")
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


## Dados extraídos do certificado de calibração

corrente_instrumento = [
    4.000,
    5.597,
    7.195,
    8.796,
    10.393,
    11.995,
    13.593,
    15.192,
    16.793,
    18.396,
    19.997,
]

pressao_instrumento = [
    0.000,
    29.993,
    59.992,
    89.995,
    119.991,
    149.993,
    179.992,
    209.994,
    239.991,
    269.997,
    299.991,
]


corrente_padrão = [
    4,
    5.6,
    7.2,
    8.8,
    10.4,
    12,
    13.6,
    15.2,
    16.8,
    18.4,
    20,
]

pressao_padrao = [
    0,
    30,
    60,
    90,
    120,
    150,
    180,
    210,
    240,
    270,
    300,
]


## Funções
def calcular_regressao_linear(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - a * sum_x) / n
    
    return a, b

def calc_pressao(corrente,a,b):
    return corrente*a+b


## Cálculos
a,b = calcular_regressao_linear(corrente_instrumento, pressao_instrumento)
print(a,b)

pressao_calculada = []
for corrente in corrente_padrão:
    pressao_calculada.append(calc_pressao(corrente,a,b))



# Plotando os gráficos
plt.figure(figsize=(12, 6))
plt.plot(corrente_instrumento, pressao_instrumento,       linewidth=6, color="green", label="Instumento")
plt.plot(corrente_padrão, pressao_calculada, linewidth=3, color="red",   label="Calculada")
plt.xlabel('Corrente (mA)')
plt.ylabel('Diferença de pressão (mbar)')
plt.legend()
plt.title('Corrente em função da diferença de pressão')
plt.grid(True)
plt.tight_layout()
plt.show()
