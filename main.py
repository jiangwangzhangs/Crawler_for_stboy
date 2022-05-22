import requests, re
from lxml import etree
from bs4 import BeautifulSoup

#the target website:
url = 'https://stboy.net/forum.php?mod=forumdisplay&fid=467&page=1'
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
'cookie': 'HwLz_2132_saltkey=G36cS66z; HwLz_2132_lastvisit=1653141264; HwLz_2132_sendmail=1; HwLz_2132_ulastactivity=338fVAplP9LgBPUg5XBVI9dMFF84mJuCfY6q4dTqZfr17mODFOGD; HwLz_2132_auth=88143%2B%2BK5%2FGQGle2s63lXxObzVWJ8yAlKirLyVttNM6waHYpUQU1KEcZ%2FygeWt9O4him7MGttRmNZ352HcVmBjPkmHPa; HwLz_2132_lastcheckfeed=1067315%7C1653144874; HwLz_2132_nofavfid=1; HwLz_2132_checkpm=1; HwLz_2132_st_t=1067315%7C1653145075%7C14343fe010f3005d6cf63414b848f51c; HwLz_2132_forum_lastvisit=D_465_1653145072D_467_1653145075; HwLz_2132_visitedfid=467; HwLz_2132_sid=zBR2ic; HwLz_2132_lip=2408%3A820c%3A820d%3Ad030%3Ab8cf%3A7440%3A307f%3Ac2d0%2C1653145075; HwLz_2132_lastact=1653145076%09misc.php%09patch'
}

#get context of target websiet
respond_1 = requests.get(url=url, headers=headers)

#analyse and get the link of every child website
html_1 = etree.HTML(respond_1.text)
divs = html_1.xpath('/html/body/div[8]/div[4]/div/div/div[5]/div[2]/form/table/tbody')
link_child_list = []
for div in divs:
    type_child = div.xpath('./tr/th/em/a[1]/text()')
    link_child = div.xpath('./tr/th/a[2]/@href')
    title_child = div.xpath('./tr/th/a[2]/text()')
    if title_child:
        if str(*link_child).startswith('forum'):
            link_child_list.append((*type_child, *title_child, 'https://stboy.net/'+str(*link_child)))
    # break


#get context of every child website
result_list = []
for ele in link_child_list:
    type_child, title_child, link_child = ele
    respond_2 = requests.get(url=link_child, headers=headers)
    html_2_bs4 = BeautifulSoup(markup=respond_2.text, features='html.parser')
    pan_inf = html_2_bs4.findAll(name='meta', attrs={'name': 'description'})
    lk_re1 = re.compile(r'链接[：:]?[ ]?(?P<link>.*?) ', re.S)
    pw_re2 = re.compile(r'提取码[：:]?[ ]?(?P<password>\w{4})', re.S)

    pan_inf = [str(ele) for ele in pan_inf]
    if pan_inf:
        for meta in pan_inf:
            result_it1 = lk_re1.finditer(str(meta))
            result_it2 = pw_re2.finditer(str(meta))
            for result_lk in result_it1:
            # result_re = result_it.__next__()
                link_pan = result_lk.group('link')
            for result_pw in result_it2:
                password_pan = result_pw.group('password')

            result_list.append((type_child, title_child, link_pan, password_pan))

for link in result_list:
    type_child, title_child, link_pan, password_pan = link
    print(type_child,'标题：', title_child, '链接：', link_pan, '提取码：', password_pan, '\n')
#


#anaylse and get the baidupan link from every child website
