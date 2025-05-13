import pandas as pd
import folium
from folium.plugins import BeautifyIcon

# 读取数据
df = pd.read_csv("flickr_barcelona_cleaned.csv")
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

# 创建地图（黑白灰底图）
m = folium.Map(location=[41.3851, 2.1734], zoom_start=13, tiles='CartoDB Positron')

# 添加 marker
for _, row in df.iterrows():
    if pd.notnull(row['lat']) and pd.notnull(row['lon']) and pd.notnull(row['url']):
        popup_html = f"""
        <b>{str(row['title'])[:30]}</b><br>
        <img src="{row['url']}" width="150"><br>
        <i>{str(row['tags'])[:50]}</i><br>
        {row['date_taken']}
        """
        popup = folium.Popup(folium.IFrame(popup_html, width=170, height=200), max_width=200)

        # 使用更小的红色圆形图钉
        icon = BeautifyIcon(
            icon_shape='marker',
            border_color='red',
            border_width=1,
            text_color='white',
            background_color='red',
            icon_size=[18, 18]
        )

        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup,
            icon=icon
        ).add_to(m)

# 保存地图
m.save("barcelona_photo_map_red.html")
print("✅ 地图已保存为 barcelona_photo_map_red.html")
