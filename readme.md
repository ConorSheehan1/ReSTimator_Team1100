## How to use
1. Run run.py
2. Open browser and go to localhost:5000

## Input data  
1. 0 values should be explicitly put in files sent to this program. Rows with empty values may be dropped.  
  This occurs in clean_timetable.py for example.

**data_analytics**

1. Run relative_unzipper.py to extract logs
2. Run db_config.py to import all files and load them into the database.

**Testing**

* Tests must be run from the test directory in order to pass.
* Tests take roughly a minute to pass
* Results may vary depending on whether nosetest or pytest is used. For best results use nose.

**Notes**

* Usage, notes, and references are included in the doc string of each file.