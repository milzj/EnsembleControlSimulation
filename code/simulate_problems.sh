date=$(date '+%d-%b-%Y-%H-%M-%S')

declare -a Problems=("vaccination_scheduling" "harmonic_oscillator")

nrefsamples=$[2**12]
nreplications="50"
nrefreplications="1"
lbrange="6"
ubrange="11"
ndrop="0"

time {
for problem in "${Problems[@]}"
do
    mkdir -p output/$date/$problem

    time python simulate_nominal_problem.py $date $problem > output/$date/$problem/simulation_terminal_output.txt
    time python simulate_reference_problem.py $date $problem $nrefsamples $nrefreplications >> output/$date/$problem/simulation_terminal_output.txt
    time python simulate_saa_problem.py $date $problem $nreplications $lbrange $ubrange >> output/$date/$problem/simulation_terminal_output.txt
    time python simulate_criticality_measures.py $date $problem $nrefsamples $nrefreplications
    time python plot_rates.py $date $date $problem $ndrop $nrefreplications

done
}
