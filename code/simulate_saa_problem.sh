date=$(date '+%d-%b-%Y-%H-%M-%S')
declare -a Problems=("harmonic_oscillator" "cubic_oscillator" "vaccination_scheduling")

declare -a Problems=("harmonic_oscillator")

nrefsamples="4"
lbrange="2"
ubrange="4"

for P in "${Problems[@]}"
do
    mkdir -p output/$date/$P
    python simulate_saa_problem.py $date $P $nrefsamples $lbrange $ubrange > output/$date/$P/simulation_terminal_output.txt
done
