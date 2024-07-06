date="01-Jul-2024-11-58-43"

declare -a Problems=("harmonic_oscillator")


ndrop="0"
nrefsamples="16"
nrefreplications="2"

for P in "${Problems[@]}"
do
    python simulate_criticality_measures.py $date $P $ndrop $nrefsamples $nrefreplications > output/$date/$P/simulation_terminal_output.txt
done
