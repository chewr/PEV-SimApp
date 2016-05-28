import cPickle as pickle
import server
import numpy as np
import matplotlib.pyplot as plt

env200 = pickle.load(open("env-hubway_sim_all-fs-200.pkl", "rb"))
env300 = pickle.load(open("env-hubway_sim_all-fs-300.pkl", "rb"))
env400 = pickle.load(open("env-hubway_sim_all-fs-400.pkl", "rb"))

t_wait_200 = []
t_wait_300 = []
t_wait_400 = []

for trip in env200.trips:
	t_wait_200.append(trip.getWait() / 60.0)

for trip in env300.trips:
	t_wait_300.append(trip.getWait() / 60.0)

for trip in env400.trips:
	t_wait_400.append(trip.getWait() / 60.0)

# t_wait_300 = np.random.randn(1000)
# t_wait_400 = np.random.randn(1000)

n_bins = 10
print "300:", len(t_wait_300), "400:", len(t_wait_400)
lt5_2 = [x for x in t_wait_200 if x <= 5.0]
lt5_3 = [x for x in t_wait_300 if x <= 5.0]
lt5_4 = [x for x in t_wait_400 if x <= 5.0]
print "Less than 5 min: 200:", len(lt5_2),"300:", len(lt5_3),"400:", len(lt5_4)
label = ["200-PEV fleet", "300-PEV fleet", "400-PEV fleet"]
plt.hist([t_wait_200, t_wait_300, t_wait_400], n_bins, histtype='bar', stacked=False, label = label)
plt.legend(prop={'size': 10})
plt.title('Wait times over hubway rides')
plt.xlabel("Wait time, minutes")
plt.ylabel("Number of trips")
plt.savefig("waits_histo.png")
plt.show()
