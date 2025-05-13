import flickrapi
import pandas as pd
import time

# 替换成你自己的 Flickr API key 和 secret
api_key = '780f942b9d7f40dedec775598c956e1a'
api_secret = '22f17d70eca55123'

# 初始化 Flickr API
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# 准备数据列表
data = []

# 抓取最新上传的前 10 页，每页 200 条
for page in range(1, 11):
    print(f"正在抓取第 {page} 页...")
    try:
        photos = flickr.photos.search(
            text='Barcelona',
            has_geo=1,
            extras='geo,tags,url_s,date_taken',
            per_page=200,
            page=page,
            sort='date-posted-desc',  # 最新上传的照片
            content_type=1,
            media='photos'
        )

        for photo in photos['photos']['photo']:
            if 'latitude' in photo and 'longitude' in photo:
                data.append({
                    'title': photo.get('title', ''),
                    'tags': photo.get('tags', ''),
                    'lat': photo.get('latitude'),
                    'lon': photo.get('longitude'),
                    'url': photo.get('url_s'),
                    'date_taken': photo.get('datetaken')
                })

        time.sleep(1)  # 避免请求过快被限速

    except Exception as e:
        print(f"第 {page} 页抓取失败：{e}")
        continue

# 保存为 CSV
df = pd.DataFrame(data)
df.to_csv("flickr_barcelona_latest.csv", index=False, encoding='utf-8-sig')

print(f"✅ 共抓取 {len(df)} 条数据，已保存至 flickr_barcelona_latest.csv")
