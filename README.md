set web hook
```sh
curl "https://api.telegram.org/bot<TOKEN>/setWebHook?url=https://<NGROK_URL/"
```

check web hook
```sh
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

## Contribuiting

### Virtual ENV
> To easily work on this project locally, we suggest to use a python virtual environment:

```sh
python -m venv ./teammate-env
cd teammate-env
source ./bin/activate
git clone <PROJECT>
```

## Local testing
> For local testing we suggest to use ngrok. You can easily install it following the [official documentation](https://ngrok.com/download)

> Start ngrok tunneling
```sh
ngrok http 8080
```

> Set telegram webhook uding the https url provided by ngrok
```sh
curl "https://api.telegram.org/bot<TOKEN>/setWebHook?url=https://<NGROK_URL/"
```

> Run local python server server
```
python source/bot.py
```

> Query the bot and enjoy!



tutorial
https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/
