import glob
import os
import requests
import xml.etree.ElementTree as ET

publications = glob.glob('_publications/*.md')

for pub in publications:
    os.remove(pub)

xml_content = requests.get('https://research.vu.nl/en/persons/pz-vroon/publications/?format=rss').content
root = ET.fromstring(xml_content)

for child in root[0][4:]:
    title = child[0].text
    link = child[1].text
    description = child[2].text
    date = child[5].text[:10]

    end_idx = description.find('<p class="type">')
    description = description[:end_idx]
    description = description.replace('In :', 'In:')
    print(title, link, date)

    with open(f'_publications/{date}-paper-title-number-1.md', 'w') as f:
        f.write(
f"""---
title: "{title}"
collection: publications
permalink: /publication/paper-{date}
excerpt: ''
date: {date}
venue: ''
paperurl: '{link}'
citation: ''
---

{description}
""")


