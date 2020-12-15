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
        rownum += 1
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
        # print(cover:'+cover+' title: '+title+' subtitle: '+subtitle+' authors: '+authors+' publishedDate: '+publishedDate+' price: '+price+' previewlink: '+previewlink+'book n°'+str(item_num)+' id: '+itemid+' )
        book_data=[cover,title,subtitle,authors,publishedDate,price,previewlink,rownum]
        matrix_data.append(book_data)
   

#Connect to the webapp database
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="Mysql=123",
database="website_db")

# Count the number of stored books
def rowcountfun():
    mycursor = mydb.cursor()
    sql_countcmd = "SELECT COUNT(id) FROM all_products;"  
    mycursor.execute(sql_countcmd)
    row_count = mycursor.fetchall()
    print("the number of all rows in the database is=" + str(row_count[0][0]))
    mycursor.close()
    return row_count


app = Flask(__name__)

@app.route("/")
def index():    
    req = request.args          # .args for GET method and .form for POST method
    print(req)
    rs = req.get("research_text")
    print(rs)
    #read data from database
    mycursor = mydb.cursor()
    mycursor.execute("select * from all_products")
    bookshelf_db = mycursor.fetchall()
    mycursor.close()    
    if rs == None or rs =="":
        return render_template("index.html", bookshelf=bookshelf_db)
    else:
        research=rs.replace(' ', '+')
        api_fetchdata(research)
        return render_template("index.html", reasearch_tab=matrix_data, bookshelf=bookshelf_db)


@app.route("/add", methods=["POST"])
def add():
    # button_id = request.form["button_id"]
    book_to_add_num = request.form['book_to_add_num']
    print("the book to add is number "+ str(book_to_add_num))
    # print (matrix_data)
    # print(type(book_to_add_num))
    for datarow in matrix_data:
        if datarow[7]==int(book_to_add_num):
            print("bbok find here are its credentials")
            print(datarow)
            add_chosen_book = datarow[0:7]
    # Check if there is a place in database and identify the id to be allocated
    # knowing the nombre of books stored in the database and the already used ids 
    # mycursor = mydb.cursor()    
    # read_id_db = "select id from all_products"
    # mycursor.execute(read_id_db)
    # id_db_rawlt=mycursor.fetchall()
    # mycursor.close()    
    # print(id_db_rawlt)
    # id_db=[]
    # for c in id_db_rawlt:
    #     id_db.append(c[0])
    #     # print(c[0])
    # print(id_db)

    # Count the number of stored books
    row_count = rowcountfun()
    # if there is an empty place it will add the new chosen book the bookshelf,otherwise it will show a message indicating full database
    if row_count[0][0] < 10:
        # possible_db_id=[1,2,3,4,5,6,7,8,9,10]
        # for i in id_db:
        #     possible_db_id.remove(i)
        # print(min(possible_db_id))
        # id=min(possible_db_id)
        add_chosen_book.insert(0,row_count[0][0]+1)      
        # print(add_chosen_book)  
        # print(len(add_chosen_book))
        # add the chosen book data to the database
        mycursor = mydb.cursor()
        sql_addcmd = "INSERT INTO all_products (id,cover,title,subtitle,authors,publishedDate,price,previewlink) VALUES (%s ,%s, %s, %s,%s, %s, %s,%s)"    
        mycursor.execute(sql_addcmd, add_chosen_book)
        mydb.commit()
        mycursor.close()
    else:
        print("db is full, you have consumed your free 10 books saving ;)")

    return redirect(url_for('index'))
  

@app.route("/delete", methods=["POST"])
def delete():
    book_to_delete_id = int(request.form['book_to_delete_id'])
    print("the book to add is number "+ str(book_to_delete_id))
    
    # Count the number of stored books
    row_count = rowcountfun()

    # Delete the chosen book data from the database
    mycursor = mydb.cursor()
    sql = "DELETE FROM all_products  WHERE id=%s"    
    mycursor.execute(sql, (book_to_delete_id,))
    mydb.commit()
    mycursor.close()

    # Update rows id after deleing a row
    mycursor = mydb.cursor()    
    for r in range(book_to_delete_id,row_count[0][0]):
        sql_updatecmd = "UPDATE all_products SET id = '%s' WHERE id =%s;"  
        before_after_id=[r,r+1]
        mycursor.execute(sql_updatecmd, before_after_id)
        mydb.commit()
    mycursor.close()

    return redirect(url_for('index'))





# @app.route("/ajax_reader", methods=["GET","POST"])
# def ajax_reader():
#     if request.method == 'POST': 
#         button_id = int(request.form["button_id"])
#         print("button clicked is number: " + str(button_id))
#         


  
@app.route("/project1")
def project1():
    return redirect("/project2")

@app.route("/project2")
def project2():
    return render_template("project2.html")

@app.route("/project3")
def project3():
    return render_template("project3.html")






if __name__=="__main__":
    # app.run()
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

