import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots


def setup_plot_style():
    """Configure matplotlib with IEEE publication style."""
    plt.style.use(['science', 'ieee'])
    plt.rcParams.update({'figure.dpi': '100'})

def create_ieee_plot(
    data_source,
    x_column,
    y_columns,
    x_label='X axis',
    y_label='Y axis',
    title='Plot',
    output_path='output/plot.png',
    figsize=(7, 3.5), #(4, 3) for half-page, (7, 3.5) for full page width
    legend_labels=None,
    x_limits=None,
    y_limits=None,
    show_grid=True,
    skiprows=0
):
    """
    Create an IEEE-style publication-quality plot from CSV data.

    Parameters
    ----------
    data_source : str or dict
        Path to CSV file or dictionary with x and y data arrays
    x_column : str or int
        Column name (if header exists) or column index for x-axis
    y_columns : str, int, list of str, or list of int
        Column name(s) or index(es) for y-axis
    x_label : str, optional
        Label for x-axis
    y_label : str, optional
        Label for y-axis
    title : str, optional
        Plot title
    output_path : str, optional
        Path to save the figure
    figsize : tuple, optional
        Figure size (width, height) in inches
    legend_labels : list of str, optional
        Custom labels for legend. If None, uses column names
    x_limits : tuple, optional
        Tuple of (min, max) for x-axis limits
    y_limits : tuple, optional
        Tuple of (min, max) for y-axis limits
    show_grid : bool, optional
        Whether to show grid lines
    skiprows : int, optional
        Number of rows to skip at the beginning (e.g., 1 for header row)

    Returns
    -------
    fig, ax : matplotlib figure and axes objects
    """
    setup_plot_style()

    # Load data from CSV or use provided dictionary/arrays
    if isinstance(data_source, str):
        # Try to read CSV with header first
        try:
            df = pd.read_csv(data_source, skiprows=skiprows)

            # Convert to numeric, coercing errors
            if isinstance(x_column, str):
                x_data = pd.to_numeric(df[x_column], errors='coerce').values
            else:
                x_data = pd.to_numeric(df.iloc[:, x_column], errors='coerce').values

            if isinstance(y_columns, (str, int)):
                y_columns = [y_columns]

            y_data_list = []
            for col in y_columns:
                if isinstance(col, str):
                    y_data_list.append(pd.to_numeric(df[col], errors='coerce').values)
                else:
                    y_data_list.append(pd.to_numeric(df.iloc[:, col], errors='coerce').values)

            if legend_labels is None:
                legend_labels = [str(col) for col in y_columns]

        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

    elif isinstance(data_source, dict):
        # Ensure data is numeric numpy arrays
        x_data = np.asarray(data_source[x_column], dtype=float)

        if isinstance(y_columns, str):
            y_columns = [y_columns]

        y_data_list = [np.asarray(data_source[col], dtype=float) for col in y_columns]

        if legend_labels is None:
            legend_labels = y_columns
    else:
        raise ValueError("data_source must be a CSV path or dictionary")

    # Remove NaN values
    valid_mask = ~np.isnan(x_data)
    x_data = x_data[valid_mask]
    y_data_list = [y[valid_mask] for y in y_data_list]

    def model_func(x, a, b, c):
        return a * x**2 + b * x**1 + c

    # Fit curve for first dataset
    #popt, pcov = curve_fit(model_func, x_data, y_data_list[0])
    #a_e, b_e, c_e = popt
    #x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
    #y_data_list[0] = model_func(x_smooth, a_e, b_e, c_e)

    # Fit curve for second dataset
    #popt, pcov = curve_fit(model_func, x_data, y_data_list[1])
    #a_e, b_e, c_e = popt
    #y_data_list[1] = model_func(x_smooth, a_e, b_e, c_e)

    #x_data = x_smooth


    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Plot each y column
    for y_data, label in zip(y_data_list, legend_labels):
        ax.plot(x_data, y_data, label=label)

    if legend_labels and any(label.strip() for label in legend_labels):
        legend = ax.legend(frameon=True)
        legend.get_frame().set_facecolor('white')

    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    #ax.set_yscale('log')
    #ax.set_title(title)

    # Set axis limits
    if x_limits is not None:
        ax.set_xlim(x_limits)
    else:
        ax.set_xlim(np.min(x_data), np.max(x_data))

    if y_limits is not None:
        ax.set_ylim(y_limits)

    # Use scientific notation for y-axis
    #ax.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))

    # Configure grid
    if show_grid:
        ax.grid(which='major', linestyle='-')
        ax.grid(which='minor', linestyle='--', alpha=0.5)
        ax.minorticks_on()

    # Tight layout
    fig.tight_layout()

    # Save figure
    fig.savefig(output_path, dpi=600)

    return fig, ax


