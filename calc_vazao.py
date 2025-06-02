print("####################################################")
print("####################################################")
print("####                                             ###")
print("####   Cálculo da vazão em função da pressão     ###")
print("####      diferencial da placa de orifício       ###")
print("####          do reator TRIGA IPR-R1             ###")
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

def calc_vazao_aproximado(delta_p, a = 2.417):
    '''
    Função para calcular a vazão aproximada a partir de determinada diferença de pressão nos lados da placa de orifício.
    
    Entradas:
        delta_p (float):    Diferença de pressão em mbar.
        a (float):          Constante de ajuste da função (encontrado por regressão).
        
    Saída:
        Vazão em m³/h (float)
    '''
    return a * np.sqrt(delta_p)
    
    
def calc_vazao_interativo(delta_p, qtd_iteracoes = 5, grafico_iteracoes=False):
    '''
    Função para calcular a vazão a partir de determinada diferença de pressão nos lados da placa de orifício.
    
    Entradas:
        delta_p (float):            Diferença de pressão em mbar.
        qtd_iteracoes (int):        Quantidade de interações para cálculo da velocidade (e consequentimente vazão).
        grafico_iteracoes (bool):   Se verdadeiro, plota gráfico da vazão e velocidade em função de cada iteração para verificar convergência.
        
    Saída:
        Vazão em m³/h (float)
    '''
    
    # Se a diferença de pressão for nula, retorne a vazão como nula sem fazer cálculos (evita divisão por 0)
    if(delta_p==0):
        return 0
    
    ############# Definição de constantes #############
    
    # Diâmetro da tubulação [m]:
    D = 0.068484

    # Diâmetro do orificio da placa em [m]:
    d = 0.05097

    # Densidade do fluxo a montante da placa de orifício em [kg/m³]:
    rho_1 = 994.24      #a 35°C, conforme MILLER (1989)

    # Viscosidade dinâmica do fluido [kg/m]
    mi = 0.000995       #a 35°C, conforme MILLER (1989)
    
    # Razão entre o diâmetro do orifício da placa e o diâmetro da tubulação [adimensional]:
    Beta = d/D

    # Fator de velocidade [admensional]:
    E = (1 - Beta**4)**(-1/2)

    #Relação entre a 'distância da tomada de pressão até o orificio da placa' e o 'diâmetro interno da tubulação'
    L_1 = 0.0254/D   # 1 polegada (distância) convertida em metros = 0.0254
    L_2 = 0.0254/D   # Mesma distância


    ############# Conversão da variável de entrada #############

    # Pressão diferencial através do orifício da placa em [Pa]  <--- Variável que será usada nos cálculos
    # (converte mbar para Pa)
    delta_p_PA = delta_p*100
    
    
    ############# Cálculo iterativo #############

    # Velocidade [m/s]
    u = 50 #Chute inicial

    # Listas para armazenar a sequência de valores de cada iteração
    n_iteracao = []         #número da iteração
    m_dot_sequencia = []
    vazao_sequencia = []
    u_sequencia = []
    nRey_sequencia = []

    # Foi estabelecido 5 iterações no cabeçalho da função como padrão, mas pode ser alterado
    for i in range(0, qtd_iteracoes):
        # Número de Reynolds do escoamento na tubulação
        nRey = u * rho_1 * D / mi

        # Coeficiente de descarga [adimensional]:
        # Equação de Reader-Harris/Gallagher (1998)?
        C = (
            0.5959
            + 0.0312 * Beta**2.1
            - 0.1840 * Beta**8
            + 0.0029 * Beta**2.5 * (10**6/nRey)**0.75
            + 0.0900 * L_1 * Beta**4 * (1-Beta**4)**(-1)
            - 0.0337 * L_2 * Beta**3
            )

        # Fluxo de massa em [kg/s]
        # Equação fornecida por ISO (1980) e DIN (1982)
        m_dot = C * E * np.pi/4 * d**2 * np.sqrt(2 * delta_p_PA * rho_1)
        
        # Vazão [m³/h]
        vazao = m_dot/rho_1*3600
        
        # Adiciona novos valores na sequência
        n_iteracao.append(i)
        m_dot_sequencia.append(m_dot)
        vazao_sequencia.append(vazao)
        u_sequencia.append(u)
        nRey_sequencia.append(nRey)
        
        ######## Fim dessa iteração, aqui já inicia o cálculo para próxima ########
        
        # Calcula nova velocidade
        u = m_dot / (rho_1 * (np.pi/4 * D**2))  # u = m_dot / (rho * A), onde A é a área da tubulação
        
        
    # Plota o gráfico das iterações, caso solicitado
    if (grafico_iteracoes):
        # Plotando os gráficos
        plt.figure(figsize=(12, 6))

        # Subplot da vazão (vazão) de cada iteração
        plt.subplot(1, 2, 1)
        plt.plot(n_iteracao, vazao_sequencia, 'b-', linewidth=2)
        plt.xlabel('Número da iteração')
        plt.ylabel('Vazão (m³/h)')
        plt.title('Vazão vs Iterações')
        plt.grid(True)

        # Subplot da velocidade (u) de cada iteração
        plt.subplot(1, 2, 2)
        plt.plot(n_iteracao, u_sequencia, 'r-', linewidth=2)
        plt.xlabel('Número da iteração')
        plt.ylabel('Velocidade (m/s)')
        plt.title('Velocidade vs Iterações')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

        
    #print("Vazão: ", vazao)
    return vazao


