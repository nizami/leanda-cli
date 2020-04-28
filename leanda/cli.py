import os
import sys
import click
import pkg_resources
import json

from leanda.api import auth, nodes, blobs
from leanda import config
from leanda.session import session


@click.group(invoke_without_command=True, chain=True)
@click.option('--debug', is_flag=True, help='Enables debug mode.')
@click.option('-v', '--version', is_flag=True, help='Show Leanda CLI version.')
@click.option('--dev/--local', default=True, help='Show Leanda CLI version.')
def cli(debug, version, dev):
    """A leanda command line interface."""
    if debug:
        click.echo(f'Debug mode is {"on" if debug else "off"}')
    if version:
        click.echo(f'v{pkg_resources.require("Leanda")[0].version}')
    if dev:
        config.config = config.dev_config
    else:
        config.config = config.local_config


@cli.command()
@click.option('-u', '--username', help='Username.', required=True, prompt=True)
@click.option('-p', '--password', help='Password.', required=True, prompt=True, hide_input=True)
def login(username, password):
    """Allows to login and store the login info for a Leanda user."""
    auth.login(username, password)


@cli.command()
@click.argument('remote_node_id')
def cd(remote_node_id):
    nodes.set_cwd(remote_node_id)


@cli.command()
def pwd():
    print(nodes.get_location())


@cli.command()
@click.option('-s', '--show_id', help='Show id of nodes.', is_flag=True, default=False)
def ls(show_id):
    nodes.print_cwd_nodes(show_id)


@cli.command()
@click.argument('remote_nodes', nargs=-1)
def rm(remote_nodes):
    for node_name_or_id in remote_nodes:
        nodes.remove(node_name_or_id)


@cli.command()
def categories():
    """List categories"""
    # nodes.create_folder('new wwww')
    # blobs.upload_files(
    #     [
    #         '/Users/nizami/Downloads/**/*.dmg',
    #         '/Users/nizami/Downloads/**/*.dmg',
    #         '/Users/nizami/Downloads/untitled folder/mm copy 259',
    #         '/Users/nizami/Downloads/untitled folder/mm copy 258',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/untitled folder/mm copy 258',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/untitled folder/mm copy 258',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/Invoice-0007.pdf',
    #         '/Users/nizami/Downloads/Insomnia-7.1.1.dmg',
    #         '/Users/nizami/Downloads/novabench.dmg'
    #     ])
    # print(nodes.create_folder('new folder'))
    # print(json.dumps(api.get_all_remote_folders(), indent=4))

    # blobs.upload_folders(['/Users/nizami/Downloads/test'])
    # blobs.upload_files(
    #     ['/Users/nizami/Documents/w/arqisoft/leanda/leanda-cli-new/Invoice-0007.pdf'], )
    # blobs.download_folder('daeda3e6-06b4-49b0-8527-287ade906229')
    blobs.remove('00170000-ac12-0242-2201-08d7e9e4f008')


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
@click.option('-w', '--watch', help='Watch and sync on changes.',  is_flag=True, default=False)
@click.option('-r', '--remote', help='Remote folder id. Root if ommited.', default=None)
@click.option('-l', '--local', help='Local directory path. Current directory if ommited.', default=None)
def sync(watch, remote, local):
    """Sync local direcory with remote folder."""
    remote = nodes.get_node_by_id(remote or session.cwd)
    local = local or os.getcwd()
    blobs.sync(local, remote)
