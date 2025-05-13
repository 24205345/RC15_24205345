import pandas as pd
import folium

# 读取数据
df = pd.read_csv("flickr_barcelona_real.csv")

# 创建 Folium 地图（中心定位在巴塞罗那）
m = folium.Map(location=[41.3851, 2.1734], zoom_start=13)

# 添加图像 Marker
for _, row in df.iterrows():
    if pd.notnull(row['lat']) and pd.notnull(row['lon']):
        popup_html = f"""
        <b>{row['title']}</b><br>
        <img src="{row['url']}" width="150"><br>
        <i>{row['tags']}</i><br>
        {row['date_taken']}
        """
        popup = folium.Popup(folium.IFrame(popup_html, width=170, height=200), max_width=200)
        folium.Marker(
            location=[float(row['lat']), float(row['lon'])],
            popup=popup,
            icon=folium.Icon(color='blue', icon='camera', prefix='fa')
        ).add_to(m)

# 保存地图
m.save("barcelona_photo_map.html")
print("✅ 地图已生成为 barcelona_photo_map.html")
