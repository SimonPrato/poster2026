from matplotlib import pyplot as plt
import numpy as np
import scienceplots  # You need to install this package first via: pip install SciencePlots


def setup_plot_style():
    """Configure matplotlib with IEEE publication style."""
    plt.style.use(['science', 'ieee'])
    plt.rcParams.update({'figure.dpi': '100'})


def plot_phase_shift(columns_phase_shift, frequencies, antenna_type):
    """
    Plot phase shift comparison between two waveports over frequency.
    
    Args:
        columns_phase_shift: Array containing frequency and phase data for both waveports
        frequencies: Frequency array
        antenna_type: String identifier for antenna type
    """
    setup_plot_style()
    
    antenna_name = antenna_type.replace('-', ' ')
    fig, ax = plt.subplots(figsize=(4, 3))
    #fig, ax = plt.subplots(figsize=(7, 3.5))     # 2:1 aspect ratio (wide)

    # Extract phase data
    phase_waveport1 = columns_phase_shift[1]
    phase_waveport2 = columns_phase_shift[2]

    # Plot phase curves
    ax.plot(frequencies / 1e9, phase_waveport1, label='Output port 1')
    ax.plot(frequencies / 1e9, phase_waveport2, label='Output port 2')

    # First delta annotation (at 1/4 position)
    idx_first = phase_waveport1.size // 4
    marker1_y_first = phase_waveport1[idx_first]
    marker2_y_first = phase_waveport2[idx_first]
    delta_first = marker1_y_first - marker2_y_first
    
    ax.plot(columns_phase_shift[0][idx_first], marker1_y_first, 
            marker='.', markersize=5, color='C0')
    ax.plot(columns_phase_shift[0][idx_first], marker2_y_first, 
            marker='.', markersize=5, color='C1')
    ax.text(columns_phase_shift[0][idx_first] + 0.05, 
            (marker1_y_first + marker2_y_first) / 2, 
            rf'$\Delta$ = {delta_first:.2f} rad',
            fontsize=8, ha='left')
    #ax.annotate('', 
    #            xy=(columns_phase_shift[0][idx_first], marker2_y_first),
    #            xytext=(columns_phase_shift[0][idx_first], marker1_y_first),
    #            arrowprops=dict(arrowstyle='<->', lw=0.8))

    # Second delta annotation (at 3/4 position)
    idx_second = (phase_waveport1.size // 4) * 3
    marker1_y_second = phase_waveport1[idx_second]
    marker2_y_second = phase_waveport2[idx_second]
    delta_second = marker1_y_second - marker2_y_second
    
    ax.plot(columns_phase_shift[0][idx_second], marker1_y_second, 
            marker='.', markersize=5, color='C0')
    ax.plot(columns_phase_shift[0][idx_second], marker2_y_second, 
            marker='.', markersize=5, color='C1')
    ax.text(columns_phase_shift[0][idx_second] - 0.0, 
            (marker1_y_second + marker2_y_second) / 2 + 0.15, 
            rf'$\Delta$ = {delta_second:.2f} rad',
            fontsize=8, ha='left')
    #ax.annotate('', 
    #            xy=(columns_phase_shift[0][idx_second], marker2_y_second),
    #            xytext=(columns_phase_shift[0][idx_second], marker1_y_second),
    #            arrowprops=dict(arrowstyle='<->', lw=0.8))

    # Configure axes and labels
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Phase Shift (rad)')
    ax.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))

    # Adjust y-axis limits to fit data
    phase_max = max(np.max(phase_waveport1), np.max(phase_waveport2))
    phase_min = min(np.min(phase_waveport1), np.min(phase_waveport2))
    ax.set_ylim(phase_min, phase_max)

    # Configure grid
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle='--', alpha=0.5)
    ax.minorticks_on()

    # Configure legend
    legend = ax.legend(frameon=True)
    legend.get_frame().set_facecolor('white')

    # Finalize plot
    fig.tight_layout()
    fig.savefig(f"output/plots/phase.png", dpi=600)
    plt.show()


