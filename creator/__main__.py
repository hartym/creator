import os.path
import re
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
@click.option("--verbose", "-v", is_flag=True, default=False)
def init(project_name, *, verbose=False):
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
            if check.checked:
                continue
            click.echo(click.style(f"Checking {check.name}... ", bold=True), nl=False)
            try:
                check.check()
            except Exception as exc:
                click.secho(f"failed ({exc}).")
                raise

            click.echo(
                click.style("ok.", fg="green")
                + " "
                + check.context[check.name.upper()]
                + " "
                + check.context[check.name.upper() + "_VERSION"]
            )

    for step in steps:
        if step.skip:
            click.echo(f"Skipping {step.title}...")
            continue
        click.secho(f"{step.title.title()}...", bold=True)
        context = {**initial}
        for check in step.checks:
            context.update(check.context)
        for substep in step.steps:
            if isinstance(substep, str):
                cmd = Template(substep).substitute(context)
                click.secho(f" $ {cmd}", fg="blue")
                subprocess.run(cmd, shell=True, check=True, capture_output=not verbose)
            else:
                substep.execute(context)
        if not os.path.exists(initial["PROJECT_NAME"] + "/.git"):
            click.secho(" $ git init", fg="blue")
            subprocess.run(
                "git init",
                shell=True,
                check=True,
                cwd=initial["PROJECT_NAME"],
                capture_output=not verbose,
            )

        click.secho(f' $ git add; git commit -m "{step.title}"', fg="blue")
        subprocess.run("git add .", shell=True, check=True, cwd=initial["PROJECT_NAME"])
        subprocess.run(
            f"git commit -m '{step.title}'",
            shell=True,
            check=True,
            cwd=initial["PROJECT_NAME"],
            capture_output=not verbose,
        )

    click.secho("Done.", bold=True)
    click.echo()
    click.secho(f"You can now run:", bold=True)
    click.echo()
    click.secho(f"  $ cd {project_name}", bold=True, fg="blue")
    click.secho(f"  $ pnpm dev", bold=True, fg="blue")
    click.secho(f"  $ pnpm storybook", bold=True, fg="blue")
    click.echo()
    click.secho("Enjoy.", bold=True)


if __name__ == "__main__":
    init()
