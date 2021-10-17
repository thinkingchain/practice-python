import requests as req
from bs4 import BeautifulSoup

block = 11851125

#本地代理
proxies = {'http' : '127.0.0.1:7890','https' : '127.0.0.1:7890'}

headers = {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}

def bsc(block) :

        print('block working:'+str(block))

        hexBlock = hex(block)
        url ="https://api.bscscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="
        url = url + str(hexBlock)
        url = url + "&boolean=true&apikey=U1KNQYPX14RKRFDV3DHRHNV5WFGZ7V7UEU"


        #print('url:'+url)

        #res = req.get(url,proxies=proxies,headers=headers)
        res = req.get(url,headers=headers)

        json = res.json()
        result = json['result']
        transactions = result["transactions"]
        print("transactions:"+str(len(transactions)))
        index = 0
        for  transaction in transactions:
            index = index + 1
            to = transaction["to"]
            # print("index" +str(index) + " => to:"+to)
            # to 为空，是创建智能合约
            if not to :
            
                #交易hash
                hash = transaction["hash"]
                transactionUrl = "https://bscscan.com/tx/"
                transactionUrl = transactionUrl + hash
                print(transactionUrl)
                
                #获取合约
                #transactionRes = req.get(transactionUrl,proxies=proxies,headers=headers)
                transactionRes = req.get(transactionUrl,headers=headers)
                #print(transactionRes.content)
                transactionSoup = BeautifulSoup(transactionRes.content,"html.parser")
                contractSpan = transactionSoup.find("span",id="spanToAdd")
                #print("index" +str(index) + " => "+ hash +" => " +contract.getText())
                
                if contractSpan :
                    contract = contractSpan.getText()
                    #print(str(index)+ "=>contract: => " +contract)
                    
                    contractUrl = "https://bscscan.com/token/"
                    contractUrl = contractUrl + contract
                    contractRes = req.get(contractUrl,headers=headers)
                    contractSoup = BeautifulSoup(contractRes.content,"html.parser")
                    officeSiteDiv = contractSoup.find("div",id="ContentPlaceHolder1_tr_officialsite_1")
                
                    if officeSiteDiv:
                        officeSiteText = officeSiteDiv.getText().replace("Official Site:", "").strip()
                        #print(officeSiteText)
                        print("index" +str(index) + " => "+ hash +" => " +contract.getText() +"officeSiteText =>" +officeSiteText)
       
       
        print('fnished:'+str(block))
        
        block = block + 1
        bsc(block)

bsc(block)






