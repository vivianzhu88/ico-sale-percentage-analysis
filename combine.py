import pandas as pd

df1 = pd.read_csv('coins_info.txt')
df2 = pd.read_csv('btc_eth_rois.txt')

pd.concat([df1, df2], axis=1).to_csv('combined.txt', index=False, na_rep='N/A')