def plot_moments(m_e, m_m, frequencies, antenna_type):
    """
    Plot electric and magnetic dipole moments over frequency.
    
    Args:
        m_e: Electric dipole moment array
        m_m: Magnetic dipole moment array
        frequencies: Frequency array
        antenna_type: String identifier for antenna type
    """
    setup_plot_style()
    
    antenna_name = antenna_type.replace('-', ' ')
    normalized_m_e = np.abs(m_e) * 377
    
    fig, ax1 = plt.subplots(figsize=(4, 3))
    #fig, ax1 = plt.subplots(figsize=(7, 3.5))     # 2:1 aspect ratio (wide)
    
    # Plot electric dipole moment on primary y-axis
    ax1.set_xlabel('Frequency (GHz)')
    ax1.set_ylabel(r'Electric Dipole Moment $\left|m_e\right|\cdot 377 \Omega$ (Vm)')
    ax1.plot(frequencies / 1e9, normalized_m_e, 
             label=r'$\left|m_e\right| \cdot 377 \Omega$')
    ax1.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))
    ax1.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    
    # Configure grid
    ax1.grid(which='major', linestyle='-')
    ax1.grid(which='minor', linestyle='--', alpha=0.5)
    ax1.minorticks_on()
    
    # Plot magnetic dipole moment on secondary y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'Magnetic Dipole Moment $\left|m_m\right|$ (Vm)', color="red")
    ax2.plot(frequencies / 1e9, np.abs(m_m), 
             label=r'$\left|m_m\right|$', 
             linestyle='--', color="red")
    ax2.tick_params(axis='y', labelcolor="red")
    ax2.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    
    # Set matching y-axis limits
    max_value = max(np.max(normalized_m_e), np.max(np.abs(m_m)))
    min_value = min(np.min(normalized_m_e), np.min(np.abs(m_m)))
    ax1.set_ylim(min_value-2e-4, max_value)
    ax2.set_ylim(min_value-2e-4, max_value)
    ax2.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))
    
    # Configure legend - positioned in top left
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = ax1.legend(lines1 + lines2, labels1 + labels2, 
                       loc='upper left', frameon=True)
    legend.get_frame().set_facecolor('white')
    
    # Finalize plot
    fig.tight_layout()
    fig.savefig(f"output/plots/dipole-moments.png", dpi=600)
    plt.show()

def plot_output_power_e_field(frequencies, output_power, e_field, antenna_type):
    """
    Plot electric field and output power over frequency.
    
    Args:
        frequencies: Frequency array
        output_power: Output power array
        e_field: Electric field array
        antenna_type: String identifier for antenna type
    """
    setup_plot_style()
    
    fig, ax1 = plt.subplots(figsize=(4, 3))
    #fig, ax1 = plt.subplots(figsize=(7, 3.5))     # 2:1 aspect ratio (wide)
    
    # Plot electric field on primary y-axis
    ax1.set_xlabel('Frequency (GHz)')
    ax1.set_ylabel(r'$|E_y|$ (V/m)')
    ax1.plot(frequencies / 1e9, e_field, label='$E_{y}$')
    ax1.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))
    ax1.set_ylim(0, np.max(e_field))
    #ax1.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    
    # Configure grid
    ax1.grid(which='major', linestyle='-')
    ax1.grid(which='minor', linestyle='--', alpha=0.5)
    ax1.minorticks_on()
    
    # Plot output power on secondary y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Output power (µW)', color="red")
    ax2.plot(frequencies / 1e9, output_power*1e6, 
             linestyle='--', label='Output power', color="red")
    #ax2.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax2.tick_params(axis='y', labelcolor="red")
    
    # Configure legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True)
    legend.get_frame().set_facecolor('white')
    
    # Finalize plot
    fig.tight_layout()
    fig.savefig(f"output/plots/output-power.png", dpi=600)
    plt.show()
