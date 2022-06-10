from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class WordCloudView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def wordcloud(request):
    context = {}
    return render(request, 'polls/wordcloud.html', context)

def showwordcloud(request):
    query = request.POST['query']

    from cgitb import text
    from types import new_class
    import requests
    from bs4 import BeautifulSoup
    import json
    import re
    import sys
    import time, random
    import pandas as pd

    header = {
        'User-Agent' : 'Mozilla/5.0 (Window NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def get_news(news_url):
        news_detail = []
        req = requests.get(news_url, headers=header)
        soup = BeautifulSoup(req.content, 'html.parser')

        title = soup.select('h2.media_end_head_headline')[0].text
        news_detail.append(title)

        pdate = soup.select('.media_end_head_info_datestamp_bunch')[0].get_text()[3:14]
        news_detail.append(pdate)

        _text = soup.select('#dic_area')[0].get_text().replace('\n', " ")
        text = _text.replace("// flahs 오류를 우회하기 위함 함수 추가 function _flash_removeCallback() {}", "" )
        news_detail.append(text.strip())
        #pcompany = soup.select('#div.article_footer')[0].a.get_text().split()[0].strip()
        pcompany = soup.select('p.c_text')[0].get_text().split()[0].strip()
        news_detail.append(pcompany)

        return news_detail

    news1 = get_news('https://n.news.naver.com/mnews/article/018/0005188810?sid=101')

    columns = ['날씨', '신문사', '제목', '내용']
    df = pd.DataFrame(columns=columns)

    query = '달러'
    s_date = "2022.06.01"
    e_date = "2022.06.10"
    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1
    news_contents = ''

    while True:
        time.sleep(random.sample(range(3), 1)[0])
        print(page)

        url = "https://search.naver.com/search.naver?where=news&query=" + query + \
            "&sort=1&field=1&ds=" + s_date + "&de=" + e_date + \
            "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + \
            "%2Ca%3A&start=" + str(page)

        req = requests.get(url, headers=header)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')

        naver_news = soup.find_all("a", {"class": "info"})
        print(naver_news)

        if naver_news == []:
            break

        for a_tag in naver_news:
            try:
                news_url = a_tag.attrs["href"]
                if news_url.startswith("https://n.news.naver.com"):
                    print(news_url)
                    news_detail = get_news(news_url)
                    print(news_detail)
                    news_contents += news_detail[2]
            except Exception as e:
                print(e)
                continue
        break
        page += 10


    import pandas as pd
    import nltk
    from nltk.stem.porter import PorterStemmer
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    nltk.download('stopwords')

    import pandas as pd
    from konlpy.tag import Hannanum

    hannanum = Hannanum()

    #news3 = []
    #news3.append(hannanum.nouns(news_detail[2]))

    news3 = hannanum.nouns(news_contents)
        
    def flatten(l):
        flatList = []
        for elem in l:
            if type(elem) == list:
                for e in elem:
                    flatList.append(e)
            else:
                flatList.append(elem)
        return flatList

    word_list = flatten(news3)
    word_list = pd.Series([x for x in word_list if len(x) > 1])
    word_list.value_counts().head(10)

    from wordcloud import WordCloud
    from collections import Counter

    font_path = '/Users/taemin/Library/Fonts/AppleSDGothicNeo.ttc'

    wordcloud = WordCloud(
        font_path = font_path,
        width=800,
        height=800,
        background_color="white"
    )

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)

    array=wordcloud.to_array()

    # %matplotlib inline
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10, 10))
    plt.imshow(array, interpolation="bilinear")
    plt.show()
    plt.savefig('polls/static/polls/images/wordcloud.png')

    context = {"query": query}
    return render(request, 'polls/showwordcloud.html', context)

