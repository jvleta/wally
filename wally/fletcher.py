import numpy as np
from dataclasses import dataclass


@dataclass
class DiffInput:
    num_gridpoints: int
    alpha: float
    s: float
    max_time: float
    output_timesteps: list[float]


class DiffusionSolver:
    def __init__(self, params: DiffInput):
        self.params = params
        self.dx = 1.0 / (params.num_gridpoints - 1)
        self.dt = self.dx * self.dx * params.s / params.alpha
        self.T = np.zeros(params.num_gridpoints)
        self.current_time = 0.0
        self._set_initial_conditions()

    def _set_initial_conditions(self):
        self.T[0] = 50.0
        self.T[self.params.num_gridpoints - 1] = 50.0

    def _apply_boundary_conditions(self):
        if self.current_time > 0.0:
            self.T[0] = 100.0
            self.T[self.params.num_gridpoints - 1] = 100.0
        else:
            self.T[0] = 50.0
            self.T[self.params.num_gridpoints - 1] = 50.0

    def step(self):
        T_old = self.T.copy()
        self._apply_boundary_conditions()
        for j in range(1, self.params.num_gridpoints - 1):
            self.T[j] = (1.0 - 2.0 * self.params.s) * T_old[j] + self.params.s * (
                T_old[j - 1] + T_old[j + 1]
            )

    def run(self):
        results = {t: None for t in self.params.output_timesteps}
        while self.current_time < self.params.max_time:
            self.step()
            for t in self.params.output_timesteps:
                print(t, self.current_time, np.abs(t - self.current_time))
                if np.abs(t - self.current_time) < 10:
                    results[t] = self.T.copy().tolist()
            self.current_time += self.dt
        return results


def DIFF(input: DiffInput):
    solver = DiffusionSolver(input)
    return solver.run()
