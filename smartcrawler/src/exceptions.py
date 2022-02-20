'''
Delay class errors
'''

class UnknownDelayTimerError(Exception):
    def __init__(self, timer):
        self.message = "The value {} is an unknown timer paramater. Please select 'random' or 'static', or 'none'".format(timer)
        super().__init__(self.message)

class MissingTimerValueError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class IllegalSetTimeError(Exception):
    def __init__(self):
        super().__init__("You cannot call set_timer() method for a None delay timer")

class MaxExceedsMinError(Exception):
    def __init__(self):
        super().__init__("The value of min_time should not exceed max_time")

'''
Crawler Errors
'''

class CrawlerTypeError(Exception):
    def __init__(self, crawlertype):
        self.message = "The value {} is an unknown crawlertype paramater. Please select 'pagination' or 'list'".format(crawlertype)
        super().__init__(self.message)

class UnknownBaseTypeError(Exception):
    def __init__(self,basetype):
        message = "The type {} is not a valid type for base. The base type should be either str or list".format(basetype)
        super().__init__(message)

class BaseTypeMismatchError(Exception):
    def __init__(self,basetype,crawlertype):
        message = "{} is not a valid base type for a {} crawler.".format(basetype, crawlertype)
        super().__init__(message)

class HeadlessValueError(Exception):
    def __init__(self):
        super().__init__("The headless parameter should only be set to either True of False.")

class EmptyListError(Exception):
    def __init__(self, message=None):
        if not message:
            self.msg = "List cannot be empty"
        else:
            self.msg = message
        super().__init__(self.msg)

'''
Items Class Errors
'''

class MissingItemsError(Exception):
    def __init__(self,val):
        super().__init__("The Items should contain a key-value pair with key '{}'".format(val))

class ItemsValueTypeError(Exception):
    def __init__(self):
        super().__init__("One or More values of Item dict is neither str nor list")

'''
Generic Errors
'''

class UnknownTypeError(Exception):
    def __init__(self, typeclass ,msg = None):
        if not msg:
            self.message = "{} is an unknown type".format(typeclass)
        else:
            self.message = msg

        super().__init__(self.message)