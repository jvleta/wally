import numpy as np
from dataclasses import dataclass

@dataclass
class DiffInput:
    jmax: int
    nmax: int
    alpha: float
    s: float
    timax: float
    timesteps: list[float]

class DiffusionSolver:
    def __init__(self, params: DiffInput):
        self.params = params
        self.dx = 1.0 / (params.jmax - 1)
        self.dt = self.dx * self.dx * params.s / params.alpha
        self.TD = np.zeros(params.jmax)
        self.current_time = 0.0
        self._set_initial_conditions()

    def _set_initial_conditions(self):
        self.TD[0] = 50.0
        self.TD[self.params.jmax - 1] = 50.0

    def _apply_boundary_conditions(self):
        if self.current_time > 0.0:
            self.TD[0] = 100.0
            self.TD[self.params.jmax - 1] = 100.0
        else:
            self.TD[0] = 50.0
            self.TD[self.params.jmax - 1] = 50.0

    def step(self):
        TD_old = self.TD.copy()
        for j in range(1, self.params.jmax - 1):
            self.TD[j] = (
                (1.0 - 2.0 * self.params.s) * TD_old[j]
                + self.params.s * (TD_old[j - 1] + TD_old[j + 1])
            )

    def run(self):
        results = {t: None for t in self.params.timesteps}
        while self.current_time < self.params.timax:
            self._apply_boundary_conditions()
            self.step()
            for t in self.params.timesteps:
                if np.abs(t - self.current_time) < 1e-5:
                    results[t] = self.TD.copy().tolist()
            self.current_time += self.dt
        return results

def DIFF(input: DiffInput):
    solver = DiffusionSolver(input)
    return solver.run()
