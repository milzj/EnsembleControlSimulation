date=$(date '+%d-%b-%Y-%H-%M-%S')

declare -a Problems=("harmonic_oscillator" "cubic_oscillator")
declare -a Problems=("vaccination_scheduling")

nrefsamples=$[2**6]
nreplications="20"
lbrange="2"
ubrange="5"

for problem in "${Problems[@]}"
do
    mkdir -p output/$date/$problem

    python simulate_nominal_problem.py $date $problem > output/$date/$problem/simulation_terminal_output.txt
    python simulate_reference_problem.py $date $problem $nrefsamples >> output/$date/$problem/simulation_terminal_output.txt
    python simulate_saa_problem.py $date $problem $nreplications $lbrange $ubrange >> output/$date/$problem/simulation_terminal_output.txt
    python simulate_criticality_measures.py $date $problem $nrefsamples
    python plot_rates.py $date $date $problem
done
