import pandas as pd

# 读取数据
df = pd.read_csv("flickr_barcelona_latest.csv")

# 数据清洗：只保留在巴塞罗那城市范围内的照片
df_cleaned = df[
    (df['lat'] >= 41.3) & (df['lat'] <= 41.45) &
    (df['lon'] >= 2.1) & (df['lon'] <= 2.23)
]

# 保存清洗后的数据
df_cleaned.to_csv("flickr_barcelona_cleaned.csv", index=False)
