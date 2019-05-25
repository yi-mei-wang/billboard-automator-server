# from app import app
# from clarifai.rest import ClarifaiApp
# import os

# app = ClarifaiApp(api_key=os.getenv('CLARIFAI_API_KEY'))

# def moderate(urls):
#     # Moderate content to see if it is sfw or contains tobacco
#     models = [app.models.get('tobacco'), app.models.get('moderation')]

#     errors = []
#     # predict with the chosen models
#     for model in models:
#         for url in urls:
#             response = model.predict_by_url(url=url)

#             results = response['outputs'][0]['data']['concepts']

#             for i in range(len(results)):
#                 if results[i]['value'] > 0.6:
#                     if results[i]['name'] != 'safe':
#                         res = {}
#                         res['pict'] = url
#                         res[results[i]['name']]= results[i]['value']
#                         errors.append(res)
#     return errors

# moderate("https://www.google.com/search?q=synthwave&safe=active&rlz=1C1CHZL_esPE747PE747&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiT-taShLHiAhX26nMBHc1rCpgQ_AUIDigB&biw=1536&bih=750#imgrc=yzmcDtYmDKuMuM:")