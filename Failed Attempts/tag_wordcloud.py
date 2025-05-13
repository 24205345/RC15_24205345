import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv("flickr_barcelona_real.csv")
all_tags = ' '.join(df['tags'].dropna().astype(str))

# 提高分辨率：设置更大的图像尺寸 + 字体细节
wordcloud = WordCloud(
    width=1600,      # 原来是800
    height=800,      # 原来是400
    background_color='white',
    collocations=False,
    max_words=200
).generate(all_tags)

# 输出更高清晰度的图像
plt.figure(figsize=(16, 8))  # 原来是 (10, 5)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig("barcelona_tag_wordcloud_hd.png", dpi=300)  # 300 DPI 保证打印级别
plt.show()

print("✅ 高清词云已保存为 barcelona_tag_wordcloud_hd.png")