def create_ieee_plot_multifile(
    data_sources,
    x_columns,
    y_columns,
    x_label='X axis',
    y_label='Y axis',
    title='Plot',
    output_path='output/plot.png',
    figsize=(4, 3),
    legend_labels=None,
    x_limits=None,
    y_limits=None,
    show_grid=True,
    skiprows=None
):
    """
    Create an IEEE-style plot from multiple CSV files.

    Parameters
    ----------
    data_sources : list of str
        List of paths to CSV files
    x_columns : int, str, or list
        Column for x-axis. Can be:
        - Single int/str: use same x column for all files
        - List of int/str: specific x column for each file
    y_columns : list of int/str or list of lists
        Y columns to plot. Can be:
        - List of int/str: one y column per file
        - List of lists: multiple y columns from each file
    x_label : str, optional
        Label for x-axis
    y_label : str, optional
        Label for y-axis
    title : str, optional
        Plot title
    output_path : str, optional
        Path to save the figure
    figsize : tuple, optional
        Figure size (width, height) in inches
    legend_labels : list of str, optional
        Custom labels for each series. If None, auto-generates labels
    x_limits : tuple, optional
        Tuple of (min, max) for x-axis limits
    y_limits : tuple, optional
        Tuple of (min, max) for y-axis limits
    show_grid : bool, optional
        Whether to show grid lines
    skiprows : int or list of int, optional
        Number of rows to skip. Can be single value or list (one per file)

    Returns
    -------
    fig, ax : matplotlib figure and axes objects

    Examples
    --------
    # Plot column 1 from file1 and column 2 from file2, both using column 0 as x
    create_ieee_plot_multifile(
        data_sources=['file1.csv', 'file2.csv'],
        x_columns=0,
        y_columns=[1, 2],
        legend_labels=['File1 Data', 'File2 Data']
    )

    # Plot multiple columns from multiple files with different x columns
    create_ieee_plot_multifile(
        data_sources=['file1.csv', 'file2.csv'],
        x_columns=[0, 1],  # x from column 0 in file1, column 1 in file2
        y_columns=[[1, 2], [3]],  # columns 1,2 from file1, column 3 from file2
        legend_labels=['F1-C1', 'F1-C2', 'F2-C3']
    )
    """
    setup_plot_style()

    # Normalize inputs
    if not isinstance(data_sources, list):
        data_sources = [data_sources]

    # Handle x_columns
    if isinstance(x_columns, (int, str)):
        x_columns = [x_columns] * len(data_sources)

    # Handle y_columns
    if not isinstance(y_columns[0], list):
        # Single column per file
        y_columns = [[col] for col in y_columns]

    # Handle skiprows
    if skiprows is None:
        skiprows = [0] * len(data_sources)
    elif isinstance(skiprows, int):
        skiprows = [skiprows] * len(data_sources)

    # Collect all data
    all_x_data = []
    all_y_data = []
    all_labels = []

    for idx, (file_path, x_col, y_cols, skip) in enumerate(
        zip(data_sources, x_columns, y_columns, skiprows)
    ):
        try:
            df = pd.read_csv(file_path, skiprows=skip)

            # Get x data
            if isinstance(x_col, str):
                x_data = pd.to_numeric(df[x_col], errors='coerce').values
            else:
                x_data = pd.to_numeric(df.iloc[:, x_col], errors='coerce').values

            # Get y data for each column
            for y_col in y_cols:
                if isinstance(y_col, str):
                    y_data = pd.to_numeric(df[y_col], errors='coerce').values
                    label = f"{file_path.split('/')[-1]}:{y_col}"
                else:
                    y_data = pd.to_numeric(df.iloc[:, y_col], errors='coerce').values
                    label = f"{file_path.split('/')[-1]}:col{y_col}"

                # Remove NaN values
                valid_mask = ~(np.isnan(x_data) | np.isnan(y_data))

                all_x_data.append(x_data[valid_mask])
                all_y_data.append(y_data[valid_mask])
                all_labels.append(label)

        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {e}")

    # Use custom labels if provided
    if legend_labels is not None:
        if len(legend_labels) != len(all_labels):
            raise ValueError(
                f"Number of legend_labels ({len(legend_labels)}) must match "
                f"number of series ({len(all_labels)})"
            )
        all_labels = legend_labels

    def model_func(x, a, b, c):
        return a * x**2 + b * x**1 + c

    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Plot all series
    for index, (x_data, y_data, label) in enumerate(zip(all_x_data, all_y_data, all_labels)):
        if index == 0:
            ax.plot(x_data, y_data, label=label, color="black", linestyle="-")
        elif index == 1:
            ax.plot(x_data, y_data, label=label, color="red", linestyle="-")
        elif index == 2:
            ax.plot(x_data, y_data, label=label, color="black", linestyle="-.")
        elif index == 3:
            ax.plot(x_data, y_data, label=label, color="red", linestyle="-.")
        elif index == 4:
            ax.plot(x_data, y_data, label=label, color="black", linestyle=":")
        elif index == 5:
            ax.plot(x_data, y_data, label=label, color="red", linestyle=":")

    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # Configure legend
    if all_labels:
        #legend = ax.legend(loc='upper left', frameon=True)
        legend = ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        legend.get_frame().set_facecolor('white')

    # Set axis limits
    if x_limits is not None:
        ax.set_xlim(x_limits)

    if y_limits is not None:
        ax.set_ylim(y_limits)

    # Use scientific notation for y-axis
    #ax.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax.set_yscale('log')
    # Configure grid
    if show_grid:
        ax.grid(which='major', linestyle='-')
        ax.grid(which='minor', linestyle='--', alpha=0.5)
        ax.minorticks_on()

    # Tight layout
    fig.tight_layout()

    # Save figure
    fig.savefig(output_path, dpi=600)

    return fig, ax



