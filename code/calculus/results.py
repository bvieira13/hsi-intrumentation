import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Conversão de milímetros para polegadas
largura_in = 8
altura_in = 6

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

def read_data(file_path):
        x_data = []
        y_data = []

        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains two values separated by a tab
                values = line.strip().split(',')
                x_data.append(float(values[0]))
                y_data.append(float(values[1]))
        return x_data, y_data

def load_cie_data():
        wavelenght, Vlamda = read_data("CIE-sle-photopic.csv")
        return wavelenght, Vlamda

def responsivity_from_qe():
    wavelenght, quantum_eff = read_data('qe-dcc1545m.csv')
    Kg = 237
    Re_max = 2.1*Kg
    qe_max = 0.56
    Re_lambda = []
    wavelenght = list(np.linspace(400,720,33))
    for wave in wavelenght:
        temp = wave*quantum_eff[wavelenght.index(wave)]*Re_max/(550*qe_max)
        Re_lambda.append(temp)
        temp *= 1e-2
        # print(f"{round(wave,1)} {temp:.2f}")
    return wavelenght, Re_lambda

def max_luminous_exp(Vsat, texp):
    wl, R = responsivity_from_qe()
    area = 5.2e-6**2*1280*1024
    irradiance = np.divide(Vsat,np.multiply(R,texp))
    flux = np.multiply(irradiance,area)
    wavelenght = list(np.linspace(400,720,33))
    return wavelenght, irradiance, flux

def plot_radiant_responsivity():
    x, y = responsivity_from_qe()
    wavelenght, quantum_eff = read_data('qe-dcc1545m.csv')
    y =np.multiply(1e-2,y)
    # Criando o gráfico principal
    fig, ax1 = plt.subplots(figsize=(largura_in,altura_in))

    # Plotando os dados de responsividade com linha sólida
    color = 'tab:red'
    ax1.set_xlabel('Comprimento de onda [nm]')
    ax1.set_ylabel('Responsividade espectral [V/($\mu$J/cm$^2$)]', color=color)
    ax1.plot(x, y, color=color, linestyle='-', label='R$_{\mathsf{e},\lambda}$')  # Linha sólida para responsividade
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(400, 720)
    ax1.set_ylim(0, 6)
    ax1.legend(loc='lower left')
    ax1.set_xticks(np.arange(400, 721, 40))
    ax1.grid(which='major', linestyle='-', linewidth='0.5', color='black')

    # Criando um segundo eixo Y para a eficiência quântica
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Eficiência Quântica [%]', color=color)
    ax2.plot(wavelenght, quantum_eff, color=color, linestyle='--',label='EQ')  # Linha tracejada para eficiência quântica
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 0.6)  # Ajuste conforme necessário
    ax2.legend(loc='lower right')
    # Salvando o gráfico
    fig.savefig("spectral-responsivity-quantum-eff.pdf",dpi=300)

def max_radiometric_estimation():
    Vsat = 1.2
    texp = 40e-6
    wl = np.zeros((5,33))
    Ee = np.zeros((5,33))
    phi = np.zeros((5,33))
    wl[0,:], Ee[0,:], phi[0,:] = max_luminous_exp(Vsat,texp)
    texp = 1e-3
    wl[1,:], Ee[1,:], phi[1,:] = max_luminous_exp(Vsat,texp)
    texp = 10e-3
    wl[2,:], Ee[2,:], phi[2,:] = max_luminous_exp(Vsat,texp)
    texp = 100e-3
    wl[3,:], Ee[3,:], phi[3,:] = max_luminous_exp(Vsat,texp)
    texp = 983e-3
    wl[4,:], Ee[4,:], phi[4,:] = max_luminous_exp(Vsat,texp)

    return wl, Ee, phi

