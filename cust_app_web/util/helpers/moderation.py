from app import app
from clarifai.rest import ClarifaiApp
import os
import pysnooper

app = ClarifaiApp(api_key=os.getenv('CLARIFAI_API_KEY'))

@pysnooper.snoop('logggg.txt')
def moderate(url):
    # Do content moderation by calling an API - extract to helper function
    
    # Get custom model
    # model = app.models.get('tobacco')
    # model.model_version = '5cd2c26325684e46a6f44c4c2f5cbb7f'  # This is optional. Defaults to the latest model version.

    # # get the general model
    # model = app.models.get("moderation")
    models = [app.models.get('tobacco'), app.models.get('moderation')]

    # predict with the model
    for model in models:
        # response = model.predict_by_url(url=url)

        response = model.predict_by_url('https://cdn.vox-cdn.com/thumbor/Wm7QhA0wWlG_g3RK_O7o9_KrQ2Y=/0x0:2040x1360/1200x800/filters:focal(857x517:1183x843)/cdn.vox-cdn.com/uploads/chorus_image/image/63345165/jabareham_180614_1777_0017.0.jpg')
        print(response)


    # How to extract what was the problem
    results = response['outputs'][0]['data']['concepts']
    # for i in range(len(results)):
    #     if results[i]['value'] > 0.5:
    #         print(results[i]['name'], results[i]['value'])
    
    return results

moderate