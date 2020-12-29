from flask import Flask, render_template, request, url_for, redirect
import requests
import mysql.connector

# Read and fetch data using Google Books API
def api_fetchdata(subject):
    global matrix_data
    matrix_data=[]
    rownum=0
    rq = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + subject)     # gives the respons type <Response [200]>
    response = rq.json()                                                              # extracts the json data
    try:
        all_items = response['items']     # extracts value of the key "items" which is a dictionnary by itself
    
        for item_num in range(len(all_items)):
            rownum += 1
            # Extract data from dictionary (json response)
            itemid = all_items[item_num]['id']
            title = all_items[item_num]['volumeInfo']['title']

            try:
                cover = all_items[item_num]['volumeInfo']['imageLinks']['thumbnail']
            except:
                cover = "/static/img/book_cover_backup.png"

            try:
                subtitle = all_items[item_num]['volumeInfo']['subtitle']
            except:
                subtitle = ''

            try:
                pre_authors = all_items[item_num]['volumeInfo']['authors']
                authors = pre_authors[0] 
                if len(pre_authors) > 1:
                    for author_num in range(len(pre_authors) - 1):
                        authors = authors + ', ' + pre_authors[author_num + 1]
            except:
                authors = ""

            try:
                publishedDate = all_items[item_num]['volumeInfo']['publishedDate'][:10]
            except:
                publishedDate = ""

            if all_items[item_num]['saleInfo']['saleability'] == 'FOR_SALE':
                price = str(all_items[item_num]['saleInfo']['retailPrice']['amount'])
            else:
                price = all_items[item_num]['saleInfo']['saleability']

            previewlink = "https://books.google.com/books?id=" + itemid

            book_data = [cover,title,subtitle,authors,publishedDate,price,previewlink,rownum]
            matrix_data.append(book_data)
    except:
        print("There is no book registered in the database of Google Books with the name '" + subject + "'")
   

#Connect to the webapp database
mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "Mysql=123",
database = "website_db")

# Count the number of stored books in the Database
def rowcountfun():
    mycursor = mydb.cursor()
    sql_countcmd = "SELECT COUNT(id) FROM all_products;"  
    mycursor.execute(sql_countcmd)
    row_count = mycursor.fetchall()
    print("the number of all rows in the database is=" + str(row_count[0][0]))
    mycursor.close()
    return row_count

# Limit the maximum number of items to strore in the bookshelf (Databsae)
maxnum_items_bookshelf = 10 

app = Flask(__name__)

# Home page
@app.route("/")
def index():    
    return render_template("index.html")

# Bookshelf application
@app.route("/bookshelf_app")
def bookshelf_app():
    req = request.args          # .args for GET method and .form for POST method
    rs = req.get("searched_keywords")
    print(rs)
    #read data from database
    mycursor = mydb.cursor()
    mycursor.execute("select * from all_products")
    bookshelf_db = mycursor.fetchall()
    mycursor.close()    
    if rs == None or rs == "":
        return render_template("bookshelf_app.html", bookshelf = bookshelf_db)
    else:
        research=rs.replace(' ', '+')       # In case the user runs a search with two words or more 
        api_fetchdata(research)
        print(matrix_data)
        if matrix_data == []:                # In case the application doesn't find any book with the searched name
            return render_template("bookshelf_app.html", bookshelf = bookshelf_db, searched_book_name = rs, search_status = "not found")
        else:                                # In case everything works fine 
            return render_template("bookshelf_app.html", reasearch_tab = matrix_data, bookshelf = bookshelf_db, search_status = "found")


# Adding the chosen book to the Databse 
@app.route("/add", methods = ["POST"])
def add():
    book_to_add_id = request.form['book_to_add_id']         # Identify the id of the book to be added
    print("the book to add is number " + str(book_to_add_id))

    # Copy data from the chosen book 
    for datarow in matrix_data:
        if datarow[7] == int(book_to_add_id):
            print(datarow)
            add_chosen_book = datarow[0:7]

    # Count the number of stored books
    row_count = rowcountfun()

    if row_count[0][0] < maxnum_items_bookshelf:        # Verifying that there is an availble space in the Database before adding a new book to it
        add_chosen_book.insert(0, row_count[0][0] + 1)      
        print(add_chosen_book)  

        #  SQL instructions to add the chosen book data to the database
        mycursor = mydb.cursor()
        sql_addcmd = "INSERT INTO all_products (id,cover,title,subtitle,authors,publishedDate,price,previewlink) VALUES (%s ,%s, %s, %s,%s, %s, %s,%s)"    # Place holder to protect from SQL Injections
        mycursor.execute(sql_addcmd, add_chosen_book)
        mydb.commit()
        mycursor.close()
    else:                                   # in case the Database is totally full
        print("db is full, you have consumed your free 10 books saving ;)")

    return redirect(url_for('bookshelf_app'))
  
# Deleting the selected book from the Databse 
@app.route("/delete", methods = ["POST"])
def delete():
    book_to_delete_id = int(request.form['book_to_delete_id'])
    print("the book to add is number " + str(book_to_delete_id))
    
    # Count the number of stored books
    row_count = rowcountfun()

    # SQL instructions to delete the chosen book data from the database
    mycursor = mydb.cursor()
    sql = "DELETE FROM all_products  WHERE id = %s"     # Place holder to protect from SQL Injections
    mycursor.execute(sql, (book_to_delete_id,))
    mydb.commit()
    mycursor.close()

    # SQL instructions to update the id of books in the database after deleing a data row
    mycursor = mydb.cursor()    
    for id_to_upd in range(book_to_delete_id, row_count[0][0]):
        sql_updatecmd = "UPDATE all_products SET id = '%s' WHERE id = %s;"      # Place holder to protect from SQL Injections
        before_after_id=[id_to_upd, id_to_upd + 1]
        mycursor.execute(sql_updatecmd, before_after_id)
        mydb.commit()
    mycursor.close()

    return redirect(url_for('bookshelf_app'))



if __name__ == "__main__":
    app.run(debug = True)