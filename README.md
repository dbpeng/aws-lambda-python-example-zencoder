# About the project
This project uses AWS API gateway, lambda, s3, [serverless](serverless.com), [zencoder](https://app.zencoder.com), [flywaydb](https://flywaydb.org) to build an example how to successfully deploy a python based lambda project into AWS lambda environment. Using virtualenv is highly recommended to try this project.

# Setup guide
## flyway
At the project root running the following commmands, be sure you have created the flyway.conf at project root.
```
#> flyway init
#> flyway migrate
```
## serverless
Before using `serverless deploy` you have to write the variable files stored in `/serverless`. There are 3 example files, replace the values with your environment setups and remove `-example` in the filename. Here's the example of deployment command
```
#> serverless deploy --stage dev --profile <your profile> 
```

# Send a job request
```
curl -X "POST" "https://{DOMAIN_NAME_AND_PATH}/transcoders/zencoder/" \
     -H 'Content-Type: application/json' \
     -d $'{
  "src": "https://wowza-video.escapex.com/hk3345678-2.mp4",
  "profile": "zen-hls"
}'
```