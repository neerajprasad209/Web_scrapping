from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import logging
from urllib.request import urlopen as  uReq

logging.basicConfig(filename="scrapper_2.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/",methods = ['GET'])
def home_page():
    return render_template("index.html")

@app.route("/result",methods = ['POST','GET'])
def index():
    
    if request.method == 'POST':
        
        try: 
            
            if request.method == 'POST':
                searchstring = request.form['content'].replace[" ",""]
                link = "https://www.flipkart.com/search?q=" + searchstring 
                
                url_link = uReq(link)
                flipkart_page = url_link.read()
                flipkart_html = bs(flipkart_page, "html.parser")
                
                bigbox = flipkart_html.find_all("div",{"class":"_1AtVbE col-12-12"})
                del bigbox[0:3]
                box = bigbox[0]
                
                product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
                
                prodRes = requests.get(product_link)
                prodRes.encoding = 'utf-8'
                
                prod_html = bs(prodRes.text,"html.parser")
                print(prod_html)
                
                commentboxs = prod_html.find_all("div",{"class": "_16PBlm"})
                
                filename = searchstring +'.csv'
                fw =open(filename,'w')
                headers = "Product, Customer Name, Rating, Heading, Comment \n"
                fw.write(headers)
                reviews = []
                
                for commentbox in commentboxs:
                    try:
                        name  = commentbox.div.div.div.find_all('p',{"class": "_2sc7ZR _2V5EHH"})[0].text
                        
                    except:
                        logging.info("name")
                    
                    try:
                        
                        rating = commentbox.div.div.find_all("p",{"class": "_2sc7ZR _2V5EHH"})[0].text
                    except:
                        rating = "no rating"
                    
                    try:
                        commentHead = commentbox.div.div.find_all("p",{"class":"_2-N8zT"})[0].text
                    except:
                        commentHead= 'No Comment Heading'
                        
                    try:
                        comtag =  commentbox.div.div.find_all("div",{"class":""})
                        custComment = comtag[0].div.text
                    except Exception as e:
                        logging.info(e)
                    
                    mydict = {"Product": searchstring, "Name": name, "Rating": rating, "CommentHead": commentHead,
                            "Comment": custComment}
                    reviews.append(mydict)
                logging.info("log my Final Result {}".format(reviews))
                return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return "Something went Wrong"
    else:
        return render_template('index.html')
    
        

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")