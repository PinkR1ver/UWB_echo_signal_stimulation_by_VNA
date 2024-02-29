## Description

This project is to do analysis based on VNA S parameters data by converting the frequency domain signal to the time domain signal. 

What we do:

* range detection

## File Structure

### range_detection
```
📦 .
┣ 📂 data
┃ ┣ 📄 05.S2P
┃ ┗ 📄 ...
┣ 📂 signal
┃ ┣ 📄 5.txt
┃ ┣ 📄 MC.txt
┃ ┣ 📄 signal.xlsx
┃ ┣ 📄 t.txt
┃ ┣ 📄 train.csv
┃ ┣ 📄 t0.csv
┃ ┗...
┣ 📂 fig
┣ 📄 flight_time_get.py
┣ 📄 freq2time.py
┣ 📄 readme.md
┣ 📄 system_delay_train.py
┗ 📄 time_domain_signal_show.m
```

* data folder contains the raw data .S2P files from the VNA.
* signal folder contains the processed data, including the time domain signal, the system delay, and the frequency domain signal. **System delay is t0**
* fig folder contains the figures.
* flight_time_get.py is the script to get the flight time from the time domain signal.
* freq2time.py is the script to convert the frequency domain signal to the time domain signal.
* system_delay_train.py is the script to get the system delay by random search training.
* time_domain_signal_show.m is the script to show the time domain signal.


![all signal](./fig/all.png)