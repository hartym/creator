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