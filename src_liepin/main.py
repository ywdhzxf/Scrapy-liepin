from scrapy import cmdline
# cmdline.execute('scrapy crawl lp'.split())

import os
os.chdir('src_liepin/spiders')
cmdline.execute('scrapy runspider liepin2.py'.split())