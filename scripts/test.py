import click
from ape.cli import network_option, NetworkBoundCommand


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    click.echo(f"You are connected to network '{network}'.")


from ape import accounts, Contract
import alienbase, compound
test = accounts.load("test")
# contract1 = Contract("0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22")
compound_ror = (compound.withdraw(acct) - compound.deposit(acct, x))/compound.deposit(acct, x)
alienbase_ror = (alienbase.withdraw(acct) - alienbase.deposit(acct, x))/alienbase.deposit(acct, x)