def create_ieee_plot_dual_yaxis(
    data_source,
    x_column,
    y1_columns,
    y2_columns,
    x_label='X axis',
    y1_label='Y1 axis',
    y2_label='Y2 axis',
    title='Plot',
    output_path='output/plot_dual.png',
    figsize=(7, 3.5),
    y1_legend_labels=None,
    y2_legend_labels=None,
    x_limits=None,
    y1_limits=None,
    y2_limits=None,
    show_grid=True,
    skiprows=0,
    y1_color='C0',
    y2_color='C1'
):
    """
    Create an IEEE-style plot with dual y-axes from CSV data.

    Parameters
    ----------
    data_source : str or dict
        Path to CSV file or dictionary with data arrays
    x_column : str or int
        Column name or index for x-axis
    y1_columns : str, int, or list
        Column(s) for left y-axis
    y2_columns : str, int, or list
        Column(s) for right y-axis
    x_label : str, optional
        Label for x-axis
    y1_label : str, optional
        Label for left y-axis
    y2_label : str, optional
        Label for right y-axis
    title : str, optional
        Plot title
    output_path : str, optional
        Path to save the figure
    figsize : tuple, optional
        Figure size (width, height) in inches
    y1_legend_labels : list of str, optional
        Custom labels for left y-axis series
    y2_legend_labels : list of str, optional
        Custom labels for right y-axis series
    x_limits : tuple, optional
        Tuple of (min, max) for x-axis limits
    y1_limits : tuple, optional
        Tuple of (min, max) for left y-axis limits
    y2_limits : tuple, optional
        Tuple of (min, max) for right y-axis limits
    show_grid : bool, optional
        Whether to show grid lines
    skiprows : int, optional
        Number of rows to skip at the beginning
    y1_color : str, optional
        Color for left y-axis (default: 'C0' - blue)
    y2_color : str, optional
        Color for right y-axis (default: 'C1' - orange)

    Returns
    -------
    fig, ax1, ax2 : matplotlib figure and axes objects

    Examples
    --------
    # Plot voltage on left axis, current on right axis
    create_ieee_plot_dual_yaxis(
        data_source='data.csv',
        x_column='time',
        y1_columns='voltage',
        y2_columns='current',
        x_label='Time (s)',
        y1_label='Voltage (V)',
        y2_label='Current (A)',
        title='Voltage and Current vs Time'
    )
    """
    setup_plot_style()

    # Load data from CSV or dictionary
    if isinstance(data_source, str):
        try:
            df = pd.read_csv(data_source, skiprows=skiprows)

            # Get x data
            if isinstance(x_column, str):
                x_data = pd.to_numeric(df[x_column], errors='coerce').values
            else:
                x_data = pd.to_numeric(df.iloc[:, x_column], errors='coerce').values

            # Process y1 columns
            if isinstance(y1_columns, (str, int)):
                y1_columns = [y1_columns]

            y1_data_list = []
            for col in y1_columns:
                if isinstance(col, str):
                    y1_data_list.append(pd.to_numeric(df[col], errors='coerce').values)
                else:
                    y1_data_list.append(pd.to_numeric(df.iloc[:, col], errors='coerce').values)

            if y1_legend_labels is None:
                y1_legend_labels = [str(col) for col in y1_columns]

            # Process y2 columns
            if isinstance(y2_columns, (str, int)):
                y2_columns = [y2_columns]

            y2_data_list = []
            for col in y2_columns:
                if isinstance(col, str):
                    y2_data_list.append(pd.to_numeric(df[col], errors='coerce').values)
                else:
                    y2_data_list.append(pd.to_numeric(df.iloc[:, col], errors='coerce').values)

            if y2_legend_labels is None:
                y2_legend_labels = [str(col) for col in y2_columns]

        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

    elif isinstance(data_source, dict):
        x_data = np.asarray(data_source[x_column], dtype=float)

        if isinstance(y1_columns, str):
            y1_columns = [y1_columns]
        if isinstance(y2_columns, str):
            y2_columns = [y2_columns]

        y1_data_list = [np.asarray(data_source[col], dtype=float) for col in y1_columns]
        y2_data_list = [np.asarray(data_source[col], dtype=float) for col in y2_columns]

        if y1_legend_labels is None:
            y1_legend_labels = y1_columns
        if y2_legend_labels is None:
            y2_legend_labels = y2_columns
    else:
        raise ValueError("data_source must be a CSV path or dictionary")

    def model_func(x, a, b, c):
        return a * x**2 + b * x**1 + c

    # Remove NaN values
    valid_mask = ~np.isnan(x_data)
    x_data = x_data[valid_mask]
    y1_data_list = [y[valid_mask] for y in y1_data_list]
    y2_data_list = [y[valid_mask] for y in y2_data_list]

    # Fit curve for first dataset
    #popt, pcov = curve_fit(model_func, x_data, y1_data_list[0])
    #a_e, b_e, c_e = popt
    #x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
    #y1_data_list[0] = model_func(x_smooth, a_e, b_e, c_e)

    # Fit curve for second dataset
    #popt, pcov = curve_fit(model_func, x_data, y2_data_list[0])
    #a_e, b_e, c_e = popt
    #y2_data_list[0] = model_func(x_smooth, a_e, b_e, c_e)

    #x_data = x_smooth
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=figsize)

    # Plot y1 data on left axis
    lines1 = []
    for i, (y_data, label) in enumerate(zip(y1_data_list, y1_legend_labels)):
        color = y1_color if len(y1_data_list) == 1 else f'C{i}'
        line = ax1.plot(x_data, y_data, label=label, color="black")
        lines1.extend(line)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color=y1_color)
    ax1.tick_params(axis='y', labelcolor=y1_color)

    # Create secondary y-axis
    ax2 = ax1.twinx()

    # Plot y2 data on right axis
    lines2 = []
    for i, (y_data, label) in enumerate(zip(y2_data_list, y2_legend_labels)):
        color = y2_color if len(y2_data_list) == 1 else f'C{i+len(y1_data_list)}'
        line = ax2.plot(x_data, y_data, label=label, color="red", linestyle='-.')
        lines2.extend(line)

    ax2.set_ylabel(y2_label, color=y2_color)
    ax2.tick_params(axis='y', labelcolor=y2_color)

    # Set title
    ax1.set_title(title)

    # Set axis limits
    if x_limits is not None:
        ax1.set_xlim(x_limits)
    else:
        ax1.set_xlim(np.min(x_data), np.max(x_data))

    if y1_limits is not None:
        ax1.set_ylim(y1_limits)

    if y2_limits is not None:
        ax2.set_ylim(y2_limits)

    # Use scientific notation
    #ax1.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    #ax2.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))

    # Configure grid
    if show_grid:
        ax1.grid(which='major', linestyle='-', alpha=0.7)
        ax1.grid(which='minor', linestyle='--', alpha=0.5)
        ax1.minorticks_on()

    # Combine legends
    all_lines = lines1 + lines2
    all_labels = [line.get_label() for line in all_lines]
    ax1.legend(all_lines, all_labels, loc='lower right', frameon=True)

    # Tight layout
    fig.tight_layout()

    # Save figure
    fig.savefig(output_path, dpi=600, bbox_inches='tight')

    return fig, ax1, ax2


