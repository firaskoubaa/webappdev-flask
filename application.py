from flask import Flask, render_template, request, url_for, redirect
import requests
import mysql.connector

#Fetching data using Google Books API
# research=input('Type the name of the book please: ')
# research='good'
# research=research.replace(' ', '+')
def api_fetchdata(subject):
    global matrix_data
    matrix_data=[]
    rq = requests.get('https://www.googleapis.com/books/v1/volumes?q='+subject)     # gives the respons type <Response [200]>
    response = rq.json()            # extracts the json data
    all_items=response['items']     # extracts value of the key "items" which is another dictionnary
 
    for item_num in range(len(all_items)):
        itemid=all_items[item_num]['id']
        title=all_items[item_num]['volumeInfo']['title']

        try:
            cover=all_items[item_num]['volumeInfo']['imageLinks']['thumbnail']
        except:
            cover="/static/img/book_cover_backup.png"

        try:
            subtitle=all_items[item_num]['volumeInfo']['subtitle']
        except:
            subtitle=''

        try:
            pre_authors=all_items[item_num]['volumeInfo']['authors']
            authors=pre_authors[0] 
            if len(pre_authors)>1:
                for i in range(len(pre_authors)-1):
                    authors=authors+', '+pre_authors[i+1]
        except:
            authors=""

        try:
            publishedDate=all_items[item_num]['volumeInfo']['publishedDate'][:10]
        except:
            publishedDate=""

        if all_items[item_num]['saleInfo']['saleability']==	'FOR_SALE':
            price=str(all_items[item_num]['saleInfo']['retailPrice']['amount'])
        else:
            price=all_items[item_num]['saleInfo']['saleability']

        previewlink="https://books.google.com/books?id="+itemid
        # print('book n°'+str(item_num+1)+' id: '+itemid+' cover:'+cover+' title: '+title+' subtitle: '+subtitle+' authors: '+authors+' publishedDate: '+publishedDate+' price: '+price+' previewlink: '+previewlink)
        book_data=[cover,title,subtitle,authors,publishedDate,price,previewlink]
        matrix_data.append(book_data)
   

#Connect to the webapp database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mysql=123",
  database="website_db"
)
mycursor = mydb.cursor()

#read data from database
mycursor.execute("select * from all_products")
myresult = mycursor.fetchall()

# # insert datat in database
# sql = "INSERT INTO all_products (name, price, description) VALUES (%s, %s, %s)"  #formating to avoid SQL Injection
# val = ('Umidigi ',120.00,'midrange phone')
# mycursor.execute(sql, val)
# mydb.commit()

app = Flask(__name__)


@app.route("/")
def index():    
    req = request.args          # .args for GET method and .form for POST method
    print(req)
    rs = req.get("research_text")
    print(rs)
    if rs == None or rs =="":
        return render_template("index.html")
    else:
        research=rs.replace(' ', '+')
        api_fetchdata(research)
        return render_template("index.html", students=matrix_data, results=myresult )
  


@app.route("/project1")
def project1():
    return render_template("project1.html")

@app.route("/project2")
def project2():
    return render_template("project2.html")

@app.route("/project3")
def project3():
    return render_template("project3.html")



if __name__=="__main__":
    # app.run()
    app.run(debug=True)