import glob
import os
import requests
import xml.etree.ElementTree as ET

publications_dir = '_publications'
rss_url = 'https://research.vu.nl/en/persons/pz-vroon/publications/?format=rss'

if not os.path.exists(publications_dir):
    os.makedirs(publications_dir)

publications = glob.glob(f'{publications_dir}/*.md')

for pub in publications:
    os.remove(pub)

xml_content = requests.get(rss_url).content
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

    with open(f'_publications/paper-{date}.md', 'w') as f:
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


