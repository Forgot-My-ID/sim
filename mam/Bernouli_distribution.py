from scipy.stats import bernoulli
import seaborn as sb
import matplotlib.pyplot as plt

data_bern = bernoulli.rvs(size=1000, p=0.6)
ax = sb.histplot(data_bern, kde=True, color='crimson', bins=2)
ax.set(xlabel='Bernoulli', ylabel='Frequency')
plt.show()
