# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Set simulation parameters
nTrials = 10000
probSuccess = 0.5
successPayout = 1
failurePayout = -1



# Create a function to simulate a Binomial Martingale
def BinomialMartingale(nTrials = 10000, probSuccess = 0.5, successPayout = 1, failurePayout = -1):    
    # Simulate many random binomial trials
    sim = list(np.random.binomial(1, probSuccess, nTrials))
    
    # Walk-forward with the results: 1 = +$1, 0 = -$1
    total = list()
    
    for i in range(0, len(sim)):
        # Handle the first iteration (cannot use previous value as it does not exist for the first iteration)
        if sim[i] == 1 and i == 0:
            total.append(successPayout)
        elif sim[i] == 0 and i == 0:
            total.append(failurePayout)
        
        # Walk-forward with all other results
        if sim[i] == 1 and i != 0:
            total.append(total[i - 1] + successPayout)
        elif sim[i] == 0 and i != 0:
            total.append(total[i - 1] + failurePayout)
    
    return total



# Run the simulation
coinFlip = BinomialMartingale(nTrials = nTrials, probSuccess = probSuccess, successPayout = successPayout, failurePayout = failurePayout)



# Plot the results
fig = plt.figure()
ax = plt.axes()
fig.patch.set_facecolor('white')
plt.style.use("ggplot")

ax.plot(coinFlip, color = 'royalblue')
ax.axhline(y = 0, color = 'gray')
ax.set_title("Coin Flip Game")
ax.set_xlabel("Iteration")
ax.set_ylabel("Return ($)")

fig.tight_layout()
plt.show()


