import pytest

from scripts.deploy import deploy
from scripts.helper_functions import get_account


@pytest.fixture()
def setup_election():
    return deploy()


@pytest.fixture()
def getVoter():
    return get_account(2)


@pytest.fixture()
def setup_election_details():
    election, owner = deploy()
    voter1 = get_account()

    election.setElectionDetails(
        "Jadu Vote",
        "jadu-vote@jadu.com",
        "The Jadu Party",
        "Amra chai Rood",
        "Jaadu Dadau",
        sender=owner,
    )

    election.addNomineeCandidate("Neel Jadu", "Amra chai Rood", sender=owner)
    return election
