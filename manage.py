import subprocess

import click


@click.group()
def cli():
    pass


@cli.command(context_settings=dict(
    ignore_unknown_options=True
))
@click.argument('uvicorn_args', nargs=-1, type=click.UNPROCESSED)
def runserver(uvicorn_args):
    cmd = [
        'uvicorn', 'app.main:app', '--reload'
    ] + list(uvicorn_args)
    subprocess.run(" ".join(cmd), shell=True, check=True)



if __name__ == '__main__':
    cli()