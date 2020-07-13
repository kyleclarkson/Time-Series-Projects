import pandas as pd
import numpy as np
from datetime import datetime

# Follow along:
# https://towardsdatascience.com/basic-time-series-manipulation-with-pandas-4432afee64ea

# A list of panda's Timestamps
date_range = pd.date_range(start='1/1/2020', end='1/08/2020', freq='H')

df = pd.DataFrame(date_range, columns=['date'])
df['date'] = np.random.randint(0, 100, size=len(date_range))
print(df.head())

# Set datetime index
df['datetime'] = pd.to_datetime(df['date'])
df = df.set_index('datetime')
df.drop(['date'], axis=1, inplace=True)

print(df.head())

