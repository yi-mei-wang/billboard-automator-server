from app import app
from clarifai.rest import ClarifaiApp
import os

app = ClarifaiApp(api_key=os.getev('CLARIFAI_API_KEY'))

def moderate():
    # Do content moderation by calling an API - extract to helper function
    
    # Get custom model
    # model = app.models.get('tobacco')
    # model.model_version = '5cd2c26325684e46a6f44c4c2f5cbb7f'  # This is optional. Defaults to the latest model version.

    # get the general model
    model = app.models.get("moderation")

    # predict with the model
    response = model.predict_by_url(url='https://cdn.pocket-lint.com/r/s/970x/assets/images/136967-gadgets-news-nsfw-are-naked-no-holds-barred-3d-printed-action-figures-the-next-big-thingimage1-lhsv5pxicr.jpg')

    # response = model.predict_by_url('https://cdn.vox-cdn.com/thumbor/Wm7QhA0wWlG_g3RK_O7o9_KrQ2Y=/0x0:2040x1360/1200x800/filters:focal(857x517:1183x843)/cdn.vox-cdn.com/uploads/chorus_image/image/63345165/jabareham_180614_1777_0017.0.jpg')


    # How to extract what was the problem
    results = response['outputs'][0]['data']['concepts']
    for i in range(len(results)):
        if results[i]['value'] > 0.5:
            print(results[i]['name'])

moderate()