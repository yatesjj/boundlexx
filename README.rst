Boundlexx
=========

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff6**Verification:**

Verify your containers are properly named:

.. code-block:: bash

   docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"

Expected output for dev: `boundlexx-django-1`, `boundlexx-postgres-1`, etc.
Expected output for test: `boundlexx-test-django-1`, `boundlexx-test-postgres-1`, etc.    :target: https://github.com/pydanny/cookiecutter-django/
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

This fork is undergoing modernization, including a switch to GitHub Container Registry (GHCR) for all image pushes. Dependency upgrades (Python 3.10+, Django 4.2+) are in progress on feature/dependency-upgrade branch to resolve 134 Dependabot vulnerabilities.

**Project Structure:**

- Main app: ``boundlexx/`` (flat, no nesting)
- Configs: Centralized in ``pyproject.toml`` (in progress)
- Scripts: Management tools in root (e.g., setup_containers.py)
- **Unified container setup:** All environment configuration is now handled by the single ``setup_containers.py`` script with simplified naming (boundlexx vs boundlexx-test).


**Quick Start for Development:**

1. Clone the repo into a meaningful folder structure:

   .. code-block:: bash

      # Example: C:\VSCode\boundlexx-yatesjj\boundlexx\
   # The current folder name (boundlexx-yatesjj) will be used for container prefixes

2. **Create local environment files:**

   .. code-block:: bash

      # Copy template files to create your local versions
      cp .env .local.env
      cp docker-compose.override.example.yml docker-compose.override.yml

3. **Set up your environment with unified container script:**

   .. code-block:: bash

      # For development environment (Django on port 28000)
      python setup_containers.py --env dev

      # For test environment (Django on port 28001)
      python setup_containers.py --env test

      # Interactive mode (prompts for environment choice)
      python setup_containers.py

4. **Customize your local environment:**

   * Edit `docker-compose.override.yml` and update the path to your local Boundless install
   * Edit `.local.env` for any personal environment variables

5. **Open in VS Code:**

   * Open the project folder in VS Code
   * Ensure the extension "Remote - Containers" (ms-vscode-remote.remote-containers) is installed
   * You should be prompted to "Reopen in Container". If not, run "Remote-Containers: Reopen in Container" from Command Palette (`Ctrl+Shift+P`)
   * VS Code will build the Docker images and start them up

**Verification:**

Verify your containers are properly named:

.. code-block:: bash

   docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"

Expected output: `boundlexx-yatesjj-django-1`, `boundlexx-yatesjj-postgres-1`, etc.

**Next Steps: Manual/Task-Based Setup**

After the container is set up, you must perform the following steps inside the container or using VS Code tasks:

1. **Install Python requirements (if not already installed by the container):**
   - Use the "Boundlexx: Install Requirements" task or run `pip install -r requirements/dev.txt` inside the container.
2. **Run database migrations:**
   - Use the "Boundlexx: Migrate Database" task or run `python manage.py migrate` inside the container.
   - **If you see "models have changes not yet reflected in a migration":** First run "Boundlexx: Make Migrations" task or `python manage.py makemigrations`, then run migrate again.
3. **Create a Django superuser:**
   - Use the "Boundlexx: Manage" task and enter `createsuperuser`, or run `python manage.py createsuperuser`.
4. **Ingest game data:**
   - Use the "Boundlexx: Ingest Game Data" task or run `python manage.py ingest_game_data 249.4.0`.
5. **Import core data (REQUIRED FIRST):**
   - **Fast setup (recommended)**: Use "Boundlexx: Create Game Objects (Core Data - English Only)" for faster initial setup with English localizations only
   - **Full setup**: Use "Boundlexx: Create Game Objects (Core Data - All Languages)" to import all 5 languages (English, French, German, Italian, Spanish)
6. **Import game objects (in order):**
   - Run "Boundlexx: Create Game Objects (Skills Only)" first, then "Boundlexx: Create Game Objects (Recipes Only)"
   - **For automation**: Use "Boundlexx: Fast Create Game Objects (Core + Skills + Recipes - English Only)" for quick English-only setup, or "Boundlexx: Create Game Objects (Core + Skills + Recipes - All Languages)" for all languages
   - **For complete automation**: Use "Boundlexx: Fast Complete Setup (Ingest + Core + Skills + Recipes - English Only)" for fast setup, or "Boundlexx: Complete Setup (Ingest + Core + Skills + Recipes - All Languages)" for full setup

> **Important:** Choose your setup approach:

**Fast Setup (Recommended for Development):**

   .. code-block:: bash

      # Quick setup with English only (~2,190 strings vs ~10,964)
      python manage.py create_game_objects --core --english-only
      python manage.py create_game_objects --skill
      python manage.py create_game_objects --recipe

      # Add remaining languages later when needed:
      python manage.py create_game_objects --core

**Full Setup (All Languages):**

   .. code-block:: bash

      # Complete setup with all 5 languages
      python manage.py create_game_objects --core
      python manage.py create_game_objects --skill
      python manage.py create_game_objects --recipe

If you encounter a KeyError or missing data error during this step (e.g., `Skill.DoesNotExist: Decoration Crafting`), ensure you ran the skills import first before attempting recipes.

**Django Server Startup:**

- If you are using Docker Compose, the Django server is typically started automatically as a service.
- If you are running locally or in a hybrid setup, you may need to start it manually with:

   .. code-block:: bash

      python manage.py runserver 0.0.0.0:28000

After these steps, your Boundlexx instance should be ready for use and development. To log in as an admin, visit http://127.0.0.1:28000/admin/ and use the credentials you created.

Container Management Scripts
----------------------------

The project includes a unified script for managing Docker container environments:

**Environment Setup:**

.. code-block:: bash

   # Interactive mode - prompts you to choose dev or test
   python setup_containers.py

   # Development environment (boundlexx-*, Django on port 28000)
   python setup_containers.py --env dev

   # Test environment (boundlexx-test-*, Django on port 28001)
   python setup_containers.py --env test

   # Preview without writing files
   python setup_containers.py --env dev --dry-run

**Key Features:**

* **Simple naming:** Development uses `boundlexx` prefix, test uses `boundlexx-test`
* **Fixed ports:** 28000 for dev, 28001 for test (no complex offset calculations)
* **Complete isolation:** Each environment gets its own containers, networks, and volumes
* **Auto-setup:** Copies `.env` to `.local.env` if missing
* **Safe defaults:** Won't overwrite existing files without confirmation

**Container Status:**

.. code-block:: bash

   # Check container status
   python container_status.py

**Note:** The unified setup script (`setup_containers.py`) only generates or updates configuration files. **It does NOT start containers automatically, nor does it print instructions to start them.** The script uses the current folder name for container and network prefixes. You are responsible for starting containers manually (e.g., with `docker-compose up -d`) after reviewing and customizing your configuration files.

**For detailed setup instructions, troubleshooting, and advanced workflows, see:**
`docs/modernization/ENVIRONMENT_SETUP.md`
