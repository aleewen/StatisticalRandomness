# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Set simulation parameters
nTrials = 10000
startingValue = 100
meanParam = 0
stddevParam = 0.01



# Create a function to simulate a Gaussian Random Walk (this is without burning any simulated values)
def GaussianRandomWalk(nTrials = 10000, startingValue = 100, meanParam = 0, stddevParam = 0.01):    
    # Simulate many random binomial trials
    sim = list(np.random.normal(meanParam, stddevParam, nTrials))
    
    # Walk-forward with the results: 1 = +$1, 0 = -$1
    total = [float(startingValue)]
    
    for i in range(1, len(sim)):
        if total[i - 1] + (total[i - 1] * sim[i]) > 0:
            total.append(total[i - 1] + (total[i - 1] * sim[i]))
        else:
            total.append(total[i - 1] + (total[i - 1] * sim[i]))
            break
    
    return total



# Run the simulation
randomWalk = GaussianRandomWalk(nTrials = nTrials, startingValue = startingValue, meanParam = meanParam, stddevParam = stddevParam)



# Plot the results
fig = plt.figure()
ax = plt.axes()
fig.patch.set_facecolor('white')
plt.style.use("ggplot")

ax.plot(randomWalk, color = 'royalblue')
ax.axhline(y = startingValue, color = 'gray')
ax.set_title("Gaussian Random Walk N~(" + str(meanParam) + "," + str(stddevParam) + ")")
ax.set_xlabel("Iteration")
ax.set_ylabel("Return ($)")

fig.tight_layout()
plt.show()