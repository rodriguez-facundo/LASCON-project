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

# Connectivity

<img width="610" alt="Screenshot 2019-05-11 at 9 10 03 AM" src="https://user-images.githubusercontent.com/32278395/57569547-d1afe900-73cc-11e9-8045-6e942968b1dc.png">

# Rasters

<img width="753" alt="Screenshot 2019-05-11 at 9 08 01 AM" src="https://user-images.githubusercontent.com/32278395/57569548-d4aad980-73cc-11e9-8c5b-8223c6fdfebe.png">

<img width="767" alt="Screenshot 2019-05-11 at 9 08 19 AM" src="https://user-images.githubusercontent.com/32278395/57569549-d83e6080-73cc-11e9-8bb9-e5fad8f62131.png">

<img width="755" alt="Screenshot 2019-05-11 at 9 09 04 AM" src="https://user-images.githubusercontent.com/32278395/57569551-dbd1e780-73cc-11e9-987b-15ef295c8b0f.png">

# NetPyNE-UI network viewer

<img width="838" alt="Screenshot 2019-05-11 at 9 10 32 AM" src="https://user-images.githubusercontent.com/32278395/57569544-ceb4f880-73cc-11e9-9e04-2e0ec6b5b0c2.png">

<img width="452" alt="Screenshot 2019-05-11 at 9 11 00 AM" src="https://user-images.githubusercontent.com/32278395/57569533-c2c93680-73cc-11e9-9300-467ef6bc4b70.png">

<img width="665" alt="Screenshot 2019-05-11 at 9 10 52 AM" src="https://user-images.githubusercontent.com/32278395/57569537-c6f55400-73cc-11e9-9e2b-ca6995d9d1a7.png">

<img width="445" alt="Screenshot 2019-05-11 at 9 10 43 AM" src="https://user-images.githubusercontent.com/32278395/57569540-c9f04480-73cc-11e9-8ebb-a35397f6da65.png">
