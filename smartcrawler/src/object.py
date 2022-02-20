import exceptions

class CrawlObject(object):

    result = list()
    crawled = list()

    def __init__(self,result):
        self.result = result
    
    def __getitem__(self,index):
        return self.result[index]

    
class CrawlItem(object):

    item = dict()

    def __init__(self,item):
        self.item = item
    
    def __getitem__(self,index):
        if type(index) is int:
            keys_list = list(self.item.keys())
            return self.item[keys_list[index]]
        else:
            return self.item[index]
    
    def keys(self):
        return list(self.item.keys())
    

class CrawlElement():

    element = None

    def __init__(self,element):
        self.element = element
    
    def text(self):
        return self.element[0].text
    
    def attr(self,attribute):
        return self.element[0].get_attribute(attribute)
    
