#!/usr/bin/python3
from ape import project

from scripts.helper_functions import get_account


def deploy() -> project.Election:
    owner, _ = get_account()
    # print(owner.address)
    e = project.Election.deploy(sender=owner, value="0.5 ether")
    return e, owner


def main():
    deploy()
