from django.test import TestCase


# def check_comma(str, comma_threshold=1, interval_threshold=15):
#     counter = 0
#     index = 0
#     distance_counter = 0
#     interval = 0
#     for i in str:
#         if counter < comma_threshold:
#             if i == ",":
#                 counter += 1
#                 interval = distance_counter
#             elif i == ".":
#                 counter = 0
#                 interval = 0
#                 distance_counter = 0
#             else:
#                 distance_counter += 1
#         else:
#             if interval > interval_threshold:
#                 new_str = str[:index - 1] + "." + str[index:]
#                 str = new_str
#                 interval = 0
#                 counter=0
#                 distance_counter=0
#         index += 1
#     return str
#
#
# text = "The service is good,but the coop fee is too high,the life in coop work term is as fun as the life in study term, it is too difficult to find a job!"
# print(check_comma(text))

# import requests
# data= "{ \"paragraph\":\"The service is very good!\"}"
# url = 'http://localhost:8000/sentiment/'
# headers = {'content-type': 'application/json'}
# r = requests.post(url, data=data, headers=headers)
# print(r.content)
# r.close()

from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
sentence="I have told the coop office that the interviews should be in a private room but unfortunately they did not pay any attention to me."
score = analyzer.polarity_scores(sentence)
print(score)

