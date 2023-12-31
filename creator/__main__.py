import re
import os.path
import subprocess
from string import Template
import click

from creator.scripts.generate_vite_project import generate_vite_project
from creator.scripts.install_ladle import install_ladle
from creator.scripts.install_tailwindcss import install_tailwindcss
from creator.scripts.install_twin_macro_with_emotion import (
    install_twin_macro_with_emotion,
)

steps = [
    generate_vite_project,
    install_tailwindcss,
    install_twin_macro_with_emotion,
    install_ladle,
]


@click.command()
@click.argument("project_name")
def init(project_name):
    initial = {
        "PROJECT_NAME": project_name,
    }
    if not re.match(r"^[a-z0-9_-]+$", project_name):
        click.echo(
            f"Invalid project name «{project_name}». Project names must contains alphanumeric, dashes and underscores "
            f"only. Please choose a different name."
        )
        return

    click.echo(f"Creating project {project_name}.")

    if os.path.exists(project_name):
        click.echo(f"Directory {project_name} already exists.")
        if click.confirm("Do you want to erase it?"):
            subprocess.run(f"rm -rf {project_name}", shell=True, check=True)
        else:
            return

    for step in steps:
        for check in step.checks:
            click.echo(f"Checking {check.name}...")
            check.check()

    for step in steps:
        if step.skip:
            click.echo(f"Skipping {step.title}...")
            continue
        click.echo(f"Executing {step.title}...")
        context = {**initial}
        for check in step.checks:
            context.update(check.context)
        for substep in step.steps:
            if isinstance(substep, str):
                cmd = Template(substep).substitute(context)
                click.echo(f" $ {cmd}")
                subprocess.run(cmd, shell=True, check=True)
            else:
                substep.execute(context)
        if not os.path.exists(initial["PROJECT_NAME"] + "/.git"):
            click.echo("Initializing git repository...")
            subprocess.run(
                "git init", shell=True, check=True, cwd=initial["PROJECT_NAME"]
            )

        click.echo(f"Committing changes for «{step.title}»...")
        subprocess.run("git add .", shell=True, check=True, cwd=initial["PROJECT_NAME"])
        subprocess.run(
            f"git commit -m '{step.title}'",
            shell=True,
            check=True,
            cwd=initial["PROJECT_NAME"],
        )


if __name__ == "__main__":
    init()