def create_ieee_plot_dual_yaxis_multifile(
    data_sources,
    x_columns,
    y1_columns,
    y2_columns,
    x_label='X axis',
    y1_label='Y1 axis',
    y2_label='Y2 axis',
    title='Plot',
    output_path='output/plot_dual.png',
    figsize=(7, 3.5),
    y1_legend_labels=None,
    y2_legend_labels=None,
    x_limits=None,
    y1_limits=None,
    y2_limits=None,
    show_grid=True,
    skiprows=None,
    y1_color='C0',
    y2_color='C1'
):
    """
    Create an IEEE-style plot with dual y-axes from multiple CSV files.

    Parameters
    ----------
    data_sources : list of str or str
        List of paths to CSV files (or single path)
    x_columns : int, str, or list
        Column for x-axis (shared across files or per-file)
    y1_columns : list
        Columns for left y-axis. Format: [(file_idx, col), ...]
        or simple list if one file
    y2_columns : list
        Columns for right y-axis. Format: [(file_idx, col), ...]
        or simple list if one file
    skiprows : int or list of int, optional
        Number of rows to skip per file

    Other parameters same as create_ieee_plot_dual_yaxis

    Returns
    -------
    fig, ax1, ax2 : matplotlib figure and axes objects

    Examples
    --------
    # Plot from single file
    create_ieee_plot_dual_yaxis_multifile(
        data_sources='data.csv',
        x_columns=0,
        y1_columns=[1, 2],  # Columns 1,2 on left axis
        y2_columns=[3],     # Column 3 on right axis
        y1_label='Power (W)',
        y2_label='Efficiency (%)'
    )

    # Plot from multiple files
    create_ieee_plot_dual_yaxis_multifile(
        data_sources=['file1.csv', 'file2.csv'],
        x_columns=0,
        y1_columns=[(0, 1), (1, 2)],  # file1-col1, file2-col2 on left
        y2_columns=[(0, 3)],           # file1-col3 on right
        y1_legend_labels=['F1', 'F2'],
        y2_legend_labels=['Efficiency']
    )
    """
    setup_plot_style()

    # Normalize inputs
    if not isinstance(data_sources, list):
        data_sources = [data_sources]

    if isinstance(x_columns, (int, str)):
        x_columns = [x_columns] * len(data_sources)

    if skiprows is None:
        skiprows = [0] * len(data_sources)
    elif isinstance(skiprows, int):
        skiprows = [skiprows] * len(data_sources)

    # Load all data files
    dfs = []
    for file_path, skip in zip(data_sources, skiprows):
        try:
            df = pd.read_csv(file_path, skiprows=skip)
            dfs.append(df)
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {e}")

    # Helper function to extract data
    def get_data(file_idx, col):
        df = dfs[file_idx]
        if isinstance(col, str):
            return pd.to_numeric(df[col], errors='coerce').values
        else:
            return pd.to_numeric(df.iloc[:, col], errors='coerce').values

    # Process columns format
    # If simple list, assume single file (file_idx=0)
    if y1_columns and not isinstance(y1_columns[0], tuple):
        y1_columns = [(0, col) for col in y1_columns]
    if y2_columns and not isinstance(y2_columns[0], tuple):
        y2_columns = [(0, col) for col in y2_columns]

    # Get x data (assuming same x for all - use first file's x column)
    x_data = get_data(0, x_columns[0])
    valid_mask = ~np.isnan(x_data)
    x_data = x_data[valid_mask]

    # Collect y1 data
    y1_data_list = []
    for file_idx, col in y1_columns:
        y_data = get_data(file_idx, col)#[valid_mask]
        def model_func(x, a, b, c):
            return a * x**2 + b * x**1 + c

        # Fit curve for first dataset
        #if file_idx==0:
        #    x_x = np.linspace(x_data.min(), x_data.max(), 400)
        #else:
        #    x_x = np.linspace(x_data.min(), x_data.max(), 29)

        #popt, pcov = curve_fit(model_func, x_x, y_data)
        #x_smooth = np.linspace(x_data.min(), x_data.max(), 400)
        #a_e, b_e, c_e = popt
        #y_data = model_func(x_smooth, a_e, b_e, c_e)
        y1_data_list.append(y_data)

    # Collect y2 data
    y2_data_list = []
    for file_idx, col in y2_columns:
        y_data = get_data(file_idx, col)#[valid_mask]
        # Fit curve for first dataset
        #if file_idx==0:
            #x_x = np.linspace(x_data.min(), x_data.max(), 400)
        #else:
            #x_x = np.linspace(x_data.min(), x_data.max(), 29)
        #popt, pcov = curve_fit(model_func, x_x, y_data)
        #x_smooth = np.linspace(x_data.min(), x_data.max(), 400)
        #a_e, b_e, c_e = popt
        #y_data = model_func(x_smooth, a_e, b_e, c_e)
        y2_data_list.append(y_data)

    #x_data = x_smooth

    # Auto-generate labels if not provided
    if y1_legend_labels is None:
        y1_legend_labels = [f'Y1-{i+1}' for i in range(len(y1_data_list))]
    if y2_legend_labels is None:
        y2_legend_labels = [f'Y2-{i+1}' for i in range(len(y2_data_list))]

    # Create figure and axes
    fig, ax1 = plt.subplots(figsize=figsize)

    # Plot y1 data
    lines1 = []
    for i, (y_data, label) in enumerate(zip(y1_data_list, y1_legend_labels)):
        color = y1_color if len(y1_data_list) == 1 else f'C{i}'
        if i==0:
            line = ax1.plot(x_data, y_data, label=label, color="black", linestyle="-.")
        else:
            line = ax1.plot(x_data, y_data, label=label, color="red", linestyle=":")

        lines1.extend(line)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color=y1_color)
    ax1.tick_params(axis='y', labelcolor=y1_color)
    ax1.yaxis.get_major_formatter().set_useOffset(False)

    # Create secondary axis
    ax2 = ax1.twinx()

    # Plot y2 data
    lines2 = []
    for i, (y_data, label) in enumerate(zip(y2_data_list, y2_legend_labels)):
        color = y2_color if len(y2_data_list) == 1 else f'C{i+len(y1_data_list)}'
        if i == 0:
            line = ax2.plot(x_data, y_data, label=label, color="black", linestyle='--')
        else:
            line = ax2.plot(x_data, y_data, label=label, color="red", linestyle='-')

        lines2.extend(line)

    ax2.set_ylabel(y2_label, color=y2_color)
    ax2.tick_params(axis='y', labelcolor=y2_color)
    ax2.yaxis.get_major_formatter().set_useOffset(False)

    ax1.set_title(title)

    # Set limits
    if x_limits is not None:
        ax1.set_xlim(x_limits)
    if y1_limits is not None:
        ax1.set_ylim(y1_limits)
    if y2_limits is not None:
        ax2.set_ylim(y2_limits)

    # Scientific notation
    ax1.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax2.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))

    # Grid
    if show_grid:
        ax1.grid(which='major', linestyle='-', alpha=0.7)
        ax1.grid(which='minor', linestyle='--', alpha=0.5)
        ax1.minorticks_on()

    # Combined legend
    all_lines = lines1 + lines2
    all_labels = [line.get_label() for line in all_lines]
    ax1.legend(all_lines, all_labels, loc='upper left', frameon=True)

    fig.tight_layout()
    fig.savefig(output_path, dpi=600, bbox_inches='tight')

    return fig, ax1, ax2


