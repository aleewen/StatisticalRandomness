# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev, median
pd.options.display.float_format = '{:20,.2f}'.format
# pd.reset_option('display.float_format')



# Set simulation parameters
nTrials = 500
startingValue = 100000
probSuccess = 0.5
successMultiplier = 1.2
pctRisk = 2

iterations = 10000



# Create a function to simulate a Gaussian Random Walk (this is without burning any simulated values)
def TradingSimulation(nTrials = 500, startingValue = 100000, probSuccess = 0.5, successMultiplier = 1.2, pctRisk = 2):    
    # Simulate many random binomial trials
    sim = list(np.random.binomial(1, probSuccess, nTrials))
    
    # Walk-forward with the results: 1 = +$1, 0 = -$1
    total = list([startingValue])
    
    for i in range(1, len(sim)):
        if sim[i] == 1:
            total.append(total[i - 1] + (total[i - 1] * (successMultiplier * pctRisk / 100)))
        elif sim[i] == 0 and (total[i - 1] - (total[i - 1] * pctRisk / 100)) > 0:
            total.append(total[i - 1] - (total[i - 1] * pctRisk / 100))
        else:
            total.append(0.0)
            break
    
    return total



# Create a function to simuate many random walks in a Monte Carlo-like manner and save results as variance increases
def MonteCarlo(iterations = 10000, nTrials = 500, startingValue = 100000, probSuccess = 0.5, successMultiplier = 1.2, pctRisk = 2):
    # Create a dataframe to store the organized data
    results = pd.DataFrame({'Risk per Trade': [], 'Mean Terminal Value': [], 'Median Terminal Value': [], 'StdDev of Terminal Values': [], 'Coeff of Variation': [],
                            'Highest Terminal Value': [], 'Lowest Terminal Value': [], 'Pct Terminal Values < 25%': [], 'Pct Bankruptcies': []})
    
    # Loop through different stdDev parameters
    for i in range(pctRisk, (pctRisk * 20) + pctRisk, pctRisk):
        # Create a list to store terminal values
        terminalValues = list()
        
        # Simulate the trading strategy
        for j in range(0, iterations):
            iterationTemp = TradingSimulation(nTrials = nTrials, startingValue = startingValue, probSuccess = probSuccess, successMultiplier = successMultiplier, pctRisk = i)
            terminalValues.append(iterationTemp[len(iterationTemp) - 1])
        
        results = pd.concat([results, pd.DataFrame(
                {'Risk per Trade': [i],
                 'Mean Terminal Value': [mean(terminalValues)],
                 'Median Terminal Value': [median(terminalValues)],
                 'StdDev of Terminal Values': [np.std(terminalValues, ddof = 1)],
                 'Coeff of Variation': [np.std(terminalValues, ddof = 1) / mean(terminalValues)],
                 'Highest Terminal Value': [max(terminalValues)],
                 'Lowest Terminal Value': [min(terminalValues)],
                 'Pct Terminal Values < 25%': [len([x for x in terminalValues if x < startingValue * 0.25])*100 / len(terminalValues)],
                 'Pct Bankruptcies': [len([x for x in terminalValues if x <= 0.0001])*100 / len(terminalValues)]
                 })])
    
    return results



# Run the simulation
monteCarlo = MonteCarlo()



# Print the Results
print(monteCarlo)



# Plot the results
fig = plt.figure()
ax = plt.axes()
fig.patch.set_facecolor('white')
plt.style.use("ggplot")

ax.plot(monteCarlo['Risk per Trade'], monteCarlo['Pct Bankruptcies'], color = 'royalblue')
ax.set_title(r"Bankrupt Accounts by Risk % per Trade")
ax.set_xlabel("Risk % per Trade")
ax.set_ylabel("% Bankrupt Accounts")

fig.tight_layout()
plt.show()


