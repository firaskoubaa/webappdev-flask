from flask import Flask, render_template, request, url_for, redirect
import requests
import mysql.connector

#Fetching data using Google Books API
# research=input('Type the name of the book please: ')
# research='good'
# research=research.replace(' ', '+')
matrix_data=[]

def api_fetchdata(subject):
    global matrix_data
    matrix_data=[]
    rownum=0
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
        book_data=[cover,title,subtitle,authors,publishedDate,price,previewlink,rownum]
        rownum += 1
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
bookshelf_db = mycursor.fetchall()

app = Flask(__name__)

@app.route("/")
def index():    
    req = request.args          # .args for GET method and .form for POST method
    print(req)
    rs = req.get("research_text")
    print(rs)
    if rs == None or rs =="":
        return render_template("index.html", bookshelf=bookshelf_db)
    else:
        research=rs.replace(' ', '+')
        api_fetchdata(research)
        return render_template("index.html", reasearch_tab=matrix_data, bookshelf=bookshelf_db)
  
@app.route("/ajax_reader", methods=["POST"])
def ajax_reader():
    button_id = int(request.form["button_id"])
    print("button clicked is number: " + str(button_id))
    if button_id in range(10):
        # add line button_id data to db
        sql = "INSERT INTO all_products (cover,title,subtitle,authors,publishedDate,price,previewlink) VALUES (%s, %s, %s,%s, %s, %s,%s)"
        val = matrix_data[button_id][0:7]
        mycursor.execute(sql, val)
        mydb.commit()
        render_template("index.html", reasearch_tab=matrix_data, bookshelf=bookshelf_db)
        return redirect(request.url)
    elif button_id in range(10,20):
        # delete line button_id-10 data to db
        sqlinst="DELETE FROM all_products WHERE id = %s;"
        rowtodel = (button_id-10,)
        print(type(rowtodel))
        mycursor.execute(sqlinst, rowtodel)
        mydb.commit()
        return redirect(request.url)
  
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