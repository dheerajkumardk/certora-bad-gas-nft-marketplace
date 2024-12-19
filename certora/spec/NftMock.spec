/*
* Verification of NftMock
*/

using NftMock as nft;

methods {
    // Methods: Summary and Non-summary declarations
    // Non-summary declarations
    // Use the function as defined in the codebase
    function totalSupply() external returns uint256 envfree;
    function mint() external;
    function balanceOf(address) external returns uint256 envfree;

    //// Summary declarations
    //// Sometimes the function is too complex
    //// Sometimes the functions are only called by one or two contracts
    //// Sometimes we want to make more assumptions for the prover
    // Ex: function totalSupply() external returns uint256 => ALWAYS(1)


    ///////////// METHOD ENTRIES //////////////
    // Exact Entries
    // Tells the prover that here's a particular function, on a particular contract, test it.
    // If contract name is omitted, the default is currentContract.
    // Ex: function currentContract.totalSupply() external returns(uint256);

    // Wildcard Entries
    // Matches any function in any contract with the indicated name, argument types and visibility
    // Ex: function _.totalSupply() external returns(uint256);

    // Catch-all Entries
    // Allows us to specify that all functions of a given contract are to behave the same way
    // Ex: function currentContract._() external returns(uint256) => ALWAYS(1);
}

// invariant totalSupplyIsNotNegative()
//     totalSupply() >= 0;


rule minting_mints_one_nft() {
    // Arrange
    env e;
    address minter;
    require e.msg.sender == minter;
    require e.msg.value == 0;
    mathint balanceBefore = nft.balanceOf(minter);

    // Act
    currentContract.mint(e);

    // Assert
    assert to_mathint(nft.balanceOf(minter)) == balanceBefore + 1;
}

// Parametric rule
rule no_change_to_total_supply() {
    method f;
    env e;
    calldataarg arg;
    uint256 totalSupplyBefore = totalSupply();

    f(e, arg);

    assert totalSupply() == totalSupplyBefore, "Total supply should not change";
}

// rule sanity {
    // satisfy true;
// }