# About the project
This is a transcoder project that can transcode a video from s3 or http server. It uses Zencoder as the transcoding service. And save the result in HLS format then store in S3.

# What you need
By using this project you need:
1. AWS account for running Lambda, SNS, API gateway and S3
2. Zencoder account
3. Maria DB, MySQL or AWS Aurora

# Setup guide
## flyway
At the project root (be sure you have created the flyway.conf at root)
```
#> flyway init
#> flyway migrate
```
## serverless
There are several steps to initial the serverless project:
1.
2.
3.
## aws


# Send a job request
```
curl -X "POST" "https://{DOMAIN_NAME_AND_PATH}/transcoders/zencoder/" \
     -H 'Content-Type: application/json' \
     -d $'{
  "src": "https://wowza-video.escapex.com/hk3345678-2.mp4",
  "profile": "zen-hls"
}'
```