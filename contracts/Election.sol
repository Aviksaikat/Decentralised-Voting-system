// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Election {
    address public admin;
    uint256 public candidateCount;
    uint256 public voterCount;
    bool private start;
    bool private end;

    // Event emitted after successful candidate registration
    event CandidateAdded(string name, string slogan);

    // Event emitted after successful voter registration
    event VoterRegistered(address indexed voterAddress, string name);

    // Candidate Details
    struct Candidate {
        uint256 candidateId;
        string name;
        string slogan;
        uint256 voteCount;
    }

    // Modeling Election Details
    struct ElectionDetails {
        string adminName;
        string adminEmail;
        string adminTitle;
        string electionTitle;
        string organizationTitle;
    }

    mapping(uint256 => Candidate) public candidateDetails;
    ElectionDetails public electionDetails;

    constructor() payable {
        require(msg.value == 0.5 ether, "Send sufficient funds");
        
        admin = msg.sender;
        candidateCount = 0;
        voterCount = 0;
        start = false;
        end = false;
    }

    function getAdmin() public view returns (address) {
        return admin;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Admin Only");
        _;
    }

    // Add new candidaites
    function addNomineeCandidate(string calldata _name, string calldata _slogan) public onlyAdmin {
        candidateCount++;
        Candidate memory newCandidate =
            Candidate({
                candidateId: candidateCount, 
                name: _name, 
                slogan: _slogan, 
                voteCount: 0
            });
        candidateDetails[candidateCount] = newCandidate;

        //add event here
        emit CandidateAdded(_name, _slogan);
    }

    function setElectionDetails(
        string calldata _adminName,
        string calldata _adminEmail,
        string calldata _adminTitle,
        string calldata _electionTitle,
        string calldata _organisationTitle
    ) public onlyAdmin {
        electionDetails = ElectionDetails(_adminName, _adminEmail, _adminTitle, _electionTitle, _organisationTitle);
        start = true;
        end = false;
    }

    // Get Elections details
    function getElectionDetails()
        public
        view
        returns (
            string memory adminName,
            string memory adminEmail,
            string memory adminTitle,
            string memory electionTitle,
            string memory organizationTitle
        )
    {
        return (
            electionDetails.adminName,
            electionDetails.adminEmail,
            electionDetails.adminTitle,
            electionDetails.electionTitle,
            electionDetails.organizationTitle
        );
    }

    // Get candidates count
    function getTotalCandidate() public view returns (uint256) {
        // Returns the total number of candidates
        return candidateCount;
    }

    // Get voters count
    function getTotalVoter() public view returns (uint256) {
        // Returns the total number of voters
        return voterCount;
    }

    // Modeling a voter
    struct Voter {
        address voterAddress;
        string name;
        bool isVerified;
        bool hasVoted;
        bool isRegistered;
    }

    address[] public voters; // Array of addresses to store addresses of voters
    mapping(address => Voter) public voterDetails;

    // Request to be added as a voter
    function registerAsVoter(string memory _name) public {
        // Check if the wallet is already registered
        require(!voterDetails[msg.sender].isRegistered, "Already registered");
        
        Voter memory newVoter = Voter({
            voterAddress: msg.sender,
            name: _name,
            hasVoted: false,
            isVerified: false,
            isRegistered: true
        });
        voterDetails[msg.sender] = newVoter;
        voters.push(msg.sender);
        voterCount += 1;

        //add event
        emit VoterRegistered(msg.sender, _name);
    }

    // Verify voter
    function verifyVoter(bool _verifiedStatus, address voterAddress) public onlyAdmin {
        voterDetails[voterAddress].isVerified = _verifiedStatus;
    }

    // Vote
    function vote(uint256 candidateId) public {
        require(voterDetails[msg.sender].hasVoted == false, "You have already voted");
        require(voterDetails[msg.sender].isVerified == true, "You are not verified to vote");
        require(start == true, "Election has not started");
        require(end == false, "Election has ended");
        candidateDetails[candidateId].voteCount++;
        voterDetails[msg.sender].hasVoted = true;
    }

    // End election
    function endElection() public onlyAdmin {
        end = true;
        start = false;
    }

    // Get election start and end values
    function getStart() public view returns (bool) {
        return start;
    }

    function getEnd() public view returns (bool) {
        return end;
    }
}
