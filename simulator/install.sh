#! /bin/sh

wget https://github.com/tawnkramer/gym-donkeycar/releases/download/v22.11.06/DonkeySimLinux.zip

unzip DonkeySimLinux.zip

rm DonkeySimLinux.zip

chmod +x DonkeySimLinux/donkey_sim.x86_64
mkdir scripts/generated_data
