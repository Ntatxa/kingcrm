#!/usr/bin/env python

import os
import click
from werkzeug.serving import run_simple

from app import engine, api, Base

import ssl
from wsgiref import simple_server


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    
    #print(os.environ)
    
    run_simple("192.168.0.210", 4000, api, use_debugger=True, use_reloader=True)
    #print(os.path)
    #run_simple("192.168.0.210", 4000, api, use_debugger=True, use_reloader=True, ssl_context='adhoc')
 
@cli.command()
def runserver2():
    httpd = simple_server.make_server("192.168.0.210", 4000, api)
    httpd.socket = ssl.wrap_socket(
        httpd.socket, server_side=True,
        certfile='cert.pem',
        keyfile='key.pem'
    )
    httpd.serve_forever()


@cli.command()
def initdb():
    if os.path.isfile("data.sqlite"):
        click.echo(
            "You have database file in the current directory"
            "to createad it run dropdb, initdb commands respectively."
        )
    else:
        click.echo("initializing database...")
        Base.metadata.create_all(engine)


@cli.command()
def dropdb():
    filename = "data.sqlite"
    if os.path.isfile(filename):
        os.remove(filename)
        click.echo("dropping database...")
    else:
        click.echo("The database doesn't exists")


if __name__ == "__main__":
    cli()
    