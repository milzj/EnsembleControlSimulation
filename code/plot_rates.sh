
P="cubic_oscillator"
P="harmonic_oscillator"
P="vaccination_scheduling"
ref_date="19-Jun-2024-20-37-51"
ref_date="27-Jun-2024-14-52-51"
ref_date="23-Jun-2024-08-20-28"
ref_date="30-Jun-2024-15-13-15"
ref_date="05-Jul-2024-14-10-24"
ref_date="04-Jul-2024-18-12-46"
saa_date=$ref_date
ndrop="3"
nrefreplications="1"
python plot_rates.py $ref_date $saa_date $P $ndrop $nrefreplications
