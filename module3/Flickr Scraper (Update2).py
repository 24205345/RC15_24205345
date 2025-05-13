import flickrapi
import pandas as pd

api_key = '780f942b9d7f40dedec775598c956e1a'
api_secret = '22f17d70eca55123'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

all_data = []

# 抓取最新上传的前1000张图片（每页200张，共5页）
for page in range(1, 6):
    print(f"📦 正在抓取第 {page} 页（最新）...")
    photos = flickr.photos.search(
        text='Barcelona',
        has_geo=1,
        extras='geo,tags,url_s,date_taken',
        per_page=200,
        page=page,
        sort='date-posted-desc',     # 👈 关键修改点：抓取“最新发布”的图像
        content_type=1,
        media='photos'
    )

    for photo in photos['photos']['photo']:
        if 'latitude' in photo and 'longitude' in photo:
            all_data.append({
                'title': photo.get('title', ''),
                'tags': photo.get('tags', ''),
                'lat': photo.get('latitude'),
                'lon': photo.get('longitude'),
                'url': photo.get('url_s'),
                'date_taken': photo.get('datetaken')
            })

df = pd.DataFrame(all_data)
df.to_csv("flickr_barcelona_real.csv", index=False)
print(f"✅ 抓取完成，共获取 {len(df)} 条图像数据")
