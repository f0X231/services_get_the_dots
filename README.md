- Virtual env
pip install virtualenv : install virtualenv 
$ python<version> -m venv <virtual-environment-name> : Creating a new virtualenv
$ virtualenv <NEWVIRTUALENV> : Creating a new virtualenv
$ source <NEWVIRTUALENV>/bin/activate : Activating that new virtualenv

- Requirements.txt
$ pip install -r requirements.txt --no-index --find-links <URL>
- --no-index - Ignore package index
- -f, --find-links <URL> - If <URL> is a URL or a path to an HTML file, then parse for links to archives. If <URL> is a local path or a file:// URL that's a directory, then look for archives in the directory listing.
$ pip freeze > requirements.txt : craete requirement.txt
