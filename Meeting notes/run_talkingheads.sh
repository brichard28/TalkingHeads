#!/bin/bash
# run_talkingheads.sh
# LES testing bash script with Maanasa [07/07/2023]
# not working currently (need to fix the way to make it properly executable)
conda activate TalkingHeads-env
cd /d D:\Experiments\TalkingHeads
python stimgen_TalkingHeads.py
D:\Experiments\TalkingHeads\TalkingHeads-venv\Scripts\activate.bat
cd D:\Experiments\TalkingHeads\GUI code
python exp_TalkingHeads.py