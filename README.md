This is a netpyne implementation of the Dentite Gyrus model

There are 3 files avaiable from which Granule cell morpologies are picked up:

- morpho/100A0Y.dat (only mature cells)
- morpho/50A50Y.dat (mature & young)
- morpho/50A50P.dat (mature & PILO treated)

to select one of those, go to **init.py** line 169

You can also control the sprouting level with the **diver** matrix in line 196 in **init.py**.  (last row, last colum)

**run it: "nrniv -python init.py"**

the calcium activated Potassium channel does not work outside 6.3 degrees unless you set q10 = 1 and compile mod files again.

you should get results similar to the ones below:

![screenshot from 2018-02-01 17-27-42](https://user-images.githubusercontent.com/32278395/35865801-a2c28f5c-0b3c-11e8-8611-b45ffb391bc4.png)
![screenshot from 2018-02-06 12-34-06](https://user-images.githubusercontent.com/32278395/35865802-a30f434c-0b3c-11e8-8980-7b5d8760cb7a.png)
