import os
import pickle
from plot_state_control import plot_state_control
from harmonic_oscillator.harmonic_oscillator import HarmonicOscillator

# Set up paths
sub_dir = os.path.join(os.path.dirname(__file__), "output", "06-Jul-2024-14-14-20", "harmonic_oscillator", "reference_problem")
pickle_file = os.path.join(sub_dir, "harmonic_oscillator_solutions_rep_0_06-Jul-2024-14-14-20.pickle")

# This will result in the correct output filenames:
# controls_reference_harmonic_oscillator_rep_0_06-Jul-2024-14-14-20.pdf
# states_reference_harmonic_oscillator_rep_0_06-Jul-2024-14-14-20.pdf
filename = "reference_harmonic_oscillator_rep_0_06-Jul-2024-14-14-20"

if os.path.exists(pickle_file):
    print(f"Loading {pickle_file}")
    with open(pickle_file, "rb") as f:
        w_opt = pickle.load(f)
    problem = HarmonicOscillator()
    plot_state_control(problem, w_opt, outdir=sub_dir, filename=filename, nsamples=2**12)
    print(f"Overwrote controls_{filename}.pdf and states_{filename}.pdf")
else:
    print(f"Pickle file not found: {pickle_file}")
