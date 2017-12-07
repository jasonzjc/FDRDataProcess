# FDRDataProcess
Functions for FDR data process

`ConvNumAmend.py` Amend the Converion Number (ConvNum) when FDR working in the mode with data rate over 100 Hz. In this case, the index will lose the hundredths digital. E.g., 101 will become 1. This code amend the ConvNum and generate a new data file with a suffix of 'conv_' in its file name.
