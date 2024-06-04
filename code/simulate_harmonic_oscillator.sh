date=$(date '+%d-%b-%Y-%H-%M-%S')

P="harmonic_oscillator"
mkdir -p output/$P/$date
python simulation.py $date $P > output/$P/$date/simulation_terminal_output.txt
