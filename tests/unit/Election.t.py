#!/usr/bin/python3
import ape
import pytest


def test_deployment(setup_election):
    election, owner = setup_election
    assert election.address is not None


def test_setup_election(setup_election):
    election, owner = setup_election
    election.setElectionDetails(
        "Jadu Vote",
        "jadu-vote@jadu.com",
        "The Jadu Party",
        "Amra chai Rood",
        "Jaadu Dadau",
        sender=owner,
    )

    assert election.getElectionDetails()[1] == "jadu-vote@jadu.com"


def test_add_candidate(setup_election):
    election, owner = setup_election
    tx = election.addNomineeCandidate("Neel Jadu", "Amra chai Rood", sender=owner)

    assert tx.status == 1


def test_register_voter(setup_election, getVoter):
    election, owner = setup_election
    voter1 = getVoter
    election.registerAsVoter("Elon Musk", sender=voter1)

    assert election.voterDetails(voter1.address)[1] == "Elon Musk"


def test_fail_election_has_not_yet_started(setup_election, getVoter):
    election, owner = setup_election
    voter1 = getVoter

    election.registerAsVoter("Elon Musk", sender=voter1)
    election.verifyVoter(True, voter1.address, sender=owner)

    with pytest.raises(
        ape.exceptions.ContractLogicError, match="Election has not started"
    ):
        election.vote(1, sender=voter1)


def test_fail_vote_without_verification(
    setup_election, getVoter, setup_election_details
):

    _, owner = setup_election
    voter1 = getVoter

    election = setup_election_details
    election.registerAsVoter("Elon Musk", sender=voter1)

    assert election.voterDetails(voter1.address).isRegistered == True

    with pytest.raises(
        ape.exceptions.ContractLogicError, match="You are not verified to vote"
    ):
        election.vote(1, sender=voter1)


def test_vote_with_verification(setup_election, getVoter, setup_election_details):
    _, owner = setup_election
    voter1 = getVoter

    election = setup_election_details
    election.registerAsVoter("Elon Musk", sender=voter1)

    election.verifyVoter(True, voter1.address, sender=owner)

    assert election.voterDetails(voter1.address).isRegistered == True

    election.vote(1, sender=voter1)

    assert election.voterDetails(voter1.address).hasVoted == True
    assert election.candidateDetails(1).voteCount == 1


def test_fail_election_not_started(setup_election, getVoter, setup_election_details):

    _, owner = setup_election
    voter1 = getVoter

    election = setup_election_details
    election.registerAsVoter("Elon Musk", sender=voter1)

    election.verifyVoter(True, voter1.address, sender=owner)

    election.endElection(sender=owner)

    with pytest.raises(
        ape.exceptions.ContractLogicError, match="Election has not started"
    ):
        election.vote(1, sender=voter1)

def test_fail_election_ended(setup_election, getVoter, setup_election_details):

    _, owner = setup_election
    voter1 = getVoter

    election = setup_election_details
    election.registerAsVoter("Elon Musk", sender=voter1)

    election.verifyVoter(True, voter1.address, sender=owner)

    election.endElection(sender=owner)

    with pytest.raises(
        ape.exceptions.ContractLogicError, match="Election has not started"
    ):
        election.vote(1, sender=voter1)


def test_end_election(setup_election, getVoter):
    election, owner = setup_election
    voter1 = getVoter
    election.endElection(sender=owner)

    assert election.getEnd() == True
    assert election.getStart() == False
