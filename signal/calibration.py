import numpy as np
import pandas as pd
from scipy.optimize import minimize

def rotation_matrix_x(theta):
    """
    Generate a 3D rotation matrix for rotation about the x-axis.

    Parameters:
        theta (float): Angle in radians for rotation around the x-axis.

    Returns:
        np.ndarray: 3x3 rotation matrix for x-axis rotation.
    """
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])

def rotation_matrix_y(phi):
    """
    Generate a 3D rotation matrix for rotation about the y-axis.

    Parameters:
        phi (float): Angle in radians for rotation around the y-axis.

    Returns:
        np.ndarray: 3x3 rotation matrix for y-axis rotation.
    """
    return np.array([[np.cos(phi), 0, np.sin(phi)],
                     [0, 1, 0],
                     [-np.sin(phi), 0, np.cos(phi)]])

def rotation_matrix_z(psi):
    """
    Generate a 3D rotation matrix for rotation about the z-axis.

    Parameters:
        psi (float): Angle in radians for rotation around the z-axis.

    Returns:
        np.ndarray: 3x3 rotation matrix for z-axis rotation.
    """
    return np.array([[np.cos(psi), -np.sin(psi), 0],
                     [np.sin(psi), np.cos(psi), 0],
                     [0, 0, 1]])

def rotate_data(df, theta, phi, psi):
    """
    Apply a 3D rotation to a dataset based on specified angles.

    Parameters:
        df (pd.DataFrame): DataFrame with columns 'x', 'y', 'z' representing 3D points.
        theta (float): Angle in radians for rotation around the x-axis.
        phi (float): Angle in radians for rotation around the y-axis.
        psi (float): Angle in radians for rotation around the z-axis.

    Returns:
        np.ndarray: Rotated 3D data as a NumPy array.
    """
    rotation_matrix = rotation_matrix_x(theta) @ rotation_matrix_y(phi) @ rotation_matrix_z(psi)
    rotated_data = df[['x', 'y', 'z']].values @ rotation_matrix.T
    return rotated_data

def objective_function(angles, df):
    """
    Objective function to optimize during calibration. The function minimizes
    the sum of the y-coordinates of the rotated data.

    Parameters:
        angles (list): List of three angles [theta, phi, psi] in radians.
        df (pd.DataFrame): DataFrame with columns 'x', 'y', 'z' representing 3D points.

    Returns:
        float: The sum of the y-coordinates of the rotated data.
    """
    theta, phi, psi = angles
    rotated_data = rotate_data(df, theta, phi, psi)
    rotated_df = pd.DataFrame(rotated_data, columns=['x', 'y', 'z'])
    return rotated_df['y'].sum()

def calibrate(df, verbose=False):
    """
    Calibrate the orientation of 3D data by optimizing rotation angles to
    minimize the sum of y-coordinates.

    Parameters:
        df (pd.DataFrame): DataFrame with columns 'x', 'y', 'z' representing 3D points.
        verbose (bool): If True, print detailed output during the process.

    Returns:
        tuple: Rotated DataFrame with adjusted 3D coordinates and Numpy Array of optimal angles [theta, phi, psi].
    """
    initial_angles = [0, 0, 0]

    result = minimize(objective_function, initial_angles, args=(df,), bounds=[(-np.pi, np.pi)]*3)

    optimal_angles = result.x
    if verbose:
        print(f"Optimal angles (theta, phi, psi): {optimal_angles}")

    rotated_data = rotate_data(df, *optimal_angles)
    rotated_df = pd.DataFrame(rotated_data, columns=['x', 'y', 'z'])

    if verbose:
        print(rotated_df.head())

    return rotated_df, optimal_angles