# Example usage
if __name__ == '__main__':
    plt.rcParams['axes.formatter.useoffset'] = False

    #create_ieee_plot(
    #    data_source="data/loop/electromagnetic-energy.csv",
    #    x_column=0,
    #    y_columns=[1, 2],  
    #    x_label='Frequency (GHz)',
    #    y_label='Energy (J)',
    #    title=r'',
    #    legend_labels=['Magnetic energy', 'Electric energy'],
    #    output_path='output/loop_electromagnetic_energy.png',
    #    x_limits=(0, 3),
    #    y_limits=(1e-14, 1e-9)
    #)
    #create_ieee_plot(
    #    data_source="data/loop/electric-magnetic-energy.csv",
    #    x_column=1,
    #    y_columns=3, 
    #    x_label='Frequency (GHz)',
    #    y_label='Energy (J)',
    #    title=r'',
    #    legend_labels=[''],
    #    output_path='output/monopole_electric_energy.png',
    #    x_limits=(0, 3),
    #    #y_limits=(1e-13, 1e-10)
    #)
    #create_ieee_plot_dual_yaxis(
    #    data_source='data/dipole-moments/linear-moments.csv',
    #    x_column=0,
    #    y1_columns=1,  # Plot column 1
    #    y2_columns=2,        # Plot column 3 on right axis
    #    x_label='Frequency (GHz)',
    #    y1_label=r'Electric Dipole Moment $|m_e|\cdot 377\,\Omega$ (Vm)',
    #    y2_label='Magnetic Dipole Moment $|m_m|$ (Vm)',
    #    title='',
    #    y1_legend_labels=['$|m_e|\cdot377\,\Omega$'],
    #    y2_legend_labels=['$|m_m|$'],
    #    output_path='output/linear-dipole-moments.png',
    #    y1_limits=(0, 0.003),
    #    y2_limits=(0, 0.003),
    #    x_limits=(0.001,3)
    #)

    # Example 2: Multiple files with dual y-axis
    # create_ieee_plot_dual_yaxis_multifile(
    #     data_sources=['file1.csv', 'file2.csv'],
    #     x_columns=0,
    #     y1_columns=[(0, 1), (1, 1)],  # file1-col1, file2-col1 on left
    #     y2_columns=[(0, 2)],           # file1-col2 on right
    #     x_label='Time (s)',
    #     y1_label='Voltage (V)',
    #     y2_label='Current (A)',
    #     title='Multi-file Dual Axis Plot',
    #     y1_legend_labels=['V1', 'V2'],
    #     y2_legend_labels=['Current'],
    #     output_path='output/dual_axis_multifile.png'
    # )

    #create_ieee_plot(
    #    data_source="data/loop/feed-return-current.csv",
    #    x_column=0,
    #    y_columns=[1, 2],  
    #    x_label='Frequency (GHz)',
    #    y_label='Current (mA)',
    #    title=r'',
    #    legend_labels=['Feed current', 'Return current'],
    #    output_path='output/loop-feed-return-current.png',
    #    x_limits=(0, 3),
    #    y_limits=(0, 40)
    #)
    create_ieee_plot_multifile(
        data_sources=['data/loop/equ-moment-power.csv', 'data/loop/output-power.csv'],
        x_columns=0,  # Use column 0 as x-axis for both files
        y_columns=[1, 1],  # Plot column 1 from file1, column 1 from file2
        x_label='Frequency (GHz)',
        y_label='Power (µW)',
        title='',
        legend_labels=['Equivalent dipole moments', 'Loop antenna'],
        output_path='output/comparison-loop.png',
        y_limits=(0, 80),
        x_limits=(0.001, 3)
    )
    
    # Example 2: Multiple files - simple case
    # Plot column 1 from file1.csv and column 2 from file2.csv
    #create_ieee_plot_multifile(
    #    data_sources=['data/loop/equ-moment-power.csv', 'data/loop/magnitude.csv'],
    #    x_columns=[1, 0],  # Use column 0 as x-axis for both files
    #    y_columns=[1, 2],  # Plot column 1 from file1, column 2 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Power (W)',
    #    title='Comparison $P_\mathrm{out}$ loop antenna and $\mathbf{m}_e$, $\mathbf{m}_m$',
    #    legend_labels=['Equivalent dipole moments', 'Monopole antenna'],
    #    output_path='output/comparison-loop.png'
    #)
    
    # Example 3: Multiple files - complex case
    # Plot multiple columns from each file
    #create_ieee_plot_multifile(
        #data_sources=['data/file1.csv', 'data/file2.csv'],
        #x_columns=[0, 0],  # Column 0 for x in both files
        #y_columns=[[1, 2], [1, 3]],  # Cols 1,2 from file1; cols 1,3 from file2
        #x_label='Time (s)',
        #y_label='Amplitude',
        #title='Comprehensive comparison',
        ##legend_labels=['F1-V1', 'F1-V2', 'F2-V1', 'F2-V3'],
        #output_path='output/multifile_complex.png'
    #)
    #create_ieee_plot_multifile(
    #    data_sources=['data/gap-loop/dipole-moments-15um.csv', 'data/gap-loop/dipole-moments-500um.csv'],
    #    x_columns=0,  # Use column 0 as x-axis for both files
    #    y_columns=[[1, 2], [1, 2]],  # Plot column 1 from file1, column 1 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Dipole moments (Vm)',
    #    title='',
    #    legend_labels=[r'15 µm - $m_e$', r'15 µm - $m_m$',r'500 µm - $m_e$', r'500 µm - $m_m$'],
    #    output_path='output/gap-sweep-moments.png',
    #    y_limits=(0, 1.2e-2),
    #    x_limits=(0.001, 3)
    #)
    #create_ieee_plot_multifile(
    #    data_sources=['data/gap-loop/output-power-15um.csv', 'data/gap-loop/output-power-500um.csv'],
    #    x_columns=0,  # Use column 0 as x-axis for both files
    #    y_columns=[1, 1],  # Plot column 1 from file1, column 1 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Output power (µW)',
    #    title='',
    #    legend_labels=[r'15 µm', r'500 µm'],
    #    output_path='output/gap-sweep-power.png',
    #    y_limits=(0, 1.2e-2),
    #    x_limits=(0.001, 3)
    #)
    #create_ieee_plot(
    #    data_source="data/loop/modes-power-offset-rotated.csv",
    #    x_column=0,
    #    y_columns=[1, 2],  
    #    x_label='Frequency (GHz)',
    #    y_label='Power (W)',
    #    title=r'',
    #    legend_labels=['TEM mode', r'TE$\textsubscript{01}$ mode'],
    #    output_path='output/power-transfer-modes.png',
    #    x_limits=(0.001, 3.3),
    #    y_limits=(1e-9, 1e-2)
    #)

    #create_ieee_plot(
    #    data_source="data/loop/feed-voltage.csv",
    #    x_column=0,
    #    y_columns=1,
    #    x_label='Frequency (GHz)',
    #    y_label='Voltage (V)',
    #    title=r'',
    #    legend_labels=[''],
    #    output_path='output/loop-feed-voltage.png',
    #    x_limits=(0.001, 3),
    #    y_limits=(0, 12)
    #)
    #create_ieee_plot_multifile(
    #    data_sources=['data/loop-geometry-comp/dipole-moments-high.csv', 'data/loop-geometry-comp/dipole-moments-wide.csv'],
    #    x_columns=0,  # Use column 0 as x-axis for both files
    #    y_columns=[[1, 2], [1, 2]],  # Plot column 1 from file1, column 1 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Dipole moment magnitudes (Vm)',
    #    title='Comparison of equivalent dipole moments at different antenna geometries',
    #    legend_labels=[r'h=2.16 mm, w=1.4 mm - $m_e$', r'h=2.16 mm, w=1.4 mm - $m_m$',r'h=1.2 mm, w=2.36 mm - $m_e$', r'h=1.2 mm, w=2.36 mm - $m_m$'],
    #    output_path='output/loop-comp.png',
    #    y_limits=(0, 1.7e-2),
    #    x_limits=(0.001, 3)
    #)
    #create_ieee_plot_multifile(
    #    data_sources=['data/dipole-moments/small-tem.csv', 'data/dipole-moments/large-tem.csv'],
    #    x_columns=0,  # Use column 0 as x-axis for both files
    #    y_columns=[[1], [1]],  # Plot column 1 from file1, column 1 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Power (W)',
    #    title='',
    #    legend_labels=[r'Small TEM cell', r'Large TEM cell'],
    #    output_path='output/output-power-comp3.png',
    #    #y_limits=(0, 1.7e-2),
    #    x_limits=(0.05, 3)
    #)
    #create_ieee_plot_multifile(
    #    data_sources=['data/shielding/output-diff-sum-silver.csv'],
    #    x_columns=0,  # Use column 0 as x-axis for both files
    #    y_columns=[[1, 2]],  # Plot column 1 from file1, column 1 from file2
    #    x_label='Frequency (GHz)',
    #    y_label='Power (fW)',
    #    title='',
    #    legend_labels=[r'$P_\mathrm{load,sum}$', r'$P_\mathrm{load,diff}$'],
    #    output_path='output/silver-power.png',
    #    #y_limits=(72.5, 100),
    #    x_limits=(0.01, 3)
    #)
    create_ieee_plot_multifile(
        data_sources=["data/shielding/total.csv"],
        x_columns=0,  # Use column 0 as x-axis for both files
        y_columns=[[1, 2, 3, 4, 5, 6]],  # Plot column 1 from file1, column 1 from file2
        x_label='Frequency (GHz)',
        y_label='Power (W)',
        title='',
        legend_labels=['','','','','',''],
        output_path='output/loop-power.png',
        #y_limits=(72.5, 100),
        x_limits=(0.05, 3)
    )
    #create_ieee_plot_dual_yaxis(
    #    data_source='data/dipole-moments/ey-offset.csv',
    #    x_column=0,
    #    y1_columns=1,  # Plot column 1
    #    y2_columns=2,        # Plot column 3 on right axis
    #    x_label='Offset in $x$-direction',
    #    y1_label=r'Output power (W)',
    #    y2_label='Electric field (V/m)',
    #    title='',
    #    y1_legend_labels=['Output power'],
    #    y2_legend_labels=['$e_\mathrm{TEM,y}^\pm$'],
    #    output_path='output/ey-offset.png',
    #    #y1_limits=(0, 20),
    #    #y2_limits=(-90, -89.88)
    #    x_limits=(0, 15)
    #)
    #create_ieee_plot_dual_yaxis(
    #   data_source="data/shielding/barium-ferrite.csv",
    #    x_column=0,
    #    y1_columns=[1, 2],
    #    y2_columns=3,
    #    x_label='Freqency (GHz)',
    #    y1_label='Shielding effectiveness (dB) - ferrite and barium titanate',
    #    y2_label='Shielding effectiveness (dB) - silver',
    #    title=r'',
    #    y1_legend_labels=[r'Barium titanate', r'Ferrite'],
    #    y2_legend_labels=[r'Silver'],
    #    output_path='output/shielding-effectiveness-barium-ferrite-silver.png',
    #    x_limits=(0.05, 3),
    ##    y_limits=(0, 100)
    #)
    #create_ieee_plot_dual_yaxis_multifile(
    #    data_sources=['data/cfm/dipole-moments.csv', 'data/ifa/dipole-moments.csv'],
    #    x_columns=0,
    #    y1_columns=[(0, 1), (1, 1)],  # file1-col1, file2-col1 on left
    #    y2_columns=[(0, 2), (1, 2)],           # file1-col2 on right
    #    x_label='Frequency (GHz)',
    #    y1_label='Electric Dipole Moment $|m_e|\cdot 377\,\Omega\,(\mathrm{Vm})$',
    #    y2_label='Magnetic Dipole Moment $|m_m|$',
    #    title='',
    #    y1_legend_labels=['CFM - $|m_e|$','IFA - $|m_e|$'],
    #    y2_legend_labels=['CFM - $|m_m|$','IFA - $|m_m|$'],
    #    output_path='output/cfm-ifa-dipoles.png',
    #    y1_limits = (0, 1.7e-2),
    #    y2_limits = (0, 1.7e-2),
    #    x_limits=(0.001, 3)
    #)
    create_ieee_plot_dual_yaxis_multifile(
        data_sources=['data/monopole/dipole-moments.csv', 'data/monopole/eqc-moments.csv'],
        x_columns=0,
        y1_columns=[(0, 1), (1, 1)],  # file1-col1, file2-col1 on left
        y2_columns=[(0, 2), (1, 2)],           # file1-col2 on right
        x_label='Frequency (GHz)',
        y1_label='Electric Dipole Moment $|m_e|\cdot 377 \Omega\,(\mathrm{Vm})$',
        y2_label='Magnetic Dipole Moment $|m_m|\,(\mathrm{Vm})$',
        title='',
        y1_legend_labels=['$|m_e|$ simulation', '$|m_e|$ schematic'],
        y2_legend_labels=['$|m_m|$ simulation', '$|m_m|$ schematic'],
        output_path='output/monopole-eqc-comp.png',
        y1_limits = (-5e-5, 3.4e-2),
        y2_limits = (-5e-5, 3.4e-2),
        x_limits=(0.1, 3)
    )
    create_ieee_plot(
    data_source='data/kr_over_freq.csv',
    x_column='Frequency (GHz)',
    y_columns=['kr_large', 'kr_small'],
    x_label='Frequency (GHz)',
    y_label=r'$k \cdot r$',
    legend_labels=[r'Large TEM cell ($r = 6\,\mathrm{mm}$)',
                   r'Small TEM cell ($r = 1.5\,\mathrm{mm}$)'],
    output_path='output/kr_over_freq.png',
    figsize=(7, 3.5),
    x_limits=(0.001, 3),
    y_limits=(0, 0.45),
)
    #create_ieee_plot(
    #    data_source="data/monopole/current-dist-3GHz.csv",
    #    x_column=4,
    #    y_columns=3,
    #    x_label='Position along antenna (mm)',
    #    y_label='Current (mA)',
    #    title=r'',
    #    legend_labels=[''],
    #    output_path='output/monopole-current-dist-3GHz.png',
    #    x_limits=(0, 4.9438202247191),
    #    y_limits=(0, 40)
    #)

    # ── Feedpoint voltage & current (dual y-axis) ────────────────────────────
    _df_v = pd.read_csv('data/monopole/feed-voltage.csv')
    _df_i = pd.read_csv('data/monopole/feed-current.csv')
    _data = {
        'freq':    _df_v.iloc[:, 0].values,
        'voltage': _df_v.iloc[:, 1].values,
        'current': _df_i.iloc[:, 1].values * 1000,  # A → mA
    }
    create_ieee_plot_dual_yaxis(
        data_source=_data,
        x_column='freq',
        y1_columns='voltage',
        y2_columns='current',
        x_label='Frequency (GHz)',
        y1_label='Voltage (V)',
        title='',
        y2_label='Current (mA)',
        y1_legend_labels=['Feedpoint voltage'],
        y2_legend_labels=['Feedpoint current'],
        output_path='output/monopole_feedpoint_voltage_current.png',
        figsize=(4, 3),
        y1_limits=(0, 22),
        y2_limits=(0, 44),
        y1_color='black',
        y2_color='red',
    )
