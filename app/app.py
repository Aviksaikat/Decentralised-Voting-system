#!/usr/bin/python3
from ape import networks
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

connected_account = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/connect", methods=["POST"])
def connect():

    return render_template("deploy.html")


@app.route("/deploy", methods=["POST"])
def deploy():
    admin_name = request.form.get("_adminName")
    admin_email = request.form.get("_adminEmail")
    admin_title = request.form.get("_adminTitle")
    election_title = request.form.get("_electionTitle")
    organization_title = request.form.get("_organisationTitle")

    account = connected_account  # Use the first account for simplicity, you can modify this to use a specific account
    contract = Election.deploy(
        admin_name,
        admin_email,
        admin_title,
        election_title,
        organization_title,
        {"from": account},
    )

    return render_template("deploy.html", contract_address=contract.address)


@app.route("/election")
def election():
    # Get the election details
    (
        admin_name,
        admin_email,
        admin_title,
        election_title,
        organization_title,
    ) = contract.getElectionDetails()
    start = contract.getStart()
    end = contract.getEnd()

    # Get the candidate count and details
    candidate_count = contract.getTotalCandidate()
    candidates = []
    for i in range(1, candidate_count + 1):
        candidate = contract.candidateDetails(i)
        candidates.append(candidate)

    return render_template(
        "election.html",
        admin_name=admin_name,
        admin_email=admin_email,
        admin_title=admin_title,
        election_title=election_title,
        organization_title=organization_title,
        start=start,
        end=end,
        candidates=candidates,
    )


@app.route("/add_candidate", methods=["POST"])
def add_candidate():
    name = request.form.get("name")
    slogan = request.form.get("slogan")

    account = accounts[
        0
    ]  # Use the first account for simplicity, you can modify this to use a specific account
    contract.addNomineeCandidate(name, slogan, {"from": account})

    return render_template("add_candidate.html", name=name, slogan=slogan)


if __name__ == "__main__":
    app.run(debug=True)
