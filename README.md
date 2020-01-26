# Certiflo Backend

# Authors
* Victor Trinh - [victortrinh](https://github.com/victortrinh)

# Setup
## Postgres
#### Set your postgres config in the config.py file.

##### Create the migration folder with this command (only do this once)
>python manage.py db init

###### **(only do these 2 step when you add a new models, if you modify existing models, or if the database is empty )
##### 1- To migrate your models changes to the migrations folder
>python manage.py db migrate --message 'initial db migration'

##### 2- To migrate your changes to the database
>python manage.py db upgrade

## Application
### Make sure to install the requirements:
#### With pip:
>pip install -r requirements.txt

### Run the application
>python manage.py run

### Run the tests
>python manage.py test

# Project architecture
## Folder structure

```bash
├── app
│   ├── main
│   │   ├── controller
│   │   ├── model
│   │   ├── service
│   ├── ├── config.py
│   ├── test
├── manage.py
```
* The controller package will contain all of the application endpoint
* The model package will contain the database models
* The service package will contain the business logic of the application

#### Main

# Contributing
If you find a bug or have an idea for an improvement, please first have a look at our [contribution guideline](https://github.com/pldelisle/spectrum/blob/master/CONTRIBUTING.md). Then,
- [X] Create a branch by feature and/or bug fix
- [X] Get the code
- [X] Commit and push
- [X] Create a pull request

# Seed Data
For noob developers using terminal under windows, 
1. Add the following line in ~/.bash_profile: alias jq=<path to repo>/DataSeed/jq.exe
2. Run the following command: source <path to repo>/DataSeed/seedScript
3. To seed all the data on an empty database, run SeedAll <serverUrl> 
4. To seed for a single endpoint, run Seed <serverUrl> <payload file> <post url>
   1. For example, to seed email: Seed localhost:5000 emails.json email/save

Note that the 2020 backlog includes upsert puts, which will allow to create resources with provided ids

# Branch naming

| Instance        | Branch                                             | Description, Instructions, Notes                   |
| --------------- | -------------------------------------------------- | -------------------------------------------------- |
| Stable          | master                                             | Accepts merges from Development and Hotfixes       |
| Development     | dev                                                | Accepts merges from Features / Issues and Hotfixes |
| Features/Issues | feature/[Issue number]-[Short feature description] | Always branch off HEAD or dev                      |
| Hotfix          | fix/[Issue number]-[Short feature description]     | Always branch off Stable                           |

# Commits syntax

##### Adding code:
> \+ Added [Short Description] [Issue Number]

##### Deleting code:
> \- Deleted [Short Description] [Issue Number]

##### Modifying code:
> \* Changed [Short Description] [Issue Number]

##### Merging branches:
> Y Merged [Short Description]
