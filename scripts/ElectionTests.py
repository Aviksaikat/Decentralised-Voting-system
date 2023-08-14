#!/usr/bin/python3
from ape import *

from scripts.deploy import deploy
from scripts.helper_functions import get_account

election, owner = deploy()
voter1 = get_account(2)


def test_deployment():
    # Check if contract is deployed
    assert election.address is not None


def test_setup_election():
    # set election
    election.setElectionDetails(
        "Jadu Vote",
        "jadu-vote@jadu.com",
        "The Jadu Party",
        "Amra chai Rood",
        "Jaadu Dadau",
        sender=owner,
    )

    # print(election.getElectionDetails()[1])
    assert election.getElectionDetails()[1] == "jadu-vote@jadu.com"


def test_add_candidate():
    # add mominees
    # print(election.getElectionDetails())
    tx = election.addNomineeCandidate("Neel Jadu", "Amra chai Rood", sender=owner)

    # print(election.candidateDetails(1))

    assert tx.status == 1


def test_register_voter():
    # print(voter1.address)

    # register as voter
    election.registerAsVoter("Elon Musk", sender=voter1)
    # print(election.voterDetails(voter1.address)[1])

    assert election.voterDetails(voter1.address)[1] == "Elon Musk"


def test_vote():
    election.verifyVoter(True, voter1.address, sender=owner)

    # print(election.voterDetails(voter1.address))

    assert election.voterDetails(voter1.address).isRegistered == True

    election.vote(1, sender=voter1)

    assert election.voterDetails(voter1.address).hasVoted == True
    assert election.candidateDetails(1).voteCount == 1


def test_end_election():
    election.endElection(sender=owner)

    assert election.getEnd() == True
    assert election.getStart() == False


def main():
    test_deployment()
    test_setup_election()
    test_add_candidate()
    test_register_voter()
    test_vote()
    test_end_election()
