echo =========================================
echo ===========================MESI==========
echo =========================================
python coherence.py mesi evict 1024 1 16
python coherence.py mesi rdafterwr 1024 1 16
python coherence.py mesi rdrdhit 1024 1 16
python coherence.py mesi rdsame 1024 1 16
python coherence.py mesi rdsameblock 1024 1 16
echo ==========================================
echo ===================Dragon=================
echo ==========================================
python coherence.py dragon evict 1024 1 16
python coherence.py dragon rdafterwr 1024 1 16
python coherence.py dragon rdrdhit 1024 1 16
python coherence.py dragon rdsame 1024 1 16
python coherence.py dragon rdsameblock 1024 1 16