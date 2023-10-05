import click
from ape.cli import network_option, NetworkBoundCommand


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    click.echo(f"You are connected to network '{network}'.")


from ape import accounts, Contract
import alienbase, compound
acct = accounts.load("test")
val = 1
# contract1 = Contract("0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22")
compound.deposit(acct, val)
alienbase.deposit(acct, val)
compound_ror = (compound.withdraw(acct) - val)/val
alienbase_ror = (alienbase.withdraw(acct) - val)/val
