# Smart Crawler - v.0.0.3
## _The Super smart Python Package for Web crawling_

Smart Crawler is a light weight crawlling package that can be used for crawlling list of items from any webpage.
All you need to configure is the class names of the items need to be crawled and few other settings and you are all set up 😃.

## 1. Features

- Can crawl upto 10,000 pages in one stretch
- Can seemlessly crawl both static and dynamically rendered webpages
- Minimal setup and hassle free web crawling
- Option to visualize the webpages that are being crawled
- In-built delay timer to avoid bot/crawler detection by websites

## 2. Tech

Programming Language(s) in use:
- [Python 3](https://www.python.org/) 

Dependency Package(s):

- [Selenium 3.141.0](https://pypi.org/project/selenium/3.141.0/) - Python bindings for Selenium.
- [Webdriver Manager 3.4.2](https://pypi.org/project/webdriver-manager/3.4.2/) - Library 

And of course Smart Crawler itself is open source with a [public repository](https://github.com/Saketh7382/smartcrawler) on GitHub.

## 3. Installation

Install the package using pip.

```sh
pip install smartcrawler
```

This automatically installs selenium\==3.141.0 and webdriver_manager==3.4.2

## 4. Usage

Here is the simple driver code for crawling the name and image of each product from mobiles section of [amazon.in](https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&s=price-desc-rank&fs=true&qid=1645356896&ref=sr_st_price-desc-rank)

```sh
import json
from smartcrawler import Delay, Items, Crawler

delay = Delay(timer='random')
delay.set_timer(3,7)

items = Items({
    "body": [".s-result-item.s-asin:not([class*='AdHolder'])"],
    "nextpage": ["a.s-pagination-next",".a-last > a"],
    "name": [".a-color-base.a-text-normal"],
    "image": [".s-asin .s-image",".s-asin .s-image"]
})

base_url = 'https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&s=price-desc-rank&fs=true&qid=1645356896&ref=sr_st_price-desc-rank'

c = Crawler(base=base_url, items=items, crawltype='pagination' , delay=delay, headless=True)
c.run()
flag = c.start()

result = list()

while flag:
    items = c.fetch()

    for item in items:
        result.append({
            "name": item["name"].text(),
            "image": item["image"].attr("src")
        })

    flag = c.next()

f = open("./output.json","w")
json.dump(result, f, indent=2)
f.close()
```

#### 4.1 Code Explaination:

```sh
from smartcrawler import Delay, Items, Crawler
```
We need to import three classes namely Delay, Items and Crawler. (Detailed explaination of these classes in [next section](#5-explaining-various-classes-and-options))
- **Delay:** class that is responsible for delayed timings between each crawling to avoid being detected as a bot.
- **Items:** class that is resposible for storing the CSS information of the items that needs to be crawled.
- **Crawler:** main crawler class that is responsible for crawling the information. Instances of Items class and Delay class are provided as input parameters to the Crawler class.

---
```sh
delay = Delay(timer='random')
delay.set_timer(3,7)
```
**Creating an instance of Delay class.** We need to provide the parameter timer to the class. In this example, the timer value is set to 'random'. (*More information regarding Delay class and various possible values of timer parameter and their functions are discussed in [next section](#5-explaining-various-classes-and-options)*).

The 'random' timer value means that the delay (in seconds) between each crawling would be random from time interval [min\_time, max\_time] which are in this case [3,7].

The default [min\_time, max\_time] interval will be [3,5]. We can change this range using `set_timer()` function as did in line 2.

---

```sh
items = Items({
    "body": [".s-result-item.s-asin:not([class*='AdHolder'])"],
    "nextpage": ["a.s-pagination-next",".a-last > a"],
    "name": [".a-color-base.a-text-normal"],
    "image": [".s-asin .s-image",".s-asin .s-image"]
})
```
**Creating an instance of Item class**. The only input parameter to the Item class is a python dict that contains CSS information regarding the items that need to be crawled. The css information is nothing but the CSS selector of the element of intrest. You can learn more about CSS selectors [from here](https://www.w3schools.com/css/css_selectors.asp).

- `body` : CSS selector for the body of the item that is of the intrest.
- `nextpage` : CSS selector for the anchor tag or button that is responsible for pagination to the next page. It must be a clicakble element.
- `name` : CSS selector for the name of the product.
- `image`: CSS selector for the image of the product.

Note: 
1. The `body` and `nextpage` values are mandatory and the program rises an error if we do not provide them. 
2. The `name` and `image` are user defined values.

---

```sh
base_url = 'https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&s=price-desc-rank&fs=true&qid=1645356896&ref=sr_st_price-desc-rank'
```

**base_url** is the first page that our crawler crawls for data. After crawlling this link, our crawler clicks for the element `nextpage` that we have provided in the items instance above to go to the next page.

---

```sh
c = Crawler(base=base_urls, items=items, crawltype='list' , delay=delay, headless=True)
c.run()
flag = c.start()

result = list()

while flag:
    items = c.fetch()

    for item in items:
        result.append({
            "name": item["name"].text(),
            "image": item["image"].attr("src")
        })

    flag = c.next()

f = open("./output.json","w")
json.dump(result, f, indent=2)
f.close()
```

1. First we have created the crawler instance 'c'. Crawler class needs to be configured with five input parameters, namely; base, items, crawltype, delay and headless. 
- `base_url`, `items` and `delay` instances that we have created above are passed to Crawler class using base, items and delay parameters respectively.
- The parameters crawltype and headless will be discussed in length in subsequent sections, for this example, we kept values `pagination` and `True` for the parameters crawltype and headless respectively.
2. `c.run()` creates a browser instance managed by selenium and webdriver_manager packages. Depending on the value of headless parameter False/True, the browser will be visible/invisible.
3. `c.start()` is responsible for crawling the **base_url**. This function returns True always and we have stored it as a flag variable that begins a while loop.
4. The while loop is started with flag variable as breaking condition, since `c.start()` always returns True, we enter the loop, where we fetch the items that has been crawled, in this case, items crawled from **base_url**.
5. Inside the loop, we call `c.fetch()` which returns the crawled items as an CrawlObject class instanve. CrawlObject is an Iterable object. Each element inside the CrawlObject class is a CrawlItem class instance. Each CrawlItem instance in items can be indexed using the key values that we have used for initiating Items class earlier. In this case valid indexed will be `name` and  `image` (not `body` and `nextpage`, since they are not user defined key values). 
6. We use a for loop to access each CrawlItem class. As mentioned earlier, we access crawled element using its appropriate index value (`name` and  `image`), the data from these elements are accessed using one of the following ways:
- If the element is something that contains text data (eg; span, p, etc...), you can access the element's text data using `text()` function. Here the name element is a span element and we require the text of the span element hence we use `item["name"].text()` to access the data.
- Another way to access the data is by `attr()` method. This method can be used if the data we are accessing is that of an attribute value of that particular element. In this case, we need the image element is an <img/> html element and we need the value of src attribute of the <img/> element. Hence we use `item["image"].attr("src")` to access the value of src attribute.
7. The data extracted in above step are again stored as a key value pair and is appended to a list, here `result`.
8. After successfully extracting the data that we have crawled, its time to move on to the next page and this can be achieved by `c.next()`. The `c.next()` works as same as `c.start()`. The metod `c.start()` is used to crawl the base page that is being specified using **base_url**.  `c.next()` on the other hand clicks on the element that we have mentioned using nextpage key in items instance. This loads the next page and the method crawls and loads the items crawled in the next page.
9. As in `c.start()` which always returns True, `c.next()` only returns true of the nextpage element is found, clicked and loaded. If not it returns False. We again assign the return value of `c.next()` to the flag variable, which is the condition to continue or break the while loop.
10. If next page is found, flag becomes True and we enter into the next iteration of the while loop and process is repeated from step.5, else the loop is breaked and we get out of the loop with crawled data being stored inside the `result` list.
11. In the end, we store the `result` list into a json file.


## 5. Explaining Various Classes and Options

In this section we will discuss all the three classes, namely; `Delay`, `Items` and `Crawler` that we use to perform crawling, in detail. We have already seen how to use them in above example, now let us look at what each and individual input parameters to these classes represent and various functionalities and advance options you can enable.

### 5.1. Delay
The Delay class is responsible for to introduce delays (in seconds) in between crawling of two pages. This is necessary because most of the websites block the crawlers after certain number of crawls. In order to not get blocked and ensure a smooth crawling flow, we need to wait few seconds after each crawling so that websites do not recognise the crawler. 

There are three types of delays we can introduce using this class. They are:
1. `random` : This type introduces random delays in between each crawling. We need to set the time interval range and the class chooses the amount of delay time from within this provided range. For ex; if we set the range to [3,7], then the timer waits x seconds of time in between each crawling where x is random timing between 3 and 7 seconds (3 & 7 included).
2. `static`: This type introduces a constant delay in between each crawling. For ex; if we set the timer to 5, then it waits 5 seconds after every crawl until end.
3. `none`: This type does not introduces any kind of delay in between each crawling and crawler continues to crawl in its own speed. (Not recomended)

We can choose one of the above values to initiate the Delay class. This can be done using timer parameter.

```sh
delay = Delay(timer='static')
```
The default value of the timer parameter will be `random`.

#### 5.1.1 set\_timer()

```sh
Delay.set_timer(min_time, max_time)
```

This function is used to set the delay value. It takes two parameters `min_time` and `max_time`. By default, these values are set to 3 & 5 respectively. That is if we use the type random delay, then by default the random time interval will be between 3 to 5 seconds. And in the same way if we use the static delay type, then the default delay time would be 3 seconds between each crawl.

We need to provide both `min_time` and `max_time` values in case we need to overwrite default delay values for a random delay type. In case of static delay type providing only  `min_time` value would be suffice. The `max_time` value would be ignored even if you used it on a static delay type.

We cannot use set_timer() function on a `none` type delay. This raises a `IllegalSetTimeError`.

#### 5.1.2 Exceptions

1. `MissingTimerValueError` : This is raised if we do not provide both min\_time and max\_time parameters for set\_timer function over a random delay type or if do not provide min\_time parameter for set\_timer function over a static delay type.
```sh
delay = Delay(timer='random')
delay.set_timer(3) #rises exception - case 1

delay = Delay(timer='static')
delay.set_timer() #rises exception - case 2
```
2. `MaxExceedsMinError` : This is raised if the value of min\_time exceeds the value of max\_time.
```sh
delay.set_timer(10,7) #rises exception
```
3. `IllegalSetTimeError` : This is raised if the value use set\_timer function over a none delay type
```sh
delay = Delay(timer='none')
delay.set_timer(3,7) #rises exception
```

### 5.2 Items

The Items class is responsible for storing the CSS information of the items that we need to crawl. To initiate this class instance, we need to provide a python dictionary of key value pairs as an input parameter where the values are CSS selectors. This input dictionary follows certain rules. They are:

1. The values of the dictionary should be CSS selectors and should be of either of type `str` or of type `list`. If you have just one CSS selector for the item, you can keep it as `str` and if you have bunch of selectors that point out to same value, for ex; in some pages, the name of the item is represented by CSS selector-1 and in some other pages it is by CSS selector-2, then you can all the possible CSS selectors of that item into a `list` and the Crawler will iterate over the list until it finds a match to crawl. 
2. There should be a key value pair with key being `body` and its value being CSS selector of the item's wrapper element. Usually while crawling list of items from a web page, the `body` will be the CSS selector that selects all the items in that page. This is a mandatory key and not providing the `body` key-value will raise `MissingItemsError`
3. If the crawler type is `pagination` (you can learn more about types of Crawlers in [next sub section](#53-Crawler)), then we need to provide another mandatory key-value pair with key being `nextpage`. The value of it should be the CSS selector of the element that is responsible for pagination to the next page and it should be a clickable element (<a> or <button>).
4. The other key value pairs in the dictionary are user defined. They can keep any name to the keys (except for body and nextpage) and the values should follow rule 1.

#### 5.2.1 Exceptions

1. `ItemsValueTypeError` : This is raised if we provide values other than `str` and `list` within input dictionary.
```sh
items = Items({
    "body": 123  #raises exception
})
```
2. `EmptyListError` : This is raised if there we provide empty list as a value within input dictionary.
```sh
items = Items({
    "body": [] #raises exception
})
```

### 5.3 Crawler

The Crawler class is responsible for performing crawling. We can initiate the Crawler class by setting up the following input parameters:
1. `crawltype`: This input parameter decides the type of the crawler. There are two types of crawlers we can use to crawl the site. They are 'pagination' and 'list' respectively. 
- By setting the value to 'pagination', we are initiating the crawler with just one base_url, from which it clicks on 'nextpage' ([reference: section 5.2](#5-2-items)). 
- By setting the value to 'list' we provide the list of urls to crawl for the crawler before hand and it picks the next url to crawl from this list instead of relying on `nextpage` element.
2. `base`: This input parameter takes either one URL (in case of crawltype='pagination') as str or list of URLs as list (in case of crawltype='list').
3. `items`: Takes the instance of Items class.
4. `delay`: Takes the instance of Delay class.
5. `headless`: This input parameter takes either **True** or **False** as value. Setting it to True will allows the crawler in background without opening a browser instance. Setting it to False will open the browser and instance and user can check the webpage that the crawler is crawling at any particular time during the process.

#### 5.3.1 run()

This function creates a browser instance. Depending on the value set to the `headless` input parameter, this browser instance will be visible/invisible.

#### 5.3.2 start()

This function crawls the first URL, known as home URL or base URL. In pagination crawler type, this first URL will be the URL passed as value to the `base` parameter. In list crawler type, the crawler receives list of URLs from `base` parameter and the crawler shuffles these URLs and randomly picks one of the URL to be the base URL.

#### 5.3.3 fetch()

This function gets the data that has been crawled at current iteration. It returns the crawled items as an CrawlObject class instanve. CrawlObject is an Iterable object. Each element inside the CrawlObject class is a CrawlItem class instance. Each CrawlItem instance in items can be indexed using the key values that we have used for initiating Items class earlier. (refer [section 4.1 for detailed explaination](#41-code-explaination))

#### 5.3.3 next()

This function works as same as `c.start()`. The metod `c.start()` is used to crawl the base page that is being specified using `base` input parameter. `next()` on the other either hand clicks on the element that we have mentioned using nextpage key in items instance (in case of crawltype='pagination') or chooses another URL from the list provided using `base` parameter in case of crawltype='list'. This loads the next page and the method crawls and loads the items crawled in the next page. (refer [section 4.1 for detailed explaination](#41-code-explaination))

## License

MIT

**Free Package, Hell Yeah!**

