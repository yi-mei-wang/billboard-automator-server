from app import app
from clarifai.rest import ClarifaiApp
import os
import pysnooper

app = ClarifaiApp(api_key=os.getenv('CLARIFAI_API_KEY'))

def moderate(url):
    # Moderate content to see if it is sfw or contains tobacco
    
    models = [app.models.get('tobacco'), app.models.get('moderation')]

    # predict with the model
    for model in models:
        response = model.predict_by_url(url=url)

        results = response['outputs'][0]['data']['concepts']


    # How to extract what was the problem
    
    # for i in range(len(results)):
    #     if results[i]['value'] > 0.5:
    #         print(results[i]['name'], results[i]['value'])
    
    return results
