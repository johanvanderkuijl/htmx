from flask import Flask, redirect, render_template, request
import time
from pydantic import BaseModel, Field
app = Flask(__name__)


class User(BaseModel):
    id: int
    name: str
    age: int
    hobbies: str
    remarks: str | None = Field(None, description="Some remarks")


class UserStore(BaseModel):
    users: list[User] = [] 

    def add(self, name: str, age: int, hobbies: str):
        new_user=User(
            id=len(self.users) + 1,
            name=name,
            age=age,
            hobbies=hobbies
        )        
        self.users.append(new_user)
        return new_user
    
   
    def remove(self, user_id: int) -> bool:
        # Find and remove the first matching user by ID
        for i, user in enumerate(self.users):
            if user.id == user_id:
                self.users.pop(i)  # Safe: pop by index during enumeration
                return True
        return False  # Not found

persons = [
    User(
        id=1,name="Jim", age=42, hobbies="kitesurfing", remarks="some remarks here"
    ),
    User(
        id=2,name="Margareth", age=38, hobbies="music"
    ),
    User(
        id=3,name="Brian", age=18, hobbies="space"
    ),
    User(
        id=4,name="Erin", age=16, hobbies="languages"
    ),
]


@app.route('/users/<int:user_id>', methods=["DELETE"])
def users(user_id):
    res = userstore.remove(user_id) 
    return ""

@app.route('/')
def index():
    return render_template(
        'index.html', persons=userstore.users)

@app.route('/add_user', methods=["POST"])
def add_user():

    name=request.form["name"]
    age=int(request.form["age"])
    hobbies=request.form["hobbies"]

    userstore.add(name, age, hobbies)

    import time
    from random import randint
    # time.sleep(randint(0,2))
    
    # print(request.headers)
    if request.headers.get('Hx-Request'):
        return render_template('users.html', persons=userstore.users)
    return redirect('/')

@app.route("/search", methods=["POST"])
def search():
    q = request.form.get("search")

    users = [x for x in userstore.users if q in x.name.lower()]

    return render_template('users.html', persons=users)

if __name__ == '__main__':
    userstore = UserStore()

    for user in persons:
        userstore.add(user.name, user.age, user.hobbies)
    
    app.run(debug=True)