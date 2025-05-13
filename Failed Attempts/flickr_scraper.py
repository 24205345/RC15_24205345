import flickrapi
import pandas as pd

# 你的 Flickr API 凭证
api_key = '780f942b9d7f40dedec775598c956e1a'
api_secret = '22f17d70eca55123'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# 抓取巴塞罗那图像
photos = flickr.photos.search(
    text='Barcelona',
    has_geo=1,
    extras='geo,tags,url_s,date_taken',
    per_page=200,
    page=1,
    sort='relevance',
    content_type=1,
    media='photos'
)

data = []
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

df = pd.DataFrame(data)
df.to_csv("flickr_barcelona_real.csv", index=False)

print("✔️ 抓取完成，已保存到 flickr_barcelona_real.csv")
