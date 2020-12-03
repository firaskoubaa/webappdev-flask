from flask import Flask, render_template, request, url_for
import requests

#Fetching data using Google Books API
# research=input('Type the name of the book please: ')
research='good'
research=research.replace(' ', '+')
matrix_data=[]
def api_fetchdata(subject):
    rq = requests.get('https://www.googleapis.com/books/v1/volumes?q='+subject)
    response = rq.json()
    all_items=response['items']
 
    for item_num in range(len(all_items)):
        itemid=all_items[item_num]['id']
        cover=all_items[item_num]['volumeInfo']['imageLinks']['thumbnail']
        title=all_items[item_num]['volumeInfo']['title']

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

        # print('book n°'+str(item_num+1)+' id: '+itemid+' cover:'+cover+' title: '+title+' subtitle: '+subtitle+' authors: '+authors+' publishedDate: '+publishedDate+' price: '+price)
        book_data=[cover,title,subtitle,authors,publishedDate,price]
        matrix_data.append(book_data)
   
api_fetchdata(research)
# print(matrix_data)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", students=matrix_data)

@app.route("/project1")
def project1():
    return render_template("project1.html")

@app.route("/project2")
def project2():
    return render_template("project2.html")

@app.route("/project3")
def project3():
    return render_template("project3.html")


# @app.route("/prject1_journey")
# def prject1_journey():
#     vnapp=request.args.get("visitor")
#     return render_template("prject1_journey.html", VisNam=vnapp)


if __name__=="__main__":
    # app.run()
    app.run(debug=True)