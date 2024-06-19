date="19-Jun-2024-18-05-52"

declare -a Problems=("harmonic_oscillator" "cubic_oscillator")

for P in "${Problems[@]}"
do
    python simulate_criticality_measures.py $date $P > output/$date/$P/simulation_terminal_output.txt
done
