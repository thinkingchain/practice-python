import requests as req
from bs4 import BeautifulSoup
import pymongo
import sys, threading
from datetime import datetime 

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

timeout = 10

bscClient = pymongo.MongoClient("mongodb://localhost:27017/")
bscDB = bscClient["newcoins-test"]
contractCol = bscDB["contracts"] 
blockCol = bscDB["block"]

workerThread = 2

worker = blockCol.find_one({"worker":workerThread})
block = worker["block"]

#本地代理
proxies = {'http' : '127.0.0.1:7890','https' : '127.0.0.1:7890'}

headers = {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}

def bsc(block) :

        print('block working:'+str(block))

        hexBlock = hex(block)
        url ="https://api.bscscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="
        url = url + str(hexBlock)
        url = url + "&boolean=true&apikey=U1KNQYPX14RKRFDV3DHRHNV5WFGZ7V7UEU"

        #res = req.get(url,proxies=proxies,headers=headers)
        res = req.get(url,headers=headers,timeout=timeout)

        json = res.json()
        result = json['result']
        transactions = result["transactions"]
        index = 0
        for  transaction in transactions:
            index = index + 1
            to = transaction["to"]
            # to 为空，是创建智能合约
            if not to :
            
                #交易hash
                hash = transaction["hash"]
                transactionUrl = "https://bscscan.com/tx/"
                transactionUrl = transactionUrl + hash

                #print(transactionUrl)
               
                #获取合约
                transactionRes = req.get(transactionUrl,headers=headers,timeout=timeout)
                transactionSoup = BeautifulSoup(transactionRes.content,"html.parser")
                contractSpan = transactionSoup.find("span",id="spanToAdd")
                
                #获取创建时间
                contentPlaceHolder1_divTimeStamp  = transactionSoup.find("div",id="ContentPlaceHolder1_divTimeStamp")
                divTimeStamp = contentPlaceHolder1_divTimeStamp.find("div", class_="row align-items-center")
                divTimeStamp2 = divTimeStamp.find("div", class_="col-md-9").getText()
                strTimeStamp = divTimeStamp2[divTimeStamp2.index("(")+1:divTimeStamp2.index(")")].replace("+UTC","").strip()
                
                dt = datetime.strptime(strTimeStamp, '%b-%d-%Y %I:%M:%S %p')
                timeStamp = dt.strftime('%Y-%m-%d %H:%M:%S')

                if contractSpan :
                    #合约地址
                    contract = contractSpan.getText()
                    
                    contractUrl = "https://bscscan.com/token/"
                    contractUrl = contractUrl + contract
                    contractRes = req.get(contractUrl,headers=headers,timeout=timeout)
                    contractSoup = BeautifulSoup(contractRes.content,"html.parser")

                    # 网址
                    officeSiteDiv = contractSoup.find(
                        "div", id="ContentPlaceHolder1_tr_officialsite_1")
                    if not officeSiteDiv:
                        print("officeSite is null : " +contractUrl)
                        continue
                    officeSiteText = ""
                    if officeSiteDiv:
                        officeSiteText = officeSiteDiv.getText().replace("Official Site:", "").strip()
                     
                    
                     # 发行总量
                    supplyDiv = contractSoup.find("div", class_="col-md-8 font-weight-medium")
                    supply = supplyDiv.find("span", class_="hash-tag text-truncate").getText()
                    token = supplyDiv.find("b").getText()
                    # 如果发行量是空，将跳过该合约，继续循环
                    if not supply or supply == "0" :
                        continue


                    # 价格price
                    price = ""
                    contentPlaceHolder1_tr_valuepertoken = contractSoup.find(
                        "div", id="ContentPlaceHolder1_tr_valuepertoken")

                    if contentPlaceHolder1_tr_valuepertoken :
                        priceSpan = contentPlaceHolder1_tr_valuepertoken.find(
                            'span', class_='d-block').find(attrs={'data-toggle': 'tooltip'})
                        price = priceSpan.getText()
                   
                    # 总市值
                    marketCap = ""
                    if contentPlaceHolder1_tr_valuepertoken :
                        marketCapSpan = contentPlaceHolder1_tr_valuepertoken.find(
                        'button', class_='u-label u-label--sm u-label--value u-label--text-dark u-label--secondary rounded')
                        if marketCapSpan :
                           marketCap = marketCapSpan.getText().strip()
                    
                   

                    # Holders
                    contentPlaceHolder1_tr_tokenHolders = contractSoup.find(
                        "div", id="ContentPlaceHolder1_tr_tokenHolders")
                    holders = contentPlaceHolder1_tr_tokenHolders.find(
                        "div", class_="mr-3").getText().replace("addresses", "").strip()
                    
                    # Transfers
                    #contentPlaceHolder1_trNoOfTxns = contractSoup.find( "div", id="ContentPlaceHolder1_trNoOfTxns")
                    #transfers = contentPlaceHolder1_trNoOfTxns.find("span",id="totaltxns").getText()

                   

                    bscContract = { "contract":contract,"hash":hash,"price": price, "marketCap": marketCap,"supply": supply,"token": token, "holders": holders,"site": officeSiteText,"timeStamp":timeStamp}
                    x = contractCol.insert_one(bscContract) 
       
        print('fnished:'+str(block))
        y = blockCol.update({"worker":workerThread}, {"worker":workerThread,"block":block})
        
        block = block + 2
        bsc(block)

bsc(block)






