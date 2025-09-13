Boundlexx
=========

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-ruff-000000.svg
     :target: https://github.com/astral-sh/ruff
     :alt: Ruff code style
.. image:: https://img.shields.io/badge/type%20checker-mypy-000000.svg
     :target: https://mypy-lang.org/
     :alt: mypy type checker


:License: MIT

`Changelog <CHANGELOG.rst>`_
----------------------------

Requirements
------------

This project is configured to work with Docker inside of VS Code using the
Remote Containers extension. It is recommend to use those. So make sure you have:

* `Docker Engine and Compose`_. Requires at least
* Docker Buildkit enabled (add `export DOCKER_BUILDKIT=1` to your shell rc or set it manually before running commands)
* `VS Code`_ with the `Remote Containers extension`_.
* MacOSX version of Boundless installed somewhere. You can use `steamcmd`_ to install it via the following command:

   .. code-block:: bash

      steamcmd +@sSteamCmdForcePlatformType macos +login username +force_install_dir /path/to/install +app_update 324510 -beta testing validate +quit

* `Boundless Icon Renderer`_ set up and ran if you want to import item images into Boundlexx

.. _Docker Engine and Compose: https://docs.docker.com/get-docker/
.. _VS Code: https://code.visualstudio.com/
.. _Remote Containers extension: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
.. _steamcmd: https://developer.valvesoftware.com/wiki/SteamCMD
.. _Boundless Icon Renderer: https://forum.playboundless.com/t/icon-renderer/55879

Setup
-----

**Modernization Note:**

This fork is undergoing modernization guided by patterns from `ark-operator <https://github.com/AngellusMortis/ark-operator>`_, including simplified structure, updated dependencies, and improved CI/CD.

**Project Structure:**

- Main app: ``boundlexx/`` (flat, no nesting)
- Configs: Centralized in ``pyproject.toml`` (in progress)
- Scripts: Management tools in root (e.g., setup_*.py)

**Quick Start for Development:**

#. Clone the repo into a meaningful folder structure:

   .. code-block:: bash

      # Example: C:\VSCode\boundlexx-yatesjj\boundlexx\
      # The parent folder name (boundlexx-yatesjj) will be used for container prefixes

#. **Create local environment files:**

   .. code-block:: bash

      # Copy template files to create your local versions  
      cp .env .local.env
      cp docker-compose.override.example.yml docker-compose.override.yml

#. **Set up development container with proper naming:**

   .. code-block:: bash

      # This prefixes all containers with your folder name (e.g., boundlexx-yatesjj-django)
      python setup_development_container_improved.py

#. **Customize your local environment:**
   
   * Edit `docker-compose.override.yml` and update the path to your local Boundless install
   * Edit `.local.env` for any personal environment variables

#. **Open in VS Code:**
   
   * Open the project folder in VS Code
   * Ensure the extension "Remote - Containers" (ms-vscode-remote.remote-containers) is installed
   * You should be prompted to "Reopen in Container". If not, run "Remote-Containers: Reopen in Container" from Command Palette (`Ctrl+Shift+P`)
   * VS Code will build the Docker images and start them up

**Verification:**

Verify your containers are properly named:

.. code-block:: bash

   docker ps --format "table {{.Names}}\t{{.Image}}"

Expected output: `boundlexx-yatesjj-django-1`, `boundlexx-yatesjj-postgres-1`, etc.

**Initial Database Setup:**

#. Before starting the server for the first time, apply all database migrations:

   .. code-block:: bash

      python manage.py migrate

#. Start the Django development server:

   .. code-block:: bash

      python manage.py runserver 0.0.0.0:28000

#. The site will be available at http://127.0.0.1:28000 on your host machine.

**User and Data Setup:**

#. Open http://127.0.0.1:28000 in your web browser. The main site and API will be available, but to access the admin or create users, you must create a Django superuser.
#. In VS Code, open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and select "Tasks: Run Task".
#. Choose "Boundlexx: Manage" from the list. When prompted for the management command, enter `createsuperuser` and follow the prompts to set up your admin user.

#. Again open "Tasks: Run Task" and run "Boundlexx: Ingest Game Data" to import the latest Boundless game data.

#. Run the full ingestion workflow using the VS Code task "Boundlexx: Create Game Objects (Full Ingestion)" which will automatically run skills first, then recipes in the correct order. Alternatively, you can run the individual tasks:

   - "Boundlexx: Create Game Objects (Skills Only)" (must run first)
   - "Boundlexx: Create Game Objects (Recipes Only)" (run after skills)

#. **Important:** Skills must always be imported before recipes. The "Full Ingestion" task handles this automatically, but if running manual commands:

   .. code-block:: bash

      # Import skills first (required!)
      python manage.py create_game_objects --skill

      # Then import recipes
      python manage.py create_game_objects --recipe

#. If you encounter a KeyError or missing data error during this step (e.g., `Skill.DoesNotExist: Decoration Crafting`), ensure you ran the skills import first before attempting recipes.

#. After these steps, your Boundlexx instance should be ready for use and development. To log in as an admin, visit http://127.0.0.1:28000/admin/ and use the credentials you created.

Container Management Scripts
----------------------------

The project includes automated scripts for managing Docker container environments:

**Development Setup:**

.. code-block:: bash

   # Copy template files to create your local versions  
   cp .env .local.env
   cp docker-compose.override.example.yml docker-compose.override.yml
   
   # Set up development container (original ports, folder-prefixed names)
   python setup_development_container_improved.py
   
   # Optional: preview changes first
   python setup_development_container_improved.py --dry-run

**Test Environment Setup:**

.. code-block:: bash

   # Set up test container (Django on port 28001, folder-prefixed names)  
   python setup_test_container.py
   
   # Optional: preview changes first
   python setup_test_container.py --dry-run

**Container Status:**

.. code-block:: bash

   # Check container status
   python container_status.py

**For detailed setup instructions, troubleshooting, and advanced workflows, see:**
`docs/modernization/ENVIRONMENT_SETUP.md`
