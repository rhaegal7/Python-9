# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup
import io

def get_baidu_search(url,first_page = True):
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text,'lxml')
    
    result = []
    
    for container in soup.find_all(attrs= {'class':'result c-container '}):
        temp = {}
        
        for t in container.find_all(attrs = {'class':'t'}):
            title = ""
            for item in t.find('a').contents:
                title += str(item).replace('<em>','').replace('</em>','')
                   
            temp['title'] = title
            temp['link'] = t.find('a').get('href')
        
        description = ''
        for item in container.find_all(attrs = {'class':'c-abstract'}):
            for i in item.contents:
                description += str(i).replace('<span class=" newTimeFactor_before_abs m">','').replace('</span>','').replace('<em>','').replace('</em>','')
        temp['description'] = description

        result.append(temp)
    
    if first_page:
        next_page = soup.find(id = 'page').find(attrs={'class': 'n'}).get('href')
    else:
        next_page = soup.find(id = 'page').find(attrs={'class': 'n'}).find_next_sibling(attrs={'class': 'n'}).get('href')
        
    return result,next_page

def get_bing_search(url):
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text,'lxml')
    
    result = []
    next_page = ''
    
    for li in soup.find_all(attrs= {'class':'b_algo'}):
        temp = {}
        
        title = ""
        for item in li.find('a').contents:
            title += str(item).replace('<strong>','').replace('</strong>','')
        temp['title'] = title
        
        temp['link'] = li.find('a').get('href')
        
        description = ''
        for item in li.find('p'):
            description += str(item).replace('<span class="news_dt">','').replace('</span>','').replace('<strong>','').replace('</strong>','')
        temp['description'] = description
        
        result.append(temp)
    
    next_page = soup.find(attrs={'class': 'sb_pagN sb_pagN_bp sb_bp '}).get('href')

    return result,next_page
    
    
def print_result(result):
    for i in result:
        print('title:')
        print(i['title'])
        print('link:')
        print(i['link'])
        print('description:')
        print(i['description'])
        print()

            
        
def main():
#    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#    print(' '.join(sys.argv[1:]))

    base1 = 'http://www.baidu.com'
    base2 = 'https://www.bing.com'
    
    word = ' '.join(sys.argv[1:])
#    word = '吉岡里帆'
    
    page = 1
    next_url_part1 = ''
    next_url_part2 = ''
    while(page<=5):
        print('第' + str(page)+'页:')
        
        if(page == 1): 
            url1 = base1 + '/s?wd='+word
            result1,next_url_part1 = get_baidu_search(url1)
            
            url2 = base2 +'/search?q=' + word
            result2,next_url_part2 = get_bing_search(url2)
            
        else:
            url1 = base1 + next_url_part1
            result1,next_url_part1 = get_baidu_search(url1,first_page=False)
            
            url2 = base2 + next_url_part2
            result2,next_url_part2 = get_bing_search(url2)

        print('百度baidu:\n')
        print_result(result1)
        print('\n\n\n必应bing:\n')
        print_result(result2)
        
        ans = input('next page?[y/n] (5 pages most)')
        if ans == 'y':            
            page += 1
        else:
            break
#        page +=1
    
    

if __name__ == '__main__':
    main()