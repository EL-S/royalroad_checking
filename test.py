import requests
from time import sleep
from bs4 import BeautifulSoup
import plyer
url_for_auth = "https://www.royalroad.com/account/login?returnUrl=https%3A%2F%2Fwww.royalroad.com%2Fhome"
url_for_books = "https://www.royalroad.com/my/bookmarks"
url_for_check = "https://www.royalroad.com/fictions/latest-updates"

payload = {
	"ReturnUrl": "https://www.royalroad.com/home",
	"Email": "***********",
	"Password": "********",
	"__RequestVerificationToken": "**************",
	"Remember" : "false"
}
i = 0
with requests.Session() as s:
	#auth
	s.post(url_for_auth,data = payload)
	#user_fictions
	res = s.get(url_for_books)
	soup = BeautifulSoup(res.text, "lxml")
	fictions = [x.find("a",class_="font-red-sunglo bold").text for x in soup.find_all("h2",class_="fiction-title")]
	while True:
		#updated_fictions
		res = s.get(url_for_check)
		soup = BeautifulSoup(res.text, "lxml")
		updated_fictions = [x.find("a").text for x in soup.find_all("h2",class_="fiction-title")]
		for el in fictions:
			if el in updated_fictions:
				plyer.notification.notify( message='Вышля новая глава',title=el)
		i += 1
		print(f"Закончил проверку №{i}")
		sleep(120)
