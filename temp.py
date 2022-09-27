import pandas as pd
df=pd.read_excel(r"sample.xlsx",index_col=False)
Sum=df.sum()
print(Sum)



