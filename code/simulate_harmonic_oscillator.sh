date=$(date '+%d-%b-%Y-%H-%M-%S')
problem="harmonic_oscillator"

mkdir -p output/$date/$problem

python simulate_nominal_problem.py $date $problem > output/$date/$problem/simulation_terminal_output.txt
python simulate_reference_problem.py $date $problem >> output/$date/$problem/simulation_terminal_output.txt
python simulate_saa_problem.py $date $problem >> output/$date/$problem/simulation_terminal_output.txt
python simulate_criticality_measures.py $date $problem
python plot_rates.py $date $date
