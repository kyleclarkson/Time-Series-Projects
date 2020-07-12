import pandas as pd
import numpy as np
from datetime import datetime

# A list of panda's Timestamps
date_range = pd.date_range(start='1/1/2020', end='1/08/2020', freq='H')

print(date_range[0])

df = pd.DataFrame(date_range, columns=['date'])

df['date'] = np.random.randint(0, 100, size=len(date_range))

print(df.head(15))