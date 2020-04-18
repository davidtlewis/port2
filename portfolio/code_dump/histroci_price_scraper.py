    def get_historic_prices_v1(self, enddate, days):
        #enddate not yet used - assumes today
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
        def converttonumber(textin):
            try:
                return locale.atof(textin)
            except ValueError:
                return 0
        daysets = int(days/100)
                            
        for y in range(daysets):
            #we have to call api in sets of 100 days
            thisenddate = enddate - BDay(y*100+(y))
            thisstartdate = thisenddate - BDay(100)
            #today = date.today()
            #fromdate = today - BDay(days)
            endunix = int(time.mktime(thisenddate.timetuple()))
            startunix = int(time.mktime(thisstartdate.timetuple()))


            url = "https://uk.finance.yahoo.com/quote/" + self.yahoo_code + "/history?period1=" + str(startunix) + "&period2=" + str(endunix) + "&interval=1d&filter=history&frequency=1d"
            print(y)
            print(url)
            page = requests.get(url)
            contents = page.content
            soup = BeautifulSoup(contents, 'html.parser')
            rows = soup.table.tbody.find_all("tr")
            print (len(rows))
            for table_row in rows:
                columns = table_row.find_all("td")
                if len(columns) == 7:
                    #save price record
                    hp = HistoricPrice(stock = self, date=datetime.strptime(columns[0].text,'%d %b %Y'), open=converttonumber(columns[1].text), high=converttonumber(columns[2].text), low=converttonumber(columns[3].text), close=converttonumber(columns[4].text), adjclose=converttonumber(columns[5].text))
                    hp.save()                   
                    #maybe use uniqueness of data to stop duplicate being added.
            # else:
                    #save div record        