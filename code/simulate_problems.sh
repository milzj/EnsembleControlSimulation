date=$(date '+%d-%b-%Y-%H-%M-%S')

declare -a Problems=("harmonic_oscillator" "cubic_oscillator")
declare -a Problems=("vaccination_scheduling" "harmonic_oscillator")


nrefsamples=$[2**12]
nreplications="50"
nrefreplications="1"
lbrange="6"
ubrange="10+1"
ndrop="0"

nrefsamples=$[2**3]
nreplications="2"
nrefreplications="1"
lbrange="1"
ubrange="2"
ndrop="0"

for problem in "${Problems[@]}"
do
    mkdir -p output/$date/$problem

    python simulate_nominal_problem.py $date $problem > output/$date/$problem/simulation_terminal_output.txt
    python simulate_reference_problem.py $date $problem $nrefsamples $nrefreplications >> output/$date/$problem/simulation_terminal_output.txt
    python simulate_saa_problem.py $date $problem $nreplications $lbrange $ubrange >> output/$date/$problem/simulation_terminal_output.txt
    python simulate_criticality_measures.py $date $problem $nrefsamples $nrefreplications
    python plot_rates.py $date $date $problem $ndrop $nrefreplications

done
