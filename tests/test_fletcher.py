import unittest
from fletcher import DiffInput, DiffusionSolver, DIFF


class TestDiffusionSolver(unittest.TestCase):
    def test_initial_conditions(self):
        params = DiffInput(
            num_gridpoints=5,
            alpha=0.1e-4,
            s=0.5,
            max_time=10.0,
            output_timesteps=[0.0],
        )
        solver = DiffusionSolver(params)
        self.assertEqual(solver.T[0], 50.0)
        self.assertEqual(solver.T[-1], 50.0)

    def test_step(self):
        params = DiffInput(
            num_gridpoints=5,
            alpha=0.1e-4,
            s=0.5,
            max_time=10.0,
            output_timesteps=[0.0],
        )
        solver = DiffusionSolver(params)
        solver._apply_boundary_conditions()
        solver.step()
        self.assertEqual(len(solver.T), params.num_gridpoints)

    def test_diff_output(self):
        diff_input = DiffInput(
            num_gridpoints=11,
            alpha=0.1e-4,
            s=0.5,
            max_time=3500.0,
            output_timesteps=[0.0, 1500.0, 3000.0],
        )
        results = DIFF(diff_input)
        print(f"Results: {results}")
        # Check that results is a dict with the right keys
        self.assertIsInstance(results, dict)
        for t in diff_input.output_timesteps:
            self.assertIn(t, results)
            self.assertIsInstance(results[t], list)
            self.assertEqual(len(results[t]), diff_input.num_gridpoints)


if __name__ == "__main__":
    unittest.main()
