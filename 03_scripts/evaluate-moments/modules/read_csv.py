import pandas as pd
import numpy as np
from typing import List, Tuple
from pathlib import Path


def read_antenna_data(antenna_type: str) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Read phase shift, magnitude, and E-field data from CSV files for antenna analysis.
    
    Args:
        antenna_type: Identifier for antenna (e.g., 'loop', 'dipole')
        
    Returns:
        Tuple of (phase_data, magnitude_data, efield_data) where each is a list of numpy arrays
        representing different columns from the CSV files.
    """
    data_dir = Path("data") / antenna_type
    
    # Read phase shift data
    phase_data = _read_csv_columns(data_dir / "phase.csv")
    
    # Read magnitude data  
    magnitude_data = _read_csv_columns(data_dir / "magnitude.csv")
    
    return phase_data, magnitude_data


def _read_csv_columns(csv_path: Path) -> List[np.ndarray]:
    """
    Helper function to read CSV and extract data columns as numpy arrays.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of numpy arrays, one per column (excluding first row)
    """
    df = pd.read_csv(csv_path, header=None, dtype=float, skiprows=1)
    return [df[col].to_numpy()[1:] for col in df.columns]

