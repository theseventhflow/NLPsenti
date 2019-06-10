from sentiment_api.sentiment import language_detect,text_preprocess,check_comma,sentiment_analysis
from sentiment_api.models import SentimentClass


class TestLanguage:
    def test_en_detect(self):
        text = "The service is good,but the coop fee is too high,the life in coop work term is as fun as the life in study term, it is too difficult to find a job!"
        language = language_detect(text)
        assert language=="en"

    def test_fr_detect(self):
        text = "Les ateliers offerts en personne ne sont pas tous très pertinents."
        language = language_detect(text)
        assert language=="fr"


class TestModel:
    def test_add_model(self):
        model = SentimentClass(title="comment1",code="abc")
        assert model.title == "comment1"
        assert model.code == "abc"


class TestSentiment:
    def test_preprocess(self):
        text = "... There are only 2 work terms! ; etc."
        text = text_preprocess(text)
        assert "..." not in text
        assert ";" not in text

    def test_comma(self):
        text = "The service, price and number of positions are all very good!"
        str = check_comma(text)
        assert "," in str

    def test_sentiment(self):
        text = "The service, price and number of positions could be better!"
        dict =  sentiment_analysis(text)
        assert dict[text] == "SUGGESTION"

        text1 = "The service, price and number of positions are very good!"
        dict1 = sentiment_analysis(text1)
        assert "POSITIVE" in dict1[text1]