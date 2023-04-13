import typer
import vizelec.pinout
import vizelec.spice

cli = typer.Typer()
cli.add_typer(vizelec.pinout.app, name="pinout")
cli.add_typer(vizelec.spice.app, name="spice")

if __name__ == "__main__":
    cli()
