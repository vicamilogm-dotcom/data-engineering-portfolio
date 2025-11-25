import click

from . import vm  # importamos el módulo donde estarán los comandos


@click.group()
def cli():
    """Herramientas DE Toolkit (deng) para gestionar la VM."""
    pass


# Registramos los comandos definidos en vm.py
cli.add_command(vm.start)
cli.add_command(vm.stop)
cli.add_command(vm.connect)


if __name__ == "__main__":
    cli()
# Permite ejecutar el CLI directamente desde este archivo