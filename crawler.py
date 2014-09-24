#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import re
import urllib
import argparse
import threadpool
from collections import deque

base_url = 'http://www.22mm.cc'
sub_url = 'href=\"(/mm/.+?)\"'
pic_url = '0]=\"(http://.+?)\"'


class Crawler:
    def __init__(self, url, sub, pic, limit, threads, outdir):
        self.url = url
        self.re_sub = sub
        self.re_pic = pic
        self.limit = limit
        self.outdir = outdir
        self.threads = threads

    def start(self):
        # handle thread
        urls = [base_url]

        pool = threadpool.ThreadPool(self.threads)
        requests = threadpool.makeRequests(self.real_iron, urls)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def html_get(self, url):
        # TODO: handle exception and retries
        fp = urllib.urlopen(url)
        return fp.read()

    def real_iron(self, urls):
        queue = deque()
        queue.append(urls)
        visited = set()
        imgs = set()

        while queue:
            l = queue.popleft()
            visited |= {l}

            print "Get Page:"+l
            data = self.html_get(l)
            # get the whole
            linkre = re.compile(self.re_sub)
            for page in linkre.findall(data):
                page = base_url + page

                if page not in visited:
                    # TODO: reduce html_get
                    if 'html' in page:
                        print "Get Html:"+page
                        page_data = self.html_get(page)
                        # capture the img
                        pattern = re.compile(self.re_pic)
                        for pic in pattern.findall(page_data):
                            pic = pic.replace('big', 'pic')
                            imgs |= {pic}
                            # reach the limit
                            if len(imgs) == self.limit and self.limit != 0:
                                # download img
                                cnt = 0
                                for each in imgs:
                                    print 'Downloading image: '+each
                                    cnt += 1
                                    i = each.rfind('/')
                                    img_name = each[(i+1):]
                                    full_path = self.outdir+'/'+img_name
                                    print 'Saving to: ' + full_path
                                    urllib.urlretrieve(each, full_path)
                                    print "%d mm_pic downloaded." % cnt
                                sys.exit()
                    queue.append(page)


def main():
    # handle arg
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--threads", type=int, default=10,
                        help="number of threads (default: 10)")
    parser.add_argument("-l", "--limit", type=int, default=0,
                        help="number of max images (default: 0 -> nolimit)")
    parser.add_argument("-o", "--outdir", default='./pics',
                        help="images output dir (default: ./pics)")

    args = parser.parse_args()
    args.threads = args.threads or 10
    args.limit = args.limit or 0
    args.outdir = args.outdir or './pics'

    if os.path.exists(args.outdir) is False:
        os.mkdir(args.outdir)

    crawler = Crawler(base_url, sub_url, pic_url,
                      args.limit, args.threads, args.outdir)
    crawler.start()

if __name__ == '__main__':
    main()
