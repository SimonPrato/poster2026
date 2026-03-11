import numpy as np
import scienceplots

def calc(output_power, output_voltage_phase_1, output_voltage_phase_2, 
         input_voltage, input_impedance, tem_inductance,
         tem_capacitance, antenna_inductance, antenna_capacitance, frequency):
    """
    Calculates currents in a circuit model with two output phases.
    
    Parameters:
    -----------
    output_power : float
        Output power in Watts.
    output_voltage_phase_1 : float
        Phase angle for output voltage phase 1 in radians.
    output_voltage_phase_2 : float
        Phase angle for output voltage phase 2 in radians.
    input_voltage : complex
        Input voltage.
    input_impedance : complex
        Input impedance.
    frequency : float
        Frequency in Hz.
    
    Returns:
    --------
    dict
        Dictionary containing all calculated variables.
    """
    # Output voltages
    u_1 = np.sqrt(output_power * 50) * np.exp(1j * output_voltage_phase_1)
    u_2 = np.sqrt(output_power * 50) * np.exp(1j * output_voltage_phase_2)

    # Hint: all voltages (including input voltage) must be effective values

    # Component values
    ct = tem_capacitance / 2 # tem cell capacitance
    lt = tem_inductance / 2# tem cell inductance
    ca = antenna_capacitance# antenna capacitance
    la = antenna_inductance # antenna inductance 

    # circuit values
    i_ca = input_voltage * 1j * 2 * np.pi * frequency * ca
    i = input_voltage / input_impedance
    i_r1 = u_1 / 50
    i_r2 = u_2 / 50
    i_ct1 = u_1 * 1j * 2 * np.pi * frequency * ct
    i_ct2 = u_2 * 1j * 2 * np.pi * frequency * ct
    i_lt1 = i_r1 + i_ct1
    i_lt2 = i_r2 + i_ct2
    i_ck = i_lt1 + i_lt2
    i_la = i - i_ca
    u_la = i_la * 2 * np.pi * frequency * la
    i_ma = i_la - i_ck
    r_c_parallel = 1/(1/50+1j*2*np.pi*frequency*ct)
    u_lt1 = 1j * 2 * np.pi * frequency * lt * i_lt1 # Note: Without induced voltage considered
    u_lt2 = 1j * 2 * np.pi * frequency * lt * i_lt2 # Note: Without induced voltage considered
    # induced voltage across septum inductors:
    induced_voltage = np.sqrt((((u_1 - u_2) - (- u_lt1 + u_lt2)) * r_c_parallel/(1j * 2*np.pi*frequency*lt+r_c_parallel))**2/50)
    m = (induced_voltage / 2 - 1j * 2 * np.pi * frequency * i_lt1 * lt ) / (1j * 2 * np.pi * frequency * i_la) # Probably to be corrected
    inductive_power = np.conj(i_la) * input_voltage * np.cos(np.angle(i_la))
    a_minus_b = induced_voltage
    # Note: Effective voltages are used here
    equ_mag_dipole_moment = 1j * a_minus_b / (416.6666* 2 * np.pi * frequency) * 299792458 * 2 * np.pi * frequency * 1.256637 * pow(10.0,-6)
    a_plus_b = np.sqrt((i_ck * 1/50 / (1/50 + 1j * 2 * np.pi * frequency * ct))**2 * 50) 
    equ_ele_dipole_moment = a_plus_b / 416.6666
    variables = [i_ca, i, i_r1, i_r2, i_ct1, i_ct2, i_lt1, i_lt2, i_ck, i_la, m, equ_mag_dipole_moment, equ_ele_dipole_moment, 1e12 * ct, 1e12 * lt, 1e12 * ca, 1e12 * la, u_1, u_2, input_impedance, induced_voltage]
    names = ['i_ca', 'i', 'i_r1', 'i_r2', 'i_ct1', 'i_ct2', 'i_lt1', 'i_lt2', 'i_ck', 'i_la', 'm', 'equ_mag_dipole_moment', 'equ_ele_dipole_moment', 'ct', 'lt', 'ca', 'la', 'u_1', 'u_2', 'input_impedance', 'induced_voltage']

    print(f"======================================================\nfreq: {frequency/1e9}\n input voltage: {input_voltage}\n output power: {output_power}\noutput voltage: {np.abs(u_1)}")
    for name, var in zip(names, variables):
        if np.iscomplexobj(var):
            mag = np.abs(var)
            angle_rad = np.angle(var)
            angle_deg = np.degrees(angle_rad)
            print(f"{name:15}: |{mag:8.8f}| ∠{angle_deg:7.5f}° ({angle_rad:7.4f} rad)")
        else:
            print(f"{name:15}: {var:8.8f} (real)")

    # Also print real scalars
    print(f"inductive_power      : {inductive_power:.4f}")
    print(f"a_minus_b           : {a_minus_b:.4f}")
    print(f"a_plus_b            : {a_plus_b:.4f}")
    print(f"equ_ele_dipole_moment: {equ_ele_dipole_moment:.4f}")

    # Collect all calculated variables
    results = {
        'u_1': u_1,
        'u_2': u_2,
        'ct': ct,
        'lt': lt,
        'ca': ca,
        'la': la,
        'i_ca': i_ca,
        'i': i,
        'i_r1': i_r1,
        'i_r2': i_r2,
        'i_ct1': i_ct1,
        'i_ct2': i_ct2,
        'i_lt1': i_lt1,
        'i_lt2': i_lt2,
        'i_ck': i_ck,
        'i_la': i_la,
        'm': m,
        'inductive_power': inductive_power,
        'a_minus_b': a_minus_b,
        'equ_mag_dipole_moment': equ_mag_dipole_moment,
        'a_plus_b': a_plus_b,
        'equ_ele_dipole_moment': equ_ele_dipole_moment
    }
    
    return results

# Example usage and output of all variables
if __name__ == "__main__":
    results = calc(1.4709888e-5, np.deg2rad(-56.86),
                   np.deg2rad(-244.2), 3.66, 
                   13.91 * np.exp(89.9984), 16.62e-9, 6.57e-12, 2.15e-9, 38.36e-15, 1e9)
    
    print("Calculated variables:")
    for name, value in results.items():
        print(f"{name}: {np.abs(value)} ∠ {np.degrees(np.angle(value))}°")

