# [Jovanka Broz](https://en.wikipedia.org/wiki/Jovanka_Broz)

Discord bot representing brotherhood and unity.

## Dependencies

* [Opus Interactive Audio Codec](https://opus-codec.org/)
* [FFmpeg](https://ffmpeg.org/)

Detailed documentation and installation instructions can be found on their respective web
pages, but for quick start you can use:

* `brew install opus ffmpeg` on OS X
* `apt-get install -y libopus0 ffmpeg` on Debian based systems

## Deploying

You can easily deploy this bot to Heroku by flowing these steps:

1. Make sure you have Heroku account, and Heroku CLI installed.
*You can find Heroku CLI installation instructions  [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)*
2. Open your terminal and log in your Heroku CLI by running `heroku login`
3. Navigate into the project directory
4. Create Heroku application by running `heroku create`
5. Login into Container Registry with `heroku container:login`
6. Set Discord Bot token as environment variable `heroku config:set JB_DISC_TOKEN="your token"`
7. Set Battle.net token as environment variable `heroku config:set JB_BNET_TOKEN="your token"`
8. Push your container with `heroku container:push worker`
9. And then release it with `heroku container:release worker`
10. Start worker dyno by running `heroku ps:scale worker=1`
11. Enjoy!

