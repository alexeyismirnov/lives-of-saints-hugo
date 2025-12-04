#!/usr/bin/env python
import sys
import re
import os
import pprint as p
from pathlib import Path
import json

def date_translate(date_string, lang):
    if lang != "ru":
        return date_string

    months = {
        'January': 'января', 'February': 'февраля', 'March': 'марта',
        'April': 'апреля', 'May': 'мая', 'June': 'июня',
        'July': 'июля', 'August': 'августа', 'September': 'сентября',
        'October': 'октября', 'November': 'ноября', 'December': 'декабря'
    }

    day, month = date_string.split()
    return f"{day} {months[month]}"


if len(sys.argv) != 3:
    print("Usage: %s filename.json month" % sys.argv[0])
    sys.exit(0)

month =  sys.argv[2]
lang = 'ru'

Path("output/%s" % month).mkdir(parents=True, exist_ok=True)

chapterTemplate = """+++
title = "{0}"
type = "chapter"
+++

{{{{% children description="true" sort="weight" showhidden="true" %}}}}
""".format(month)

#with open("output/%s/_index.md" % month, "w+") as f:
#    f.writelines(chapterTemplate)

with open(sys.argv[1]) as f:
    arr = [p for p in json.load(f) if month in p['date']]

    for s in arr:
        day = int(s['date'].split()[0])
        title = s['saint']
        filename = "%s.md" % s['reading']

        pageTemplate = """+++
draft = false
hidden = true
linkTitle = '{0}'
description = '{1}'
weight = {2}
+++

{{{{% include file="content/{3}/lives/{4}" %}}}}
""".format(title, date_translate(s['date'], lang), day, lang, filename)

        with open("output/%s/%s" % (month, filename), "w+") as f:
            f.writelines(pageTemplate)

    # print(arr)
