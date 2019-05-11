### This is a netpyne implementation of the Dentite Gyrus model

#### Requirements:
    - Python3
    - Neuron 7.6.2
    - NetPyNE

#### Run:
    - `git clone https://github.com/rodriguez-facundo/LASCON-project.git`
    - `cd LASCON-project`
    - `nrnivmodl mod`
    - `nrniv -python init.py`

To change network composition, choose a different file from **init.py** line 169:

- morpho/100A0Y.dat (only mature cells)
- morpho/50A50Y.dat (mature & young)
- morpho/50A50P.dat (mature & PILO treated)

You can also control the sprouting level from the **diver** matrix at line 196 (**init.py**).  (last row, last colum)



NOTES: 
    - The calcium activated Potassium channel does not work outside 6.3 degrees unless you set q10 = 1 and recompile mod files.
    - Templates n5, n111, n112 present disconected sections. You can choose other templates instead.

Some results playing with the model:

