https://github.com/AngellusMortis/boundlexx/issues


Update Github Actions #34
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024
Owner
The Github Actions workflows are quite dated, they should be updated quite a bit.

Reference new workflows: https://github.com/AngellusMortis/ark-operator/tree/master/.github/workflows

Simplify/Update Project Structure #33
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
The project structure can be simplified and modernized a bit.

Reference repo: https://github.com/AngellusMortis/ark-operator

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Replace DRF with Django Ninja #32
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Django Rest Framework is the old way of doing REST APIs in Django. However, it very slow. django-ninja is a more modern way of doing so using pydantic.

This is a complex issue because the v1/v2 APIs must not break otherwise downstream tools will break. So, there are two possible approaches:

Attempt to rebuild the v2 API in django-ninja, if it works, then deprecate the v1 API and the remove after a set period of time (probably 6 months).
If reconstructing v2 API is not possible, make a v3 API using django-ninja. Deprecate the v1 and v2 APIs and then remove after a set period of time (probably 6 months).
Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Replace Celery with TaskIQ #31
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Celery is not asyncio native. As a result, it performs badly with a large volume of small tasks. This is very noticeable for updating the shop data from the official game API.

TaskIQ is a new and modern task runner for Python. TaskIQ should be setup and then the Celery task be gradually migrated to using it.

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Update requirements management #30
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Boundlexx currently uses pip + pip-tools and multiple separate requirements files.

The requirements should be moved inside of the pyproject.toml and the requirement update process be simplified and only use uv

Example pyproject.yoml

Example update script: https://github.com/AngellusMortis/ark-operator/blob/master/.bin/update-requirements

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Update Linters #29
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Boundlexx currently uses flake8, pycodestyle, mypy, pylint, isort and black. These should all be replaced with just mypy and ruff.

Ruff should first be added a requirement + a sensible default config (exmaple). Then issues should be fixed incrementally. Once all of the ruff issues are fixed, it can be enabled by default for CI and the old ones can be removed.

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Raise Code Coverage #28
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Code Coverage for Boundlexx is currently pretty low. This makes it difficult to make updates with confidence as an update could break multiple things.

Coverage should be raised gradually to at least 85%.

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Remove Huey #27
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Huey was an experiment in getting rid of Celery. It did not pan out. All of the existing Huey tasks should be converted back to Celery tasks.

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Move setup.cfg into pyproject.toml #26
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
The pyproject.toml is now the preferred way of doing tool configuration. All of the configs in setup.cfg should be moved to the pyproject.toml.

Example pyproject.toml

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Rename container images #25
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Containers should be renamed to boundlexx-django and boundlexx-django-dev (kebab casing).

Activity

AngellusMortis
added
modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Fix Steam Login #24
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Steam login is required to use the internal game APIs for Boundless. The method to login recently broken and now planet data can no longer be fetched, meaning no new data for new Exos or Sovereigns.

The entrypoint for logging into steam can be found at here.

Since it requires authenticating the user with the game as well, it requires a session ticket. The only way previously figured out how to generate these was to use a Node.js library. The script for that can be found here.

Ideally, the new method should be converted to using a Python native solution, but if Node.js is still required, that is fine.

The end goal of this ticket is that the prompt_steam_guard management command should function again.

Activity

AngellusMortis
added
bug
Something isn't working

fix-boundlexx
Issue must be completed to bring Boundlexx into a working state
 on Dec 25, 2024
Redlotus99
Redlotus99 commented on Jan 17
Redlotus99
on Jan 17
Ive been trying to look at this and sort of been playing around with this in order to try and get this fixed. My main problem is trying to test it out as Im not sure how to do that.

AngellusMortis
AngellusMortis commented on Jan 17
AngellusMortis
on Jan 17 · edited by AngellusMortis
Owner
Author
https://docs.djangoproject.com/en/3.2/intro/tutorial01/
https://docs.djangoproject.com/en/3.2/ref/django-admin/

The end goal of this ticket is that the prompt_steam_guard management command should function again.

