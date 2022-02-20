#Importing Exception Classes
import exceptions
from object import CrawlObject, CrawlItem, CrawlElement

#Importing Dependency Packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys
import random as rand
import time

class Items(object):

    body = None
    kv_pairs = None

    def __init__(self,kv_pairs):
        if type(kv_pairs) is not dict:
            msg = "Items must be a dict. {} is not a compatible type.".format(type(kv_pairs).__name__)
            raise exceptions.UnknownTypeError(type(kv_pairs).__name__,msg)
        
        if "body" not in kv_pairs:
            raise exceptions.MissingItemsError('body')
        
        for i in kv_pairs:
            if type(kv_pairs[i]) not in [str,list]:
                raise exceptions.ItemsValueTypeError()
            
            if type(kv_pairs[i]) is list:
                if len(kv_pairs[i]) == 0:
                    message = "One or more values of Items have an empty list"
                    raise exceptions.EmptyListError(message)
            
            if type(kv_pairs[i]) is str:
                kv_pairs[i] = [kv_pairs[i]]
        
        self.body = kv_pairs["body"][0]
        self.kv_pairs = kv_pairs

    
    def __getitem__(self,index):
        return self.kv_pairs[index]
    
    def keys(self):
        return list(self.kv_pairs.keys())
    

class Delay():

    min_time = 3
    max_time = 5

    def __init__(self, timer='random'):
        if timer not in ['random','static','none',None]:
            raise exceptions.UnknownDelayTimerError(timer)
        
        self.timer = timer

        if self.timer == 'none' or self.timer is None:
            self.min_time = None
            self.max_time = None
        
    def set_timer(self, min_time=None, max_time=None):
        if self.timer == 'random':
            if not min_time or not max_time:
                msg = '"Random delay timer is missing parameter(s) min_time or max_time or both. You need to specify min_time and max_time for a random delay timer."'
                raise exceptions.MissingTimerValueError(msg)

            if min_time > max_time:
                raise exceptions.MaxExceedsMinError
            
            self.min_time = min_time
            self.max_time = max_time
        elif self.timer == 'static':
            if not min_time:
                msg = "Static delay timer is missing parameter min_time. You need to specify min_time for a static delay timer."
                raise exceptions.MissingTimerValueError(msg)

            self.min_time = min_time
            self.max_time = min_time

        else:
            raise exceptions.IllegalSetTimeError()
            
    
    def type(self):
        return self.timer
        
    def wait(self):
        if self.type() in ['random','static']:
            counter = rand.randint(self.min_time,self.max_time)
            print("sleeping {} seconds".format(counter))
            time.sleep(counter)

            
class Crawler():

    base = None
    
    def __init__(self, base, items, crawltype='pagination', delay = Delay('random'), headless=True):
        if type(base) not in [str, list]:
            raise exceptions.UnknownBaseTypeError(type(base).__name__)
        
        if type(items).__name__ != "Items":
            msg = "items must be of type smartcrawler.Items. {} is not a compatible type for items".format(type(items).__name__)
            raise exceptions.UnknownTypeError(type(items).__name__, msg)
        
        if "nextpage" not in items.keys():
            raise exceptions.MissingItemsError('nextpage')
        
        if crawltype not in ['pagination', 'list']:
            raise exceptions.CrawlerTypeError(crawltype)
        
        if type(base) is str and crawltype == "list":
            raise exceptions.BaseTypeMismatchError(type(base).__name__, crawltype)
        
        if crawltype == "list" and len(base) == 0:
            message = "Base list cannot be empty"
            raise exceptions.EmptyListError(message)
        
        if type(base) is list and crawltype == "pagination":
            raise exceptions.BaseTypeMismatchError(type(base).__name__, crawltype)
        
        if headless != True and headless != False:
            raise exceptions.HeadlessValueError()
        
        sys.setrecursionlimit(11000)
        
        self.base = base
        self.items = items
        self.crawltype = crawltype
        self.delay = delay
        self.headless = headless

        if self.crawltype == "list":
            rand.shuffle(base)
        
        self.crawleditems = list()
    
    def start(self):
        if self.crawltype == 'pagination':
            url = self.base
        else:
            url = self.base.pop()

        self.chrome.get(url)

        return True
    
    def fetch(self):
        current_body = self.chrome.find_elements_by_css_selector(self.items.body)

        result = list()

        for item in current_body:
            item_dict = dict()
            for k in self.items.keys():
                if k != "body":
                    item_dict[k] = CrawlElement(None)
                    for i in self.items[k]:
                        v = item.find_elements_by_css_selector(i)
                        if v:
                            item_dict[k] = CrawlElement(v)
                            break
                            
            result.append(CrawlItem(item_dict))

        return CrawlObject(result)

    def next(self):

        flag = False

        if (self.crawltype == 'pagination'):
            nextpage = self.chrome.find_elements_by_css_selector(self.items["nextpage"][0])
            if nextpage:
                nextpage[0].click()
                self.delay.wait()
                flag = True
        elif (self.crawltype == 'list'):
            if len(self.base) > 0:
                nextpage = self.base.pop()
                self.chrome.get(nextpage)
                self.delay.wait()
                flag = True
        
        if not flag:
            self.delay.wait()

        return flag
    
    def run(self):
        self.options = Options()
        self.options.headless = self.headless
        self.chrome = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=self.options)
        self.chrome.set_window_position(-10000,0)

