set web hook
```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebHook?url=https://<NGROK_URL/"
```

check web hook
```bash
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
> How install ngrok


tutorial
https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/

