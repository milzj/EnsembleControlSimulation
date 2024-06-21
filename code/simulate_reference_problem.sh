date=$(date '+%d-%b-%Y-%H-%M-%S')
declare -a Problems=("harmonic_oscillator" "cubic_oscillator" "vaccination_scheduling")
declare -a Problems=("vaccination_scheduling")

nrefsamples="16"

for P in "${Problems[@]}"
do
    mkdir -p output/$date/$P
    python simulate_reference_problem.py $date $P $nrefsamples > output/$date/$P/simulation_terminal_output.txt
done
