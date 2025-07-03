import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
# Note: The code below is a numerical simulation of heat diffusion in a rod.
# todo: modify function so that it DiffInput contains a list of timesteps to plot the results. For those timesteps, we should call plt.plot() to plot the temperature distribution.

@dataclass
class DiffInput:
    jmax: int
    nmax: int
    alpha: float
    s: float
    timax: float
    timesteps: list[float] = None  # Optional list of timesteps to plot


def DIFF(input: DiffInput):
    # TODO: Modify this function to return a dictionary with results for the specified timesteps
    results = {time_step: None for time_step in input.timesteps}
    """
    Numerical simulation using only the dimensional temperature array (TD).
    """
    jmax = input.jmax
    alpha = input.alpha
    s = input.s
    timax = input.timax

    dx = 1.0 / float(jmax - 1)  # spatial step size
    dt = dx * dx * s / alpha

    print(f"Calculated dx={dx}, dt={dt}")

    TD = np.zeros(jmax)  # dimensional temperature
    DUM = np.zeros(jmax)  # dummy array for calculations

    current_time = 0.0

    # Set initial boundary conditions
    TD[0] = 50.0  # 100 * 0.5
    TD[jmax - 1] = 50.0

    print(f"Initial boundary conditions set: TD[0]={TD[0]}, TD[{jmax-1}]={TD[jmax-1]}")

    # Main simulation loop
    while current_time < timax:
        if current_time > 0.0:
            TD[0] = 100.0  # 100 * 1.0
            TD[jmax - 1] = 100.0
        else:
            TD[0] = 50.0  # 100 * 0.5
            TD[jmax - 1] = 50.0

        # Update TD in-place using a copy to avoid overwriting values needed for computation
        TD_old = TD.copy()
        for j in range(1, jmax - 1):
            TD[j] = (1.0 - 2.0 * s) * TD_old[j] + s * (TD_old[j - 1] + TD_old[j + 1])
        # Optional: Plot the temperature distribution at specified timesteps
        print (f"At time {current_time:.2f}s {input.timesteps}")
        for time_step in input.timesteps:
            if np.abs(time_step - current_time) < 1e-5:
                results[time_step] = TD.copy().tolist()  # Store the temperature distribution at this timestep
        current_time += dt

    return results


if __name__ == "__main__":
    # Example usage
    diff_input = DiffInput(jmax=11, nmax=10, alpha=0.1e-4, s=0.5, timax=3500.0, timesteps=[0.0, 1500.0, 3000.0])
    DIFF(diff_input)
