date=$(date '+%d-%b-%Y-%H-%M-%S')
declare -a Problems=("harmonic_oscillator" "cubic_oscillator" "vaccination_scheduling")
declare -a Problems=("vaccination_scheduling")
declare -a Problems=("harmonic_oscillator")

nrefsamples="16"
nreplications="4"
nrefreplications="2"

for P in "${Problems[@]}"
do
    mkdir -p output/$date/$P
    python simulate_reference_problem.py $date $P $nrefsamples $nreplications $nrefrepliations > output/$date/$P/simulation_terminal_output.txt
done
