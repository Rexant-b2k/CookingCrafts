## Postman collection for checking API (TDD)

The file `cookingcrafts_ru.postman_collection.json` contains postman collection - the set of prepared requests to test the API.

## Preparing Django project for launching collection:
1. Check that virtual environment is created and activated, all dependencies are installed.
2. For local API check set in `.env` file or directly in `settings.py` the value `DEBUG = True` to use local SQLite3 DB.
3. Apply migrations; Create in DB at least 2 ingredients and 3 tags. It is possible to use management commands (python manage.py initial_ingredients && python manage.py initial_tags)*
4. Start DEV server.

*After preparing the project, make copy (backup) of the DB file `db.sqlite3`: 
It could be helpful in a case of failure.*

## Uploading collection to the Postman:

1. Launch the Postman.
2. In main menu press `File` -> `Import`.
3. In the pop-up window you will be asked to drag and drop collection file or choose file via file manager.
Upload the file `cookingcrafts_ru.postman_collection.json` into the Postman.

## Collection launch:

1. After previoous steps, in the left side of the Postman window, in the `Collections` tab the imported collection appears.
Place the coursor, press `...` near the name of collection and in choose `Run collection` from dropping list. In the middle part of scrren there will list of requests from collection, and in the right side - menu for setting launch parameters.
2. In the right menu switch on the `Persist responses for a session` function - it will provide the list of API responses adter launching the collection.
3. Press the button `Run <collection name>`.
4. You will see the result of launcing tests and collection. Failed tests could be filtered by pressing tab `Failed`.
To check the details of request and recieved response, click on test.

## Relaunch the collection:
1. Move to the folder `postman_collection` in the root of the project.
2. While active virtual environment, launch the script for cleaning database fro, objects which were created during preivous postman launch: `bash clear_db.sh`.  
During script execution all users and objects that were created during last collection launch will be removed (in a case of correct setting `on_delete` in the project models).
  
In a case of cleaning failure, use the backup `db.sqlite3`: replace the DB file by file from backup. 
It is also possible ro remove DB file and repeat steps from block _Preparing Django project for launching collection_.
