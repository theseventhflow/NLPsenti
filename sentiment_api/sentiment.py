from nltk.tokenize import sent_tokenize
from langdetect import detect
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()

suggestion_en=["I was also hoping", "would", "could", "advice", "advise", "perhaps", "maybe", "may be"
            ,"may","might","how about","why not","what if","could always","I thought","should"]
suggestion_fr=["Peut-être", "Possiblement", "Pourrait", "J’aimerais", "Ce serait bien que", "Pourquoi pas"
            ,"Je pense que","Serait-il possible","J’aimerais que","Pourriez-vous","Pouvez-vous"]
neg_fr = ["ne comprends pas","extrêmement impoli"]
def keyword_match(keyword, sentence):
    m = re.search(keyword,sentence,re.IGNORECASE)
    return bool(m)

# keyword = "Would be"
# sentence = "More positions could be better!"
# print(keyword_match(keyword,sentence))

# change some punctuation marks
def text_preprocess(text):
    # text = text.replace("...", ". ")
    text = text.replace(".", ". ")
    text = text.replace("!", "! ")
    text = text.replace(";",". ")
    text = text.replace("1)",". ")
    text = text.replace("2)",". ")
    # text = text.replace("etc.","etc")
    return text



# detect whether it is English or French
def language_detect(text):
    text_part = text[:40]
    language = detect(text_part)
    return language


# separate some sentences which contain commas, but ignore the very short phrases
def check_comma(str, comma_threshold=1, interval_threshold=15):
    counter = 0
    index = 0
    distance_counter = 0
    interval = 0
    for i in str:
        if counter < comma_threshold:
            if i == ",":
                counter += 1
                interval = distance_counter
                distance_counter=0
            elif i == "."or i=="!":
                counter = 0
                interval = 0
                distance_counter = 0
            else:
                distance_counter += 1
        else:
            if interval > interval_threshold:
                new_str = str[:index - 1] + "." + str[index:]
                str = new_str
            interval = 0
            counter = 0
            distance_counter = 0
        index += 1
    return str


# comma checking and punctuation filtering
# language detecting
# Then use different nip libraries
# English library can return result with a dictionary with 4 keys: positive, negative, neutral and the total score
# total score has the range [-1,1]
# French library can return result with a tuple. the left one is sentiment and the second one is subjectivity.
# Subjectivity can show us whether a sentence is an opinion or just an explanation or a story
# sentiment [-1,1], subjectivity [0,1]
def sentiment_analysis(text, comma_threshold=1, interval_threshold=15):
    result={}
    text = check_comma(text, comma_threshold, interval_threshold)
    text = text_preprocess(text)
    is_suggestion=False
    is_negative = False
    try:
        language = language_detect(text)
        if language == "en":
            sentences = sent_tokenize(text)
            analyzer = SentimentIntensityAnalyzer()
            for sentence in sentences:
                for keyword in suggestion_en:
                    is_suggestion = keyword_match(keyword,sentence)
                    is_suggestion = False
                    if is_suggestion:
                        result[sentence]="SUGGESTION"
                        break
                if not is_suggestion:
                    score = analyzer.polarity_scores(sentence)
                    if (score['neg']>0.09 and score["compound"]<0.1) or score["compound"]<-0.3:
                        result[sentence] = "NEGATIVE,             neg: %s, pos: %s, neu: %s, compound: %s"%(score["neg"] ,score["pos"],score["neu"],score["compound"])
                    elif score["compound"] > 0.3 and score['pos']>0.17:
                        result[sentence] = "POSITIVE,             neg: %s, pos: %s, neu: %s, compound: %s"%(score["neg"] ,score["pos"],score["neu"],score["compound"])
                    else:
                        result[sentence] = "NEUTRAL,              neg: %s, pos: %s, neu: %s, compound: %s"%(score["neg"] ,score["pos"],score["neu"],score["compound"])
            return result
        if language == "fr":
            sentences = sent_tokenize(text,language="french")
            analyzer = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
            for sentence in sentences:
                for keyword in suggestion_fr:
                    is_suggestion = keyword_match(keyword,sentence)
                    if is_suggestion:
                        result[sentence] = "SUGGESTION"
                        break
                for keyword in neg_fr:
                    is_negative = keyword_match(keyword,sentence)
                    if is_negative:
                        result[sentence] = "NEGATIVE"
                        break
                if not is_suggestion and not is_negative:
                    score = analyzer(sentence).sentiment
                    if (score[0] < 0 and score[1]>0) or (score[0]<0.1 and score[1]>0.25):
                        result[sentence] = "NEGATIVE              sentiment: %s, subjectivity %s"%(score[0],score[1])
                    elif score[0] > 0.2:
                        result[sentence] = "POSITIVE              sentiment: %s, subjectivity %s"%(score[0],score[1])
                    else:
                        result[sentence] = "NEUTRAL               sentiment: %s, subjectivity %s"%(score[0],score[1])
            return result
    except:
        result["Message"] = "MEANINGLESS"
        return result

# text = " J'aurais aimé être mieux accompagnée au vu des problématiques qui auraient pu être engendrées j’aimerais."
# print(sentiment_analysis(text))


