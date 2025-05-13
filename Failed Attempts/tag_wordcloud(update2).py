import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import matplotlib.font_manager as fm

# 加载数据
df = pd.read_csv("flickr_barcelona_cleaned.csv")

# 合并所有标签
tags = ' '.join(df['tags'].dropna().astype(str))
words = tags.split()

# 自定义停用词（扩展版）
custom_stopwords = {
    # 相机设备类
    'sony', 'canon', 'nikon', 'ilce7cm2', 'ilce7', 'iphone12promax', 'iphone16pro', 'iphone',
    'e28200mmf2856a071', 'lens', 'format', 'mm', 'mmf', 'focalength', 'focallength', 'metadata', 'exif', 'pixar',
    # 摄影参数类
    'iso400', 'iso1000', 'iso2000', 'iso3200', 'iso6400', 'iso8000', 'iso1600', 'iso2500', 'iso5000', 'iso1250',
    # 与地点无关的关键词（地理噪音）
    'bruxelles', 'belgique', 'belgium', 'bxl', 'bru', 'spain', 'europa', 'europe', 'espana', 'spagna', 'españa',
    # 多余的词缀或语言干扰
    'promax', 'file', 'data', 'photo', 'photobook', 'imagen', 'snapshot', 'shot', 'pics',
    # 无效或模板化词
    'springbreak2025', '2025springbreakmediterraneancruise', '2025springbreak', 'mediterraneancruise',
    'android', 'mobile', 'network', 'connect', 'upload', 'flickr',
    # 平台行为词
    'eventoconstruccion', 'evento', 'networking', 'executiveforum', 'executive', 'directivos',
    # 通用视觉形容词
    'light', 'shadow', 'color', 'colors', 'flor', 'blossom', 'reflection', 'daylight', 'outdoor',
    # 杂项（企业、工程词）
    'municipio', 'infraestructurasmunicipals', 'infraestructuras', 'construccionesrubau', 'construccion', 'rubau',
    'cesarchivadeagustin', 'cesarchiva', 'miguelmartipujol', 'ricardfont'
}

# 清洗词汇
filtered = [
    w.lower() for w in words
    if len(w) >= 4 and
       not re.match(r'^\d+$', w) and
       all(stop not in w.lower() for stop in custom_stopwords)
]
cleaned_text = ' '.join(filtered)

# 设置字体路径（跨平台兼容）
font_path = fm.findfont(fm.FontProperties(family='DejaVu Sans'))

# 创建词云
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    max_words=200,
    collocations=False,
    colormap='cool',
    font_path=font_path
).generate(cleaned_text)

# 绘图保存
plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig("barcelona_tag_wordcloud_cleaned_final.png", dpi=300)
plt.show()

print("✅ 词云已清洗并保存为 barcelona_tag_wordcloud_cleaned_final.png")
