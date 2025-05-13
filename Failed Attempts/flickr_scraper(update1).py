import flickrapi
import pandas as pd

# 你的 Flickr API Key 和 Secret
api_key = '780f942b9d7f40dedec775598c956e1a'
api_secret = '22f17d70eca55123'

# 初始化 API
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

all_data = []

# 分页抓取前 5 页，每页 200 张（最多抓 1000 张）
for page in range(1, 6):
    print(f"📦 正在抓取第 {page} 页...")
    photos = flickr.photos.search(
        text='Barcelona',
        has_geo=1,
        extras='geo,tags,url_s,date_taken',
        per_page=200,
        page=page,
        sort='relevance',
        min_taken_date='2020-01-01',  # 限定为2020年以后的图片
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

# 转换成 DataFrame 保存
df = pd.DataFrame(all_data)
df.to_csv("flickr_barcelona_real.csv", index=False)
print(f"✅ 抓取完成，共获取 {len(df)} 条图像数据")
