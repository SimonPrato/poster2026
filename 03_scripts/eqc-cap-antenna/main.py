import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calculate_moments import calc


def load_csv_column(file_path, column_index, skiprows=1):
    """Load a specific column from a CSV file as a NumPy array."""
    data = pd.read_csv(file_path, header=None, dtype=float, skiprows=skiprows)
    # Corrected indexing to ensure it grabs the specific column index requested
    return data.iloc[:, column_index].to_numpy()


def compute_dipole_moments(frequencies, output_power, s_phase_1,
                           s_phase_2, feed_current, tem_impedance,
                           tem_cell_capacitance, tem_cell_inductance,
                           antenna_inductance, antenna_capacitance):
    """Calculate dipole moments for all frequency values."""
    m_e = []
    m_m = []
    for i, freq in enumerate(frequencies):
        result = calc(
            output_power[i],
            s_phase_1[i],
            s_phase_2[i],
            feed_current[i], # Updated parameter
            tem_impedance[i],
            tem_cell_inductance[i],
            tem_cell_capacitance[i],
            antenna_inductance[i],
            antenna_capacitance[i],
            freq
        )
        m_e.append(result['equ_ele_dipole_moment'])
        m_m.append(result['equ_mag_dipole_moment'])
    return m_e, m_m


def plot_dipole_moments(frequencies, m_e, m_m, antenna_name):
    """Plot normalized electric and magnetic dipole moments over frequency."""
    normed_m_e = np.abs(m_e) * 377  # normalize electric dipole moment
    abs_m_m = np.abs(m_m)

    plt.style.use(['science', 'ieee'])
    fig, ax1 = plt.subplots(figsize=(3.9, 2.64))

    # Left Y-axis: Electric dipole moment
    ax1.set_xlabel('Frequency [GHz]')
    ax1.set_ylabel(r'Electric Dipole Moment $\left|m_e\right|\cdot 377\ \Omega$ [V/m]', color='tab:red')
    ax1.plot(frequencies / 1e9, normed_m_e, color='tab:red', label=r'$\left|m_e\right|\cdot 377\Omega$')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.minorticks_on()
    ax1.grid(which='major', linestyle='-', linewidth=0.5, color='#BBBBBB')
    ax1.grid(which='minor', linestyle=':', linewidth=0.4, color='#DDDDDD')
    ax1.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    # Right Y-axis: Magnetic dipole moment
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'Magnetic Dipole Moment $\left|m_m\right|$ [V/m]', color='tab:blue')
    ax2.plot(frequencies / 1e9, abs_m_m, color='tab:blue', linestyle="--", label=r'$\left|m_m\right|$')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    # Synchronize Y-axis limits
    max_val = max(np.max(normed_m_e), np.max(abs_m_m))
    ax1.set_ylim(0, max_val)
    ax2.set_ylim(0, max_val)
    ax1.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))
    ax2.set_xlim(np.min(frequencies / 1e9), np.max(frequencies / 1e9))

    # Title and legend
    fig.suptitle(f'Dipole Moments of {antenna_name} Antenna in TEM Cell', y=0.93)
    fig.tight_layout()
    legend = fig.legend(loc='upper left', bbox_to_anchor=(0.15, 0.82), frameon=True)
    legend.get_frame().set_facecolor('white')

    fig.savefig(f"output/{antenna_name}.png", dpi=600)
    plt.show()


def save_dipole_moments_to_csv(frequencies, m_e, m_m, output_file):
    """Save frequencies and dipole moments to a CSV file."""
    df = pd.DataFrame({
        'Frequency [GHz]': frequencies/1e9,
        'Electric Dipole Moment normalized (m_e) [V·m]': m_e,
        'Magnetic Dipole Moment (m_m) [V·m]': m_m
    })

    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


def main():
    antenna_name = "monopole"  # Updated name

    # Load antenna free-space data (updated paths)
    antenna_capacitance = load_csv_column(f'data/{antenna_name}-free-space/capacitance.csv', 2)
    antenna_inductance = load_csv_column(f'data/{antenna_name}-free-space/inductance.csv', 2)
    frequencies = load_csv_column(f'data/{antenna_name}-free-space/capacitance.csv', 1) * 1e9

    # Load TEM cell (empty) data
    tem_cell_capacitance = load_csv_column('data/tem-cell-empty/capacitance.csv', 2)
    tem_cell_inductance = load_csv_column('data/tem-cell-empty/inductance.csv', 2)

    # Load monopole-in-TEM-cell data (updated paths)
    impedance_magnitude = load_csv_column(f'data/{antenna_name}-tem-cell/impedance.csv', 1)
    impedance_phase_deg = load_csv_column(f'data/{antenna_name}-tem-cell/impedance.csv', 2)
    antenna_tem_impedance = impedance_magnitude * np.exp(1j * np.deg2rad(impedance_phase_deg))

    s_param_mag = load_csv_column(f'data/{antenna_name}-tem-cell/magnitude.csv', 1)
    output_power = np.power(10.0, s_param_mag / 10)

    # Updated paths for phase
    wp1_voltage_phase = load_csv_column(f'data/{antenna_name}-tem-cell/phase.csv', 1) 
    wp2_voltage_phase = load_csv_column(f'data/{antenna_name}-tem-cell/phase.csv', 2) 
    antenna_voltage_phase = load_csv_column(f'data/{antenna_name}-tem-cell/phase.csv', 3) 
    phase_shift_1 = wp1_voltage_phase - antenna_voltage_phase
    phase_shift_2 = wp2_voltage_phase - antenna_voltage_phase

    antenna_feed_voltage = load_csv_column(f'data/{antenna_name}-tem-cell/feed-voltage.csv', 1)

    # Compute dipole moments
    m_e, m_m = compute_dipole_moments(
        frequencies,
        output_power,
        phase_shift_1,
        phase_shift_2,
        antenna_feed_voltage,
        antenna_tem_impedance,
        tem_cell_capacitance,
        tem_cell_inductance,
        antenna_inductance,
        antenna_capacitance
    )

    # Plot results
    plot_dipole_moments(frequencies, m_e, m_m, antenna_name)

    # Save dipole moments to csv file
    output_csv = f"output/{antenna_name}_dipole_moments.csv"
    save_dipole_moments_to_csv(frequencies, np.abs(np.multiply(m_e, 377)), np.abs(m_m), output_csv)


if __name__ == "__main__":
    main()
