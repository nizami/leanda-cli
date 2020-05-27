import click
import json
import logging
import os
import pkg_resources
import sys

from os import path

from leanda import config, util
from leanda.api import auth, nodes, blobs, category_trees
from leanda.session import session

logger = logging.getLogger('cli')


@click.group(invoke_without_command=True, chain=True)
@click.option('--debug', is_flag=True, help='Enables debug mode.')
@click.option('-v', '--version', is_flag=True, help='Show Leanda CLI version.')
def cli(debug, version):
    """A leanda command line interface."""
    if debug:
        logger.info(f'Debug mode is {"on" if debug else "off"}')
        # logging.getLogger().setLevel(logging.DEBUG)
    if version:
        logger.info(f'v{pkg_resources.require("Leanda")[0].version}')


@cli.command()
def whoami():
    """Check authorization and explore session data."""
    print(util.pretty_json(session.load()))


@cli.command()
@click.option('-u', '--username', help='Username.', required=True, prompt=True)
@click.option('-p', '--password', help='Password.', required=True, prompt=True, hide_input=True)
def login(username, password):
    """Allows to login and store the login info for a Leanda user."""
    auth.login(username, password)


@cli.command()
def logout():
    """Do logout. Session data is removed."""
    session.save({})
    logger.info('Session info was deleted.')


@cli.command()
def pwd():
    """Identify current Leanda working directory."""
    print(nodes.get_location())


@cli.command()
@click.argument('remote_node_id')
def cd(remote_node_id):
    """Change Leanda's current working directory."""
    nodes.set_cwd(remote_node_id)


@cli.command()
@click.option('-s', '--show_id', help='Show id of nodes.', is_flag=True, default=False)
def ls(show_id):
    """Browse remote Leanda folder."""
    nodes.print_cwd_nodes(show_id)


@cli.command()
@click.argument('remote_nodes', nargs=-1)
def rm(remote_nodes):
    """Allows to remove file or folder."""
    for node_name_or_id in remote_nodes:
        nodes.remove(node_name_or_id)

@cli.command()
@click.option('-r', '--remote', help='Remote folder id. Root if ommited.', default=None)
@click.option('-l', '--local', help='Local directories and files (glob pattern) list. Current directory if ommited.', multiple=True, default=None)
def upload(remote, local):
    """Upload local direcory or file list to remote folder."""
    blobs.upload(local, remote)


@cli.command()
@click.option('-r', '--remote', help='Remote folder id. Root if ommited.', default=None)
@click.option('-l', '--local', help='Local directory. Current directory if ommited.', default=None)
def download(remote, local):
    """Download remote folder or file list to local directory."""
    remote = nodes.get_node_by_id(remote or session.cwd)
    local = local or os.getcwd()
    blobs.download_folder(remote, local)


@cli.command()
@click.option('-w', '--watch', help='Watch and sync on changes.',  is_flag=True, default=True)
@click.option('-r', '--remote', help='Remote folder id. Root if ommited.', default=None)
@click.option('-l', '--local', help='Local directory path. Current directory if ommited.', default=None)
def livesync(watch, remote, local):
    """Sync local direcory with remote folder."""
    remote = nodes.get_node_by_id(
        remote or session.cwd) or nodes.get_node_by_id(session.owner)
    local = path.abspath(local or os.getcwd())
    print('Local folder is "%s"' % local)
    print('Remote folder is "%s"' % nodes.get_location(remote))
    blobs.sync(local, remote)




@cli.command()
def categories():
    """List categories"""
    logger.info(util.pretty_json(category_trees.get_categories()))
