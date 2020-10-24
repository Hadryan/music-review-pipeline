#!/usr/bin/env python

import rymscraper as rym
import pandas as pd

# create connection
network = rym.RymNetwork()

# get charts as source for artists
rym_url = rym.RymUrl.RymUrl()
chart_infos = network.get_chart_infos(rym_url=rym_url, max_page=3)
df = pd.DataFrame(chart_infos)



# get list of albums for artists

# get album details

# close & quit browser to avoid memory leaks
network.browser.close()
network.browser.quit()
