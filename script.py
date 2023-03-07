import neuron
from neuron import h, rxd, gui2
# print(neuron.__version__) ==> 8.2.2
from neuron.units import ms, mV
import textwrap
import matplotlib.pyplot as plt
import csv
import plotnine as p9
import pandas as pd
import json
import pickle



soma = h.Section(name = "soma")
print(h.topology())
soma.L = 20
soma.diam = 20
print(soma.psection())

allCommands = textwrap.fill(", ".join(dir(h)))

soma.insert("hh")

print("type(soma) = {}".format(type(soma))) #section = name
print("type(soma(0.5)) = {}".format(type(soma(0.5)))) #segment = section[location]

# print(type(soma).var)   this is how variables of a section are addressed
# print(type(soma).var_mech)    mechanisms of variable
mech = soma(0.5).hh
print(dir(mech))
print(mech.gkbar)
print(soma(0.5).hh.gkbar)

iclamp = h.IClamp(soma(0.5))   #an IClamp is a point source of current (for membrane dynamics), we specify the segment to which it'll bind
iclampAttrs = [item for item in dir(iclamp) if not item.startswith("__")]

iclamp.delay = 2
iclamp.dur = 0.1
iclamp.amp = 0.9

# print(soma.psection())

#set up recording variables, they will be configured for a simulation
v = h.Vector().record(soma(0.5)._ref_v)  # Membrane potential vector
t = h.Vector().record(h._ref_t)  # Time stamp vector

#running a simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)   #each cell has a resting potential of 65 mV
h.continuerun(40 * ms)

# plt.figure()
# plt.plot(t, v)
# plt.xlabel("t (ms)")
# plt.ylabel("v (mV)")
# # plt.show()

#reading and writing csv files
with open("data.csv", "w") as f:
    csv.writer(f).writerows(zip(t, v))

with open("data.csv") as f:
    reader = csv.reader(f)
    tnew, vnew = zip(*[[float(val) for val in row] for row in reader if row])


data = pd.read_csv("data.csv", header=None, names=["t", "v"])

#reading and writing json
with open("data.json", "w") as f:
    json.dump({"t": list(t), "v": list(v)}, f, indent=4)

with open("data.json") as f:
    data = json.load(f)
tnew = data["t"]
vnew = data["v"]


#reading and writing pickle files
with open("data.p", "wb") as f:
    pickle.dump({"t": t, "v": v}, f)

with open("data.p", "rb") as f:
    data = pickle.load(f)
tnewp = data["t"]
vnewp = data["v"]
