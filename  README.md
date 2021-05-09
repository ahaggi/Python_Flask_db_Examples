1- Download and install py https://www.python.org/download

2- Confirm that [installationpath]\PythonXX and [installationpath]PythonXX\Scripts; is part of the path.

3- Confirm that pip is installed `pip help`

4- Install virtualenv `pip install virtualenv`

5- Install virtualenvwrapper-win `pip install virtualenvwrapper-win`


Setup a Virtual Environemt:

    1- Make a Virtual Environemt: 
    This will create a folder (Virtual Environemt <venv_name> in %USERPROFILE%\Env) with python.exe, pip, and setuptools all ready to go in its own little environment. 
    `mkvirtualenv <venv_name>`

    2- run the flwg to activate the newly created virtual environemt 
    `%USERPROFILE%\Env\ <venv_name> \Scripts\activate`
    
    BUT
        In our case we changed the virtual enviroment path for this project, so activate it sa:
        `E:\WindowsUserProfile\Desktop\prosjekter\ProjPy\Envs\venv1\Scripts\activate`
    
        NOTE: in case if you're using "Powershell", you may encouter the fleg err:
            "...Scripts\activate.ps1 is not digitally signed. You cannot run this script on the current system..."
            In that case change the "ExecutionPolicy" as follows:
            `Set-ExecutionPolicy Unrestricted -Scope Process`

    if you encounter a problem try running the flwg ` Set-ExecutionPolicy Unrestricted -Scope Process ` and try step2 again.

    3- run
    `workon <venv_name>`

    4- Connect a project with the virtual environemt
    `setprojectdir "<project_path>" `

    Anything we install now will be specific to this project. And available to the projects we connect to the virtual environemt <venv_name>.

Install project dependency:
    Make sure you are connected to <venv_name>, the cmd prompt should look like " ( <venv_name> ) c:\something " , and install the dependencies declared at the "requirements.txt". 
    "requirements.txt" contains a list of items to be installed using pip install like so:
    `py -m pip install -r requirements.txt`


This project is structured as "Flask’s Application Factory"
    https://hackersandslackers.com/flask-application-factory

    
Run the project:
`python <PROJECT_NAME>\wsgi.py`


