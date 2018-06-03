# Pagar.me Conciliator

This application was created to help you understand everything that's happening inside your Pagar.me account. This is made through requesting the objects using the Pagar.me API and saving all the data in a PostgreSQL database (local or remote).

Also, when having all the objects in a database, it's possible to run countless queries to search and analyze data as you wish, avoiding the limitations of the API.

It's possible to use your API key (found in your dashboard) or user credentials.

## Points of attention
- **This application will not perform any operation on your Pagar.me account besides fetching for information** and there are no intentions to do so.

- All the information fetched won't be sent to anywhere outside your computer unless explicitely programmed by the user in the database configuration.

- This tool was developed to be **used by developers who know how to work with programming and databases**. You should not use it if you don't know.

- Do not change the code if you don't know what it will cause. It's your responsability.

## Database
You can either work with a local PostgreSQL database, or use a remote one. To choose between them, you have to change the parameters in the `database-prod.json` file. The `database-test.json` file is used only for the tests and shouldn't be changed.

If using a local database, the default connection parameters are:
```
user=postres
password=postgres
database=postgres
```

## Authentication
To choose between the authentication methods, you have to change the `environment_variables.env` file as following:

### API key
```
AUTHENTICATION_METHOD=api_key
API_KEY=ak_live_123456789abcdefghijklmnopqrstuvwxyz
```

### User credentials
If you want to authenticate with user credentials you have to set the environment that will be used (`test` or `live`):

```
AUTHENTICATION_METHOD=user
ENVIRONMENT=test
```

## Execution

### First run
If is your first time running the application, you will have to build the image and setup the database. You can do this using the following make commands:

```bash
# Make some preparations that are necessary for everything to work
make init
# Build the image
make build-prod
# Create a local PostgreSQL database
make up-database
# If it's the first run, wait about 10 seconds to execute the next command
# so the database has time to start completely
# Apply all the migrations that are not applied yet
make migrate
# Conciliate everything
make conciliate OPERATION=all
```

If not using a local database, you can skip the `make up-database` part, but you have to remember to change the parameters in the `database-prod.json` file (before building the image) and to run the migrations.

You only have to apply the migrations when there's a new one or when you restart the database.

### Conciliate new updates

If you already conciliated the history and only want the things that changed since the last run, use the following command:

```bash
make conciliate OPERATION=new
```

### Other operations
For now these are the only operations implemented
