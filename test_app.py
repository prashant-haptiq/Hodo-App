import pytest 
from app import app , todos

@pytest.fixture 
def client():  #creating a test client for our Hodo app 
    #this sets an environment for each test , for each functionality (check loading of index page, add , check , delete , edit )
    
    #setting the app for testing mode 
    app.config['TESTING'] = True 

    #creating a testing client 
    with app.test_client() as client:
        #before each test reset the todo list 
        todos.clear()

        todos.append({"task": "first task" , "done": False}) 

        yield client #what yield does is set's up something before the test runs , then give that thing to the test function and cleans up after the function run 

        #clearing the list again after the test is done 
        todos.clear()



def test_indexpage_load(client):
    #checking if index page loads correctly 
    response = client.get('/')
    assert response.status_code == 200
    assert b"Tasks Todo" in response.data 


def test_add(client): 
    #checking if item is adding using post request 
    response = client.post('/add' , data={'todo': 'New test task'}) 

    assert response.status_code == 302  #status code == 302 because that means , it successfully avoids resubmitting the form in case user reloads the page 

    #verify new task is added to the list 
    assert len(todos) == 2 

    assert todos[1]['task'] == 'New test task'
    assert todos[1]['done'] == False 



def test_check(client): 
    #checking a todo item as done 
    #the initial task is at index 0 & done is false 
    assert todos[0]['done'] is False 


    #checking the first item 
    response = client.get('/check/0')


    #checking that it avoids redirect 
    assert response.status_code == 302 


    #check if the item is false now 
    assert todos[0]['done'] is True 




def test_delete(client):
    #adding a second item in the todos list , to be deleted 
    todos.append({"task":"Task to be deleted" , "done": False}) 

    #check the length of the list 
    assert len(todos) == 2 


    #this will hit the delete endpoint for the second task (index 1) 
    response = client.get('/delete/1') 

    #checking for the redirect and the list now should contain only 1 item 
    assert response.status_code == 302 
    assert len(todos) == 1 
    assert todos[0]['task'] == 'first task'


def test_edit(client):
    #test the get request to the edit page 
    response = client.get('/edit/0')

    assert response.status_code == 200 

    #updated to check the save button text 
    assert b'Save' in response.data 


    response = client.post('/edit/0' , data={'todo': 'updated task'}) 


    #check for the redirect and the updated task 
    assert response.status_code == 302 
    assert todos[0]['task'] == 'updated task'










