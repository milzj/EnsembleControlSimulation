date=$(date '+%d-%b-%Y-%H-%M-%S')
declare -a Problems=("harmonic_oscillator" "cubic_oscillator")

for P in "${Problems[@]}"
do
    mkdir -p output/$date/$P
    python simulate_saa_problem.py $date $P > output/$date/$P/simulation_terminal_output.txt
done
