# LIBRARY SYSTEM

## WHAT
This was an assignment in **PYTHON** sofware writing and testing.
We're creating a library system with books and users and the system
takes care of rentals and availability.
GUI is through CLI.

## DATABASE
There's no real database here but my pseudodatabase of library books
is saved as a JSON file in the root dir.

## INSTALLATION
No installation is necessary. Run "new_library_app.py" from your chosen Python environment.

## TESTS
All tests are in their respective folder. All tests done by "Unittest". Be sure to set path 
for testing to correct module if testing from VSC.<br/>
In my system_test I test the whole app and use the mock extension to set patch to not overwrite
database etc.
**UPDATE** library_testsuite.py has been added to be able to run ALL test via CLI, use command<br/>
'python -m unittest -v library_testsuite'


## AUTHOR
Richard Fehling, student at EC Utbildning, MVT22<br/>
richard.fehling@learnet.se