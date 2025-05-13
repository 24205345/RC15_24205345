import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import random

# 加载数据
df = pd.read_csv("flickr_barcelona_cleaned.csv")

# 合并所有标签
tags = ' '.join(df['tags'].dropna().astype(str))
words = tags.split()

custom_stopwords = {
    # 相机设备类
    'sony', 'canon', 'nikon', 'ilce7cm2', 'ilce7', 'iphone12promax', 'iphone16pro', 'iphone', 'iphone365',
    'canoneosrp', 'canoneosr', 'canoneosrp100', 'canonrp', 'canoneos100', 'mm', 'mmf', 'lens', 'format',
    'e28200mmf2856a071', 'focalength', 'focallength', 'metadata', 'exif', 'pixar',

    # 摄影参数类
    'iso100', 'iso200', 'iso400', 'iso640', 'iso800', 'iso1000', 'iso1250', 'iso1600',
    'iso2000', 'iso2500', 'iso3200', 'iso4000', 'iso5000', 'iso8000',

    # 与地点无关的关键词（地理噪音）
    'bruxelles', 'belgique', 'belgium', 'bxl', 'bru', 'spain', 'espana', 'españa', 'spagna', 'europa', 'europe',

    # 巴塞罗那/加泰罗尼亚地区名（现在排除）
    'barcelona', 'barcelonad', 'barcelonacity', 'barcelonagram', 'barcelonagramers',
    'catalonia', 'catalunya', 'cataluña', 'cataloniaespanya', 'katalonien',

    # 多余的语言碎片/平台行为
    'example', 'file', 'data', 'photo', 'photobook', 'imagen', 'snapshot', 'shot', 'pics',
    'eventoconstruccion', 'evento', 'network', 'networking', 'executiveforum', 'executive', 'directivos', 'connect', 'upload', 'flickr',
    'contactgroups', 'groupes', 'filmisnotdead', 'android', 'mobile',

    # 杂项标识与冗余模板（大量集中重复）
    'springbreak2025', '2025springbreak', 'mediterraneancruise', '2025springbreakmediterraneancruise',
    '2026springbreakmediterraneancruise', 'spring2026', '2026springbreak',

    # 通用视觉属性
    'light', 'shadow', 'color', 'colors', 'flor', 'blossom', 'reflection', 'daylight', 'outdoor',

    # 建筑项目/开发公司等
    'municipio', 'infraestructurasmunicipals', 'infraestructuras', 'construccionesrubau', 'construccion', 'rubau',
    'cesarchivadeagustin', 'cesarchiva', 'miguelmartipujol', 'ricardfont', 'poblesespanyol', 'macrosius',

    # 特殊词合并补充
    'architectureexample', 'parcgràcia', 'macrosius'
}

filtered_words = [
    w.lower() for w in words
    if len(w) >= 4 and
       not re.match(r'^\d+$', w) and
       not w.lower() in custom_stopwords
]

# 合并为清洗后的字符串
cleaned_text = ' '.join(filtered_words)

# ✅ 不再高亮关键词
highlight_words = set()

# 修改颜色函数为纯黑白灰
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    gray = random.randint(60, 180)
    return f"rgb({gray}, {gray}, {gray})"

# 创建词云
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    max_words=200,
    collocations=False
).generate(cleaned_text)

# 应用颜色方案
wordcloud = wordcloud.recolor(color_func=custom_color_func)

# 绘图并保存
plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig("barcelona_tag_wordcloud.png", dpi=300)
plt.show()

print("✅ 黑白灰 + 红点风格词云已生成并保存为 barcelona_tag_wordcloud.png")
