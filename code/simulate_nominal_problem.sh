date=$(date '+%d-%b-%Y-%H-%M-%S')
declare -a Problems=("harmonic_oscillator" "cubic_oscillator" "vaccination_scheduling")

for P in "${Problems[@]}"
do
    mkdir -p output/$date/$P
    python simulate_nominal_problem.py $date $P > output/$date/$P/simulation_terminal_output.txt
done
