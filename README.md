# SAMOTA-lib: An Extensible Framework for Surrogate-Assisted Many Objective Testing Approach for ADS Testing

This project presents SAMOTA-lib, a Python library that implements all the key algorithms and models of SAMOTA, a novel approach designed for Test Suite generation for ADS testing.
This repositary contains the implementation and license to use SAMOTA-lib.

## Requirements

- Software requirements:

  Python version: 3.9+

  Packages: see requirements.txt, or simply run the commands in the Install section to install the packages you need

- Hardware recommendations:

  OS: Windows 10 64-Bit
  
  CPU: AMD Ryzen 7 1700 3.0Ghz / Intel Core i7-6700 3.4Ghz (or better)
  
  RAM: 32 GB RAM
  
  GPU: AMD R9 290 / Nvidia GeForce GTX 970
  
  DirectX: Version 11
  
  Storage: 50 GB available space

Note: these are the hardware recommendataions copied from (https://documentation.beamng.com/support/troubleshooting/requirements/#:~:text=Recommended%20Requirements%201%20OS%3A%20Windows%2010%2064-Bit%202,mods%20will%20increase%20required%20storage%20space.%20Gamepad%20recommended.) for the BeamNG application, which also applies for the BeamNG.tech simulator used within this library.

In my personal experience I used my Ryzen 5 with integrated graphics, 16GB RAM, and Windows 10 and it works fine. Therefore, it should work on the majority of somewhat recent hardware.

## Install

1. First, to clone the repo run: git clone https://github.com/SashaSaw/SAMOTA-Lib.git

2. Then, open the cloned library: cd place/where/you/cloned/the/repository

3. pip install virtualenv (if you don't already have virtualenv installed)

4. virtualenv <name of env> (to create your new environment)

5. source <name of env>/bin/activate (to enter the environement)

6. pip install -r requirements.txt

That should be it. You're ready to use the library!

## How to Run

To run the an example implementation of the library simpy run the command 'python main.py' in the terminal.

## How to Test

To run the existing unit test cases you should be able to simply run the command 'python test.py' in the terminal.

## Authors

Alexander Saw, sawsasha26@gmail.com

## License

MIT License (see https://github.com/SashaSaw/SAMOTA-Lib/blob/main/LICENSE for more details)
