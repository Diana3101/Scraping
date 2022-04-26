import codecs
import json
import os

json_file = "rgru_articles.json"
json_data = []

os.mkdir("sas_ready_txt_rgru")
with open(json_file) as json_fileopen:
    json_data = json.load(json_fileopen)


def process_text(title, text):
    # text_list = text.split(".")
    # text_list = text_list[1:]
    # text = ".".join([sent for sent in text_list])
    title = " ".join([sent for sent in title])
    title_list = title.split(' — ')
    title = title_list[0]
    text = text.replace("'", "")
    text = text.replace("\xa0", ' ')
    text = text.strip()

    return title + "\n\n" + text


for article in json_data:
    article_text = process_text(article['article_title'], article['article_text'])
    article_uuid = article['article_uuid']
    with codecs.open("sas_ready_txt_rgru/" + article_uuid + ".txt", "w", "utf-8-sig") as temp:
        temp.write(article_text)
