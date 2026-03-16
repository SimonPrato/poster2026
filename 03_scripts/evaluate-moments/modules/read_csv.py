import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from typing import List, Tuple
from pathlib import Path


# === Common interpolation frequency axis ===
# All CSV data is resampled onto this shared frequency grid (in GHz).
FREQ_START_GHZ  = 1e-3   # 1 MHz
FREQ_STOP_GHZ   = 3.0    # 3 GHz
FREQ_NUM_POINTS = 1000   # 1 MHz to 3 GHz across 1000 points
FREQ_AXIS_GHZ   = np.linspace(FREQ_START_GHZ, FREQ_STOP_GHZ, FREQ_NUM_POINTS)


def read_antenna_data(antenna_type: str) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Read phase shift and magnitude data from CSV files for antenna analysis.
    All data columns are interpolated onto a common frequency axis
    (1 MHz to 3 GHz) using quadratic (2nd-order) interpolation.

    Args:
        antenna_type: Identifier for antenna (e.g., 'loop', 'dipole').

    Returns:
        Tuple of (phase_data, magnitude_data).
        Each is a list of numpy arrays aligned to FREQ_AXIS_GHZ.
        Element [0] of each list is the common frequency axis (GHz).
    """
    data_dir = Path("data") / antenna_type

    phase_data     = _read_and_interpolate(data_dir / "phase.csv")
    magnitude_data = _read_and_interpolate(data_dir / "magnitude.csv")

    return phase_data, magnitude_data


def _read_and_interpolate(csv_path: Path) -> List[np.ndarray]:
    """
    Read a CSV file and interpolate every data column onto FREQ_AXIS_GHZ
    using quadratic (2nd-order) spline interpolation.

    Expects:
      - First column : frequency axis in GHz.
      - Remaining columns : data values to interpolate.

    The target range [FREQ_START_GHZ, FREQ_STOP_GHZ] must lie fully within
    the data's own frequency span; extrapolation is not allowed and raises
    a ValueError with a descriptive message.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        List of numpy arrays:
          [0] – FREQ_AXIS_GHZ (the shared frequency axis, in GHz)
          [1] – first data column interpolated onto FREQ_AXIS_GHZ
          [2] – second data column interpolated onto FREQ_AXIS_GHZ
          ...
    """
    df = pd.read_csv(csv_path, header=None, dtype=float, skiprows=1)
    raw_columns = [df[col].to_numpy()[1:] for col in df.columns]

    freq_raw  = raw_columns[0]   # frequency axis from the CSV (GHz)
    data_cols = raw_columns[1:]  # remaining columns

    # Guard: target range must be inside the raw data span
    if FREQ_START_GHZ < freq_raw.min() or FREQ_STOP_GHZ > freq_raw.max():
        raise ValueError(
            f"{csv_path.name}: interpolation target "
            f"[{FREQ_START_GHZ:.4f} GHz, {FREQ_STOP_GHZ:.4f} GHz] "
            f"exceeds the available data span "
            f"[{freq_raw.min():.4f} GHz, {freq_raw.max():.4f} GHz]. "
            "Reduce FREQ_START_GHZ / FREQ_STOP_GHZ or extend the CSV data."
        )

    # Interpolate each data column with a quadratic (2nd-order) spline
    interpolated: List[np.ndarray] = [FREQ_AXIS_GHZ]
    for col in data_cols:
        interp_fn = interp1d(freq_raw, col, kind="quadratic", assume_sorted=False)
        interpolated.append(interp_fn(FREQ_AXIS_GHZ))

    return interpolated
