from flask import Flask
from flask_pymongo import PyMongo
from flask import Flask,render_template,url_for,request,redirect

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/MoviesDB"
mongo = PyMongo(app)

@app.route('/')
def my_home():
	return render_template('index.html')

#Routing pages dynamically
@app.route('/<string:page_name>')
def html_page(page_name):
	return render_template(page_name)

#Displaying all the data
@app.route("/show_data")
def show_data():
    movies_names = mongo.db.Movies.find({},{"_id":0,"name":1})
    mn=list(movies_names)
    output1=[]
    for i in range(len(mn)):
    	for key in mn[i]:
    		output1.append(mn[i][key])

    image_link= mongo.db.Movies.find({},{"_id":0,"img":1})
    img=list(image_link)
    output2=[]
    for i in range(len(img)):
    	for key in img[i]:
    		output2.append(img[i][key]) 

    movie_summary= mongo.db.Movies.find({},{"_id":0,"summary":1})
    ms=list(movie_summary)
    output3=[]
    for i in range(len(ms)):
    	for key in ms[i]:
    		output3.append(ms[i][key])
    return render_template("index.html",movies=output1,image=output2,summary=output3)


#Inserting Data into the Database
@app.route('/insert_data', methods=['POST'])
def insert_data():
	if request.method=='POST':
		movie_name=request.form['mname']
		img_link=request.form['imglink']
		summary=request.form['summary']
		mongo.db.Movies.insert({'name':movie_name,'img':img_link,'summary':summary})
		msg="Inserted Successfully"
		return render_template("index.html",message=msg)
	else:
		return 'something is wrong'

#Updating Data into the Database
@app.route('/update',methods=['POST'])
def update_data():
	if request.method=='POST':
		movie_name=request.form['mname']
		new_name=request.form['new_name']
		img_link=request.form['imglink']
		summary=request.form['summary']
			
		myquery = { "name": movie_name }
		new_movie_name ={ "$set": { "name": new_name } }
		new_img_link={"$set":{"img":img_link}}
		new_summary={"$set":{"summary":summary}}
		
		mongo.db.Movies.update_one(myquery,new_img_link)
		mongo.db.Movies.update_one(myquery,new_summary)
		mongo.db.Movies.update_one(myquery,new_movie_name)
		msg="Updated Successfully into the database"
		return render_template("index.html",message=msg)
	else:
		return 'something is wrong'


#Deleting Data by taking MovieName as input
@app.route('/delete',methods=['POST'])
def delete_data():
	if request.method=='POST':
		movie_name=request.form['mname']
		myquery = { "name": movie_name }
		mongo.db.Movies.delete_one(myquery)
		msg="Deleted Successfully"
		return render_template("index.html",message=msg)
	else:
		return 'something is wrong'
    