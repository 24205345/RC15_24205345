import pandas as pd
from collections import Counter

# 读取 CSV 文件
df = pd.read_csv("flickr_barcelona_cleaned.csv")
tags = ' '.join(df['tags'].dropna().astype(str)).split()
tags = [tag.lower() for tag in tags if len(tag) >= 4]

# 自定义停用词
stopwords = {
    'sony', 'canon', 'nikon', 'ilce7cm2', 'ilce7', 'iphone12promax', 'iphone16pro', 'iphone',
    'e28200mmf2856a071', 'lens', 'format', 'mm', 'mmf', 'focalength', 'focallength', 'metadata', 'exif', 'pixar',
    'iso400', 'iso1000', 'iso2000', 'iso3200', 'iso6400', 'iso8000', 'iso1600', 'iso2500', 'iso5000', 'iso1250',
    'bruxelles', 'belgique', 'belgium', 'bxl', 'bru', 'spain', 'europa', 'europe', 'espana', 'spagna', 'españa',
    'barcelona', 'catalonia', 'catalunya',
    'promax', 'file', 'data', 'photo', 'photobook', 'imagen', 'snapshot', 'shot', 'pics',
    'springbreak2025', '2025springbreakmediterraneancruise', '2025springbreak', 'mediterraneancruise',
    'android', 'mobile', 'network', 'connect', 'upload', 'flickr',
    'eventoconstruccion', 'evento', 'networking', 'executiveforum', 'executive', 'directivos',
    'font', 'example', 'flor', 'color', 'reflection', 'daylight',
    'municipio', 'infraestructurasmunicipals', 'infraestructuras', 'construccionesrubau', 'construccion', 'rubau',
    'cesarchivadeagustin', 'cesarchiva', 'miguelmartipujol', 'ricardfont'
}

# 清洗标签
filtered = [t for t in tags if t not in stopwords]
top_tags = Counter(filtered).most_common(30)

# HTML tag 块
html_tags = '\n'.join(
    f'<a class="tag" href="https://www.flickr.com/search/?text={tag}" target="_blank">{tag}</a>'
    for tag, _ in top_tags
)

# HTML 文件结构
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Barcelona Tag WordCloud</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #fff;
      text-align: center;
    }}
    h2 {{
      margin-top: 30px;
      color: #444;
    }}
    #taglist {{
      margin-top: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
    }}
    .tag {{
      font-size: 18px;
      padding: 6px 12px;
      background: #f5f5f5;
      border-radius: 6px;
      color: #333;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .tag:hover {{
      background: crimson;
      color: white;
    }}
    img {{
      margin-top: 40px;
      max-width: 90%;
      border: 2px solid #ccc;
    }}
  </style>
</head>
<body>

  <h2>📸 Explore Top Tags from Barcelona Flickr Photos</h2>

  <div id="taglist">
    {html_tags}
  </div>

  <img src="barcelona_tag_wordcloud.png" alt="WordCloud Image">

</body>
</html>
"""

# 保存 HTML 文件
with open("interactive_wordcloud.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML 文件已生成：interactive_wordcloud.html")