def plot_radiometric_graph():
    wl, Ee, phi = max_radiometric_estimation()
    Ee *= 1e3
    fig_irr = plt.figure(figsize=(largura_in,altura_in))
    plt.semilogy(wl[0],Ee[0],label="t$_{exp}$ = 0,04 ms",linestyle='-',linewidth=2)
    plt.semilogy(wl[1],Ee[1],label="t$_{exp}$ = 1 ms",linestyle='--',linewidth=2)
    plt.semilogy(wl[2],Ee[2],label="t$_{exp}$ = 10 ms",linestyle='-.',linewidth=2)
    plt.semilogy(wl[3],Ee[3],label="t$_{exp}$ = 100 ms",linestyle=':',linewidth=2)
    plt.semilogy(wl[4],Ee[4],label="t$_{exp}$ = 983 ms",linestyle='-',marker='o',linewidth=2)
    plt.xlabel('Comprimento de onda [nm]')
    plt.ylabel('Irradiancia espectral [mW/m$^2$/nm]')
    plt.xlim(400,720)
    plt.ylim(1,1e6)
    plt.xticks(np.arange(400, 721, 40))
    plt.legend(loc='best', ncol=3,facecolor=(0.9, 0.9, 0.9, 0.15),fontsize=14) 
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', axis='y', linestyle=':', color='gray')       
    fig_irr.savefig("max-spectral-flux-density-mt9m001.pdf",dpi=300)

    phi *=1e3
    fig_phi = plt.figure(figsize=(largura_in,altura_in))
    plt.semilogy(wl[0],phi[0],label="t$_{exp}$ = 0,04 ms",linestyle='-',linewidth=2)
    plt.semilogy(wl[1],phi[1],label="t$_{exp}$ = 1 ms",linestyle='--',linewidth=2)
    plt.semilogy(wl[2],phi[2],label="t$_{exp}$ = 10 ms",linestyle='-.',linewidth=2)
    plt.semilogy(wl[3],phi[3],label="t$_{exp}$ = 100 ms",linestyle=':',linewidth=2)
    plt.semilogy(wl[4],phi[4],label="t$_{exp}$ = 983 ms",linestyle='-',marker='o',linewidth=2)
    plt.xlabel('Comprimento de onda [nm]')
    plt.ylabel('Fluxo radiante espectral [mW/nm]')
    plt.xlim(400,720)
    plt.ylim(1e-5,1e2)
    plt.xticks(np.arange(400, 721, 40))
    plt.legend(loc='best', ncol=3,facecolor=(0.9, 0.9, 0.9, 0.15),fontsize=14)
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', axis='y', linestyle=':', color='gray')
    fig_phi.savefig("max-spectral-flux-mt9m001.pdf",dpi=300)

def optical_consideration():
    wl, Ee, phi = max_radiometric_estimation()
    phi *=1e3
    wave, Tlctf = read_data('transmitance-lctf.csv')
    Tlctf = np.divide(Tlctf,100)
    Tlens = np.ones(Tlctf.shape)
    Ttotal = np.multiply(Tlctf,Tlens)
    phi_t = np.divide(phi,Ttotal)
    return wl, phi_t

def plot_system_spectral_response():
    wl, phi = optical_consideration()     
    fig_phi = plt.figure(figsize=(largura_in,altura_in))
    plt.semilogy(wl[0],phi[0],label="t$_{exp}$ = 0,04 ms",linestyle='-',linewidth=2)
    plt.semilogy(wl[1],phi[1],label="t$_{exp}$ = 1 ms",linestyle='--',linewidth=2)
    plt.semilogy(wl[2],phi[2],label="t$_{exp}$ = 10 ms",linestyle='-.',linewidth=2)
    plt.semilogy(wl[3],phi[3],label="t$_{exp}$ = 100 ms",linestyle=':',linewidth=2)
    plt.semilogy(wl[4],phi[4],label="t$_{exp}$ = 983 ms",linestyle='-',marker='o',linewidth=2)
    plt.xlabel('Comprimento de onda [nm]')
    plt.ylabel('Fluxo radiante espectral [mW/nm]')
    plt.xlim(400,720)
    plt.ylim(1e-4,1e3)
    plt.xticks(np.arange(400, 721, 40))
    plt.legend(loc='best', ncol=3,facecolor=(0.9, 0.9, 0.9, 0.15),fontsize=14)
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', axis='y', linestyle=':', color='gray')
    fig_phi.savefig("max-spectral-flux-mt9m001-wo.pdf",dpi=300)

# TODO: Implementar interpolação para extrair valor exato do gráfico
def plot_floating_capacitance():  
    min_lithografic_size, cfd = read_data('floating-diff-capacitance.csv')     
    fig_phi = plt.figure(figsize=(largura_in,altura_in))
    plt.plot(min_lithografic_size,cfd,linestyle='-',linewidth=2)
    plt.xlabel('Tamanho mínimo de característica litográfica [$\mu$m]')
    plt.ylabel('Capacitância de difusão flutuante [fF]')
    plt.xlim(0,2)
    plt.ylim(0,20)
    plt.xticks(np.arange(0, 2.1, 0.5))
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    fig_phi.savefig("floating-diff-capacitance.pdf",dpi=300)

if __name__ == "__main__":
    # This block will only be executed if the script is run directly
    plot_radiant_responsivity()
    plot_radiometric_graph()
    plot_system_spectral_response()
    plot_floating_capacitance()