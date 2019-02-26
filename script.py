# %matplotlib inline

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import KaplanMeierFitter

draft_df = pd.read_csv("main-big-2017-s-clean.csv")
# set some plotting aesthetics, similar to ggplot

sns.set(palette = "colorblind", font_scale = 1.35,
        rc = {"figure.figsize": (12,9), "axes.facecolor": ".92"})
# keplar object
kmf = KaplanMeierFitter()
kmf.fit(durations = draft_df.duration, event_observed = draft_df.retired)
print("Event Table:")
print(kmf.event_table)



# get the values for time = 0 from the survival table
event_at_0 = kmf.event_table.iloc[0, :]
# now calculate the survival probability for t = 0
surv_for_0 =  (event_at_0.at_risk - event_at_0.observed) / event_at_0.at_risk

# Calculate the survival probability for t = 1
event_at_1 = kmf.event_table.iloc[1, :]
surv_for_1 =  (event_at_1.at_risk - event_at_1.observed) / event_at_1.at_risk
print("Calculate the survival probability for t = 1")
print(surv_for_1)


# Calculate the survival probability for t = 2
event_at_2 = kmf.event_table.iloc[2, :]
surv_for_2 =  (event_at_2.at_risk - event_at_2.observed) / event_at_2.at_risk
print("Calculate the survival probability for t = 2")
print(surv_for_2)


# The probability that an NFL player has a career longer than 2 years
surv_after_2 = surv_for_0 * surv_for_1 * surv_for_2
print("The probability that an NFL player has a career longer than 2 years")
print(surv_after_2)

# pridict for t=1,3,5,10
# print(kmf.predict([1,3,5,10]))

# surival function
print("surival function:")
print(kmf.survival_function_)

# median
print(kmf.median_)

# plot the KM estimate
kmf.plot()
# Add title and y-axis label
plt.title("The Kaplan-Meier Estimate for Drafted NFL Players\n(2007-2017)")
plt.ylabel("Probability a Player is Still Active")
plt.show()