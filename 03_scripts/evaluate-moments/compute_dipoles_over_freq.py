from scipy.optimize import curve_fit
from modules.read_csv import *
from modules.calculate_moments import *
from modules.plot_moments import *

import numpy as np
import matplotlib.pyplot as plt


# === Configuration ===
antenna_power = 1.0  # in Watts
antenna_type = "loop" # same name as data folder to be read

# === Data Loading ===
columns_phase_shift, columns_magnitude = read_antenna_data(antenna_type=antenna_type)

# Convert frequencies from GHz to Hz
frequencies = columns_phase_shift[0] * 1e9

# Adjust positive phase values by subtracting 2π, if desired
#columns_phase_shift[1][columns_phase_shift[1] > 0] -= 2 * np.pi
#columns_phase_shift[2][columns_phase_shift[2] < 0] += 2 * np.pi

# === Phase, Magnitude, and E-Field Processing ===
#columns_phase_shift[1] -= np.pi # Subtract np.pi if necessary
#columns_phase_shift[2] += np.pi # Subtract np.pi if necessary

phase_shift = columns_phase_shift[1] - columns_phase_shift[2]


# Compute output power from dB magnitude
magnitude = columns_magnitude[1]
output_power = antenna_power * np.power(10.0, magnitude / 10.0)
waveport_impedance = 50
tem_cell_height = 24e-3
efield = np.sqrt(output_power * 50) * np.sqrt(2) / (tem_cell_height / 2)

# === Plotting and Moment Calculations ===
plot_phase_shift(columns_phase_shift, frequencies, antenna_type)

m_e, m_m = calculate_moments(efield, phase_shift, output_power, frequencies)
plot_moments(m_e, m_m, frequencies, antenna_type)

# Optional: visualize power and E-field relationship
plot_output_power_e_field(frequencies, output_power, efield, antenna_type)
frequencies = frequencies / 1e9
data = np.column_stack((frequencies, output_power))
np.savetxt('output/csv/output-power.csv', data, delimiter=',',
header='Frequency (GHz),Output Power (W)')


frequencies = frequencies * 1e9
def model_func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

# Fit curve
popt, pcov = curve_fit(model_func, frequencies, m_e)

# Parameters fitted
a_e, b_e, c_e , d_e = popt

# Fit curve
popt, pcov = curve_fit(model_func, frequencies, m_m)

# Parameters fitted
a_m, b_m, c_m, d_m = popt

print(f"===================================================================================================================")
print(f"The dipole moments are expressed as a function of frequency below.")
print(f"This terminal output can be copied and inserted in the magnitude expression of each dipole moment.")
print(f"-------------------")
print(f"Electric Dipole Moments fitted parameters: ({a_e}) * Freq * Freq * Freq + ({b_e}) * Freq * Freq + ({c_e}) * Freq + ({d_e})")
print(f"Magnetic Dipole Moments fitted parameters: ({a_m}) * Freq * Freq * Freq + ({b_m}) * Freq * Freq + ({c_m}) * Freq + ({d_m})")
print(f"===================================================================================================================")

def model_func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

# Fit curve
popt, pcov = curve_fit(model_func, frequencies, m_e)

# Parameters fitted
a_e, b_e, c_e , d_e = popt

# Fit curve
popt, pcov = curve_fit(model_func, frequencies, m_m)

# Parameters fitted
a_m, b_m, c_m, d_m = popt



