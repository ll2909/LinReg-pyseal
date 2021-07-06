# LinReg-pyseal
Linear Regression using Microsoft SEAL Homomorphic Encription API.

Based on satssehgal's project, showed on https://youtu.be/nlsd2LO-S50
, his repo: https://github.com/satssehgal/Homomorphic-Encryption

I kept the same client/server architecture and the same methods for the
linear regression model training (sklearn.linear_model) as shown in the video, I just changed
the encryption backend, using pySEAL (https://github.com/Lab41/PySEAL), a port of
Microsoft SEAL API, natively written in C++ (https://github.com/microsoft/SEAL).

To test the program, run the script client.py

