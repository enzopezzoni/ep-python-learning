from flask import Flask

app = Flask(__name__)

@app.route('/') #the home route
def index():
    return 'hello world'

#create a new route (/hello)
#return 'Hey there!'

@app.route('/hello')
def say_hello():
    return 'Hey there!'

#create a route called classmates
#return a list of you classmates

@app.route('/classmates')
def get_classmates():
    return {"response_code": 200, "data": ['Dan', 'Pavel', 'Enzo', 'Son', 'Priscilla', 'Sanjeev']}

#use a route parameter
@app.route('/<name>')
def say_hello_with_name(name):
    return f'Hey there {name}'

#implement a route that returns the classsmate that matches an id
# /classmates/<id>

@app.route('/classmates/<id>')
def get_classmate(id):
    #create a list of dictionaries, with each name having an i
    names = [{"id": 1, "name": "Dan"},
        {"id": 2, "name": "Enzo"},
        {"id": 3, "name": "Pavel"},
        {"id": 4, "name": "Son"},
        {"id": 5, "name": "Ella"},
        {"id": 6, "name": "Priscilla"}]
    #return the item that matches the id in the route
    for item in names:
        if item['id'] == int(id):
            return item
    return {"response-code": 404}

#make sure that the items in the list are proper json (use double quotes)

if __name__ == '__main__':
    app.run()