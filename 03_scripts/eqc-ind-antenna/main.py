import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from calculate_moments import calc

# === Common interpolation frequency axis ===
FREQ_START_GHZ  = 1e-3   # 1 MHz
FREQ_STOP_GHZ   = 3.0    # 3 GHz
FREQ_NUM_POINTS = 1000
FREQ_AXIS_GHZ   = np.linspace(FREQ_START_GHZ, FREQ_STOP_GHZ, FREQ_NUM_POINTS)
FREQ_AXIS_HZ    = FREQ_AXIS_GHZ * 1e9


def load_csv_column(file_path, column_index, skiprows=1, unwrap_phase=False):
    """
    Load a column from a CSV file, interpolating onto the shared 1 MHz–3 GHz
    frequency axis (1000 points, linear interpolation).

    Column 0 is always treated as the frequency axis (GHz).
    Requesting column_index=0 returns FREQ_AXIS_GHZ directly.
    Any other column_index is interpolated onto FREQ_AXIS_GHZ.

    Set unwrap_phase=True for phase columns to correct ±π wrap-arounds
    before interpolation.
    """
    data = pd.read_csv(file_path, header=None, dtype=float, skiprows=skiprows)
    columns = [data[col].to_numpy() for col in data.columns]

    if column_index == 0:
        return FREQ_AXIS_GHZ

    freq_raw = columns[0]
    col_raw  = np.unwrap(columns[column_index]) if unwrap_phase else columns[column_index]

    interp_fn = interp1d(freq_raw, col_raw, kind='linear', assume_sorted=False)
    return interp_fn(FREQ_AXIS_GHZ)


def compute_dipole_moments(frequencies, output_power, s_phase_1,
                           s_phase_2, feed_voltage, tem_impedance,
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
            feed_voltage[i],
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
    # Create a DataFrame with the data
    df = pd.DataFrame({
        'Frequency [GHz]': frequencies/1e9,
        'Electric Dipole Moment (m_e) [A·m]': m_e,
        'Magnetic Dipole Moment (m_m) [V/m]': m_m
    })

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


def main():
    antenna_name = "loop"  # Example: rename this to your actual antenna label

    # Load antenna free-space data
    # All CSV files now have Freq [GHz] as col 0, data value(s) from col 1 onward
    antenna_capacitance  = load_csv_column('data/loop-free-space/capacitance.csv', 1)
    antenna_inductance   = load_csv_column('data/loop-free-space/inductance.csv',  1)
    frequencies          = load_csv_column('data/loop-free-space/capacitance.csv', 0) * 1e9

    # Load TEM cell (empty) data
    tem_cell_capacitance = load_csv_column('data/tem-cell-empty/capacitance.csv', 1)
    tem_cell_inductance  = load_csv_column('data/tem-cell-empty/inductance.csv',  1)

    # Load loop-in-TEM-cell data
    impedance_magnitude = load_csv_column('data/loop-tem-cell/impedance.csv', 1)
    impedance_phase_deg = load_csv_column('data/loop-tem-cell/impedance.csv', 2)
    antenna_tem_impedance = impedance_magnitude * np.exp(1j * np.deg2rad(impedance_phase_deg))

    s_param_mag  = load_csv_column('data/loop-tem-cell/magnitude.csv', 1)
    output_power = np.power(10.0, s_param_mag / 10)  # Assuming 1W input power
    print(output_power)

    # phase.csv cols: 0=Freq, 1=wp1_ez_phase, 2=wp2_ez_phase, 3=atan(voltage)
    wp1_voltage_phase     = load_csv_column('data/loop-tem-cell/phase.csv', 1, unwrap_phase=True)
    wp2_voltage_phase     = load_csv_column('data/loop-tem-cell/phase.csv', 2, unwrap_phase=True)
    antenna_voltage_phase = load_csv_column('data/loop-tem-cell/phase.csv', 3, unwrap_phase=True)
    phase_shift_1 = wp1_voltage_phase - antenna_voltage_phase
    phase_shift_2 = wp2_voltage_phase - antenna_voltage_phase

    antenna_feed_voltage = load_csv_column('data/loop-tem-cell/feed-voltage.csv', 1)

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
