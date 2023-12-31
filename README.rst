Creator
=======

Bootstrap a vitejs + typescript + react + tailwindcss + emotion + twin macro + ladle project, using minimum templating 
and maximum execution of processes documented by each project.

Why?
::::

Modern js tooling can be quite complex, and it's easy to get lost in the weeds. This project creates an opinionated
empty frontend project with batteries included, so you can get started quickly (tldr: I lost so many time doing this
over and over, bumping into the same caveats that it was time to automate it).

Quickstart
::::::::::

.. code-block:: bash

    brew install pipx
    pipx ensurepath
    pipx run --spec git+https://github.com/hartym/creator.git@main creator <project_name>

After a while, you can run:

.. code-block:: bash

    pnpm dev
    pnpm build
    pnpm preview
    pnpm storybook
    pnpm storybook:build
    pnpm storybook:preview

Enjoy.

To do list
::::::::::

* install and bootstrap react-query (optional ?)
* add a test suite with examples and entrypoints for the target project
* add a test suite for the project itself, to validate it continues running with upstream updates
* push to ci/cd
* add a backend (optional ?)
* add options for non obvious choices (python backend, ...)