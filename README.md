# Shortlister

Imports a directory and shows information of applicants

## Startup
Accepts an argument (path to your role_folder) when running the script:
```bash
python main.py test_role
``` 

## Learning notes(misc)

### Python Modules

#### Pickling
Pickle: python module    
pickling = converting object into binary files  
unpickling = the inverse operation of pickling, converts binary file back to object

#### Pathlib
pathlib = library for working with file paths
glob = fetches files

#### readchar
module for recording and comparing keypresses

#### universal-startfile
opens pdf files with system's default application
crossplatform version of os.startfile

Shell escaping
(os.system only works with filenames that don't have any spaces or other shell metacharacters in the pathname)


### Design concepts

MVC design:     
separate into Model(data/logic),View(output) and Controller(mediator)
currently controller object contains loads all the data in using functions in model, and using functions in view, it prints out the results.

UML diagram: visualisation of class

