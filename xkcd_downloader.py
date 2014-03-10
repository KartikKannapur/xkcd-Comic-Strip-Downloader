from BeautifulSoup import BeautifulSoup
import urlparse
import urllib2
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

import urllib
import re
import json
 
def main():
    # remove, make and move into the XKCD_IMAGES directory
    if not os.path.isdir('JSON'):
        os.mkdir('JSON');
    safeDelMove('XKCD_IMAGES')
    upto = getUpto()
    num = getCurrent()
    
    for cnt in range(upto, num+1):
        if cnt == 404:
            continue
        getImg(cnt)
    
    return 0
 
def getCurrent():
    
    print "Fetching home page: trying to identify latest number"
    # put the homepage into a BeautifulSoup
    f = urllib.urlopen("http://xkcd.com/info.0.json")
    s = f.read()
    f.close()
    latest = json.loads(s)
    print "Found latest comic was: " + str(latest['num'])
    return int(latest['num']);
 
def getImg(number):
    strNum = str(number)
    print "Getting image for comic: " + strNum
    # extract the image url from the page
    f = urllib.urlopen("http://xkcd.com/"+strNum+"/info.0.json")
    comics = f.read()
    f.close()
    comic = json.loads(comics)
    # clean up the url
    imgUrl = comic['img'];
    ext = imgUrl.split('.')[-1]
    # download the img
    filename = strNum + "." + ext
    urllib.urlretrieve(imgUrl, filename)
    # write the raw json data
    f = open("../JSON/"+strNum+".json",'w')
    f.write(comics)
    f.close()
 
    print "Successfully downloaded:  " + strNum
 
def safeDelMove(s):
    if not os.path.isdir(s):
        os.mkdir(s);
    os.chdir(s)
 
def getUpto():
    upto = 0
    dirs = os.listdir('.')
    for f in dirs:
        x = int(re.sub(r"\..+", "", f))
        if x > upto:
            upto = x
    return upto+1
 
if __name__ == '__main__':
    main()