https://github.com/AngellusMortis/boundlexx/blob/master/boundlexx/boundless/game/client.py#L256-L268
https://github.com/AngellusMortis/boundlexx/blob/master/boundlexx/boundless/management/commands/prompt_steam_guard.py

Redlotus99
Redlotus99 commented on Jan 18
Redlotus99
on Jan 18 · edited by Redlotus99
I understand what needs to change and even have made changes, I would like to test my changes for the Steam login, but didn't see how I could test that. I've been able to get Boundlexx running locally, but not sure exactly how I would test the Steam changes.

When trying to browse to port 8000 I don't have anything running it seems. I can go to port 28000 and see Boundlexx though.

Redlotus99
Redlotus99 commented on Feb 2
Redlotus99
on Feb 2
Go to http://127.0.0.1:8000/ in your Web browser and click "Sign In". Then sign in with Discord or Github

Going to http://localhost:28000 does open Boundlexx, but I get no "Sign In".

Once I have the site running, I do the steps below, but I have to run Boundlexx: Create Superuser then:

Back in VS Code, run the command "Tasks: Run Task" and then "Boundlexx: Make Superuser".
Enter the username for your user when prompted.
Repeat "Tasks: Run Task" for the "Boundlexx: Ingest Game Data" and "Boundlexx: Create Game Objects" tasks.

I run Ingest Game Data which completed but when running Create Game Objects it fails when creating skills. @AngellusMortis

AngellusMortis
AngellusMortis commented on Feb 4
AngellusMortis
on Feb 4
Owner
Author
Getting the ingest data and game objects should not be needed for fixing steam. You do not even need to run the Django Web server for it all to work.

(you can look up your own guides/resources for learning, I am just linking official docs for each)

You should understand the basis of how containers / Docker / Docker Compose works: https://docs.docker.com/get-started/
Understand how Django works (and of course Python by extension): https://docs.djangoproject.com/en/3.2/intro/tutorial01/
you should understand how Django settings work
you should understand how to run migrations for databases
you should understand what Management commands are and how to run them
Probably need to know a some Node.js to update the authentication script
Once you have that, you need to populate the settings with your Boundless and Steam username/passwords. There should be envs you can provide in the .env file (STEAM_USERNAMES and STEAM_PASSWORDS). Then you run the management command for prompt_steam_guard management command to test. If that management command and it succeeds, everything else should succeed.

If you get all working, you should fork the repo and make a PR

Redlotus99
Redlotus99 commented on Feb 5
Redlotus99
on Feb 5 · edited by Redlotus99
I have the login working successfully, but it does prompt in the terminal for the 2FA, which I can then use via Steam Mobile App to authenticate with and connect. Is this correct, or does it need to grab this information automatically from Steam?

If so, I think the only way to do that is via a secret key, but that is not a viable solution.

Update to Django 4.2+ #23
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Django 3.2 is end of lifed. The project should be updated to at least Django 4.2 (ideally 5.2).

Django's docs on upgrading: https://docs.djangoproject.com/en/5.1/howto/upgrade-version/

As part of this, you may also need to update redis and postgres/timescaledb

Activity

AngellusMortis
added
fix-boundlexx
Issue must be completed to bring Boundlexx into a working state

modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Update to Python 3.10+ #22
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
Python 3.9 is soon to be end of lifed. The project should be updated to at least Python 3.10 (ideally 3.12).

Activity

AngellusMortis
added
fix-boundlexx
Issue must be completed to bring Boundlexx into a working state

modernize
Update Boundlexx to latest standards
 on Dec 25, 2024

 Ensure Containers Build in GHA #21
Open
@AngellusMortis
Description
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
For Boundlexx to be deployed, the containers must automatically be built by Gihtub Actions when a commit is pushed to the default branch.

Optional: all of the existing linters should also pass.

Activity

AngellusMortis
added
fix-boundlexx
Issue must be completed to bring Boundlexx into a working state
 on Dec 25, 2024