################################################
# Plota gráfico da vazão de 0 a 300 mbar
################################################

# Listas para armazenar sequência de valores
delta_p_sequencia = []
vazao_sequencia = []
aproximação_sequencia = []
diff_sequencia = []

# Usando intervalo de 0.1 para maior precisão no início do gráfico
for delta_p in np.arange(0, 300, 0.1): #300 mbar = 30.000 Pa
    # Calcula vazão usando a função interativa calc_vazao_interativo()
    vazao = calc_vazao_interativo(delta_p)
    
    # Calcula vazão usando a função calc_vazao_aproximado()
    aproximação = calc_vazao_aproximado(delta_p)
    
    # Calcula diferença percentual entre os resultados
    if vazao==0:
        diff = None
    else:
        diff = 100*(vazao-aproximação)/vazao
    
    # Adiciona novos valores na sequência
    delta_p_sequencia.append(delta_p)
    vazao_sequencia.append(vazao)
    aproximação_sequencia.append(aproximação)
    diff_sequencia.append(diff)

# Plotando os gráficos
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
# Gráfico do fluxo de massa (m_dot)
plt.plot(delta_p_sequencia, vazao_sequencia,       linewidth=6, color="green", label="Fórmula iterativo")
plt.plot(delta_p_sequencia, aproximação_sequencia, linewidth=3, color="red",   label="Fórmula aproximado")
plt.xlabel('Diferença de pressão (mbar)')
plt.ylabel('Vazão (m³/h)')
plt.legend()
plt.title('Vazão em função da diferença de pressão')
plt.grid(True)
plt.tight_layout()

plt.subplot(2, 1, 2)
# Gráfico da diferença percentual entre gráficos
plt.plot(delta_p_sequencia, diff_sequencia, linewidth=2, color='blue', label="Diferença %")
plt.xlabel('Diferença de pressão (mbar)')
plt.ylabel('Diferença percentual entre formulas (%)')
#plt.legend()
plt.title('Diferença percentual em função da diferença de pressão')
plt.grid(True)
plt.tight_layout()
plt.show()


################################################
# Gera tabela com valores na faixa de trabalho
################################################

tabela_deltaP_vazao = []
tabela_deltaP_vazao.append([121.47 , calc_vazao_interativo(121.47)])
tabela_deltaP_vazao.append([131.23 , calc_vazao_interativo(131.23)])
tabela_deltaP_vazao.append([141.46 , calc_vazao_interativo(141.46)])
tabela_deltaP_vazao.append([151.16 , calc_vazao_interativo(151.16)])
tabela_deltaP_vazao.append([163.36 , calc_vazao_interativo(163.36)])
tabela_deltaP_vazao.append([173.21 , calc_vazao_interativo(173.21)])
tabela_deltaP_vazao.append([187.90 , calc_vazao_interativo(187.90)])
tabela_deltaP_vazao.append([194.23 , calc_vazao_interativo(194.23)])
tabela_deltaP_vazao.append([201.60 , calc_vazao_interativo(201.60)])

print("")
print("")
print("")
print("Tabela com valores na faixa de trabalho:")
print("")
print("Pressão |       Vazão")
print("--------|--------------------")
for i in range (0,len(tabela_deltaP_vazao)):
    print(tabela_deltaP_vazao[i][0], "\t| ", tabela_deltaP_vazao[i][1])
print("")
print("")
