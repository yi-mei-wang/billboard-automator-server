
from app import app
from clarifai.rest import ClarifaiApp
import os

app = ClarifaiApp(api_key=os.getenv('CLARIFAI_API_KEY'))


def moderate(urls):
    # Moderate content to see if it is sfw or contains tobacco
    models = [app.models.get('cigarettes'), app.models.get('moderation')]
    errors = []
    # predict with the chosen models
    for model in models:
        for index, url in enumerate(urls):
            res = {}
            response = model.predict_by_url(url=url)
            results = response['outputs'][0]['data']['concepts']
            for i, v in enumerate(results):
                if results[i]['value'] > 0.6 and results[i]['name'] not in 'safe':
                    res['index']: index
                    res['error']: results[i]['name']
                    print(res)
            errors.append(res)

    return errors
