# Synchro API
A simple REST API to interact with the Fake API in JSONPlaceholder - Free Fake REST API

## Technical Requirement
**Python Version** used: `3.11.6`

## Libraries Used
 - `psycopg2-binary`:  Python-PostgreSQL Database Adapter (`binary` to avoid building it from source)
 - `python-decouple`: To load sensible information from the `.env` file
 - `requests`: To make requests for JsonPlaceholder Free Fake Rest API
 - `coverage`: To measure the test coverage


## Building and Running the Project
Run the next command to build and run the project
```bash
make initial
```

### Create a Django Superuser
```bash
make createsuperuser
```

## Other useful commands
### Import Data
This command will load the local data with the data from JsonPlaceholder Free Fake Rest API. If there is
some data in the local database, it will do nothing.
```bash
make import_data
```

To reset the `blog` app data and import the data from JsonPlaceholder Free Fake Rest API, run this command
```bash
make import_data_force_reset
```

### Testing
```python
make test  # this command will run the tests
make coverage  # this command will run the tests and will check the test coverage
make report  # this command will show the test coverage
```

## How to use Synchro API

The Synchro API is available from Django /admin/ and API requests.
For the API requests, we need first a bearer token.

### Django /admin/

Go to http://127.0.0.1:8000/admin/
and use your superuser credentials (`make createsuperuser` if you didn't do it above)

In Django Admin, we are able to Read, Create, Update or Delete any information related to our `Blog` App.
We can also create new users and `tokens`.

This `token` part is relevant to use the API. In order to check them or create them, just go to `Tokens`:
  
http://127.0.0.1:8000/admin/authtoken/tokenproxy/
![tokens.png](docs%2Ftokens.png)

If your user or any other user don't have a Token yet, you can create a new one clicking on `Add Token` button.
  
http://127.0.0.1:8000/admin/authtoken/tokenproxy/add/
![new_token.png](docs%2Fnew_token.png)


### API requests

These are some of the `endpoints` available to manipulate de data:

 - List posts:
`GET` http://127.0.0.1:8000/blog/post/
 - Post details:
`GET` http://127.0.0.1:8000/blog/post/{id}/
 - Update post:
`PUT` http://127.0.0.1:8000/blog/post/{id}/
 - Create post:
`POST` http://127.0.0.1:8000/blog/post/
 - Delete post:
`DELETE` http://127.0.0.1:8000/blog/post/{id}/

 - List comments:
`GET` http://127.0.0.1:8000/blog/comment/
 - Post details:
`GET` http://127.0.0.1:8000/blog/comment/{id}/
 - Update comment:
`PUT` http://127.0.0.1:8000/blog/comment/{id}/
 - Create comment:
`POST` http://127.0.0.1:8000/blog/comment/
 - Delete comment:
`DELETE` http://127.0.0.1:8000/blog/comment/{id}/

#### Authorisation
To make a request, remember to use the token mention above

#### Example
For our example, we will use `Postman`.

First of all, copy and paste the token from Django `/admin/` into `Authorization` section.
And select `Bearer Token` as the Authorization `Type`

![postman_authorisation.png](docs%2Fpostman_authorisation.png)

We want to check the details for our post with `id=1`, so the endpoint is: 
http://127.0.0.1:8000/blog/post/1/
And the method is `GET`

Click on `Send` button. It should respond with a Status: 200 OK and a Body similar to this one:
```json
{
    "id": 1,
    "user": 99999942,
    "title": "testv1",
    "body": "testv1 body just for test purposes"
}
```
![get_details.png](docs%2Fget_details.png)


## Synchronisation Approach

To address the synchronisation between the Django system and the "Fake API on JSONPlaceholder", let's consider five
different options. Each approach has its advantages and disadvantages, depending on the 
specific requirements and the context of the project.

### Options to Consider

1. **Option 1 - Comparison and Synchronisation**:
   - **Description**: Download data periodically, compare with the local database, and synchronise differences.
   - **Pros**: Full control over synchronisation; can efficiently handle massive changes.
   - **Cons**: Potentially resource-intensive and complex.

2. **Option 2 - `Updated` Field and POST Command**:
   - **Description**: Mark updated records and synchronise them using a specific command.
   - **Pros**: Simpler and more straightforward; good for minor and controlled changes.
   - **Cons**: Requires manual intervention or a cron job for synchronisation.

3. **Option 3 - Automatic Triggers**:
   - **Description**: Synchronise immediately after each CRUD operation.
   - **Pros**: Keeps the system synchronised in real-time.
   - **Cons**: Can be resource-intensive and complex; risk of errors and overload if there are many CRUD operations.

4. **Option 4 - Queue and Workers**:
   - **Description**: Use a queue system (like Redis with Celery) to handle synchronisation tasks.
   - **Pros**: Efficient handling of heavy loads and activity peaks.
   - **Cons**: Increases system complexity.

5. **Option 5 - Webhooks**:
   - **Description**: If JSONPlaceholder supports webhooks, we can receive notifications of changes and act accordingly.
   - **Pros**: Real-time event-based synchronisation.
   - **Cons**: Depends on the functionality of the external API.

### What could it do in a real example

I would do a combination of **Option 1** and **Option 3** with a layer of **Queue and Workers**:

- Implement periodic synchronisation (Option 1) to ensure all data is up-to-date. This can be less frequent, depending on the nature of the data.
- Use automatic triggers (Option 3) to synchronise changes immediately after CRUD operations, placing synchronisation tasks in a queue to handle 
them efficiently and avoid overloads.
- Ensure to handle exceptions and retries in the queue system to guarantee robustness.

In the end, the choice depends on the nature of the application, the frequency of changes in the data,
and the capabilities of the external API. I would make sure to thoroughly test any approach I choose to ensure that it 
handles all intended use cases and adequately manages errors or interruptions.

### What it really does considering the current project

I finally decided to implement Option 3 to keep it simple.
To trigger it, we only need to Create, Update or Delete with a request.
