date=$(date '+%d-%b-%Y-%H-%M-%S')

P="harmonic_oscillator"
mkdir -p output/$date/$P
python simulate_saa_problem.py $date $P > output/$date/$P/simulation_terminal_output.txt
