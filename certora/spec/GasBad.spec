/*
* Verification of GasBadNftMarketplace
*/

using GasBadNftMarketplace as gasBadMarketplace;
using NftMock as nft;
using NftMarketplace as marketplace;

methods {
    function getListing(address nftAddress, uint256 tokenId) external returns (INftMarketplace.Listing) envfree optional;
    function getProceeds(address seller) external returns (uint256) envfree optional;

    // DISPATCHER(true) - tells the prover not to assume anything about this function and to draw logic only from examples of this function found within known contracts
    // Use NftMock.safeTransferFrom for all safeTransferFrom calls
    function _.safeTransferFrom(address,address,uint256) external => DISPATCHER(true);
    
    function _.onERC721Received(address,address,uint256,bytes) external => NONDET;
}

ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
    // init_state - sets the initial state
    // axiom - declare that something must always hold true
}
ghost mathint log4Count {
    init_state axiom log4Count == 0;
}

/*
* Hooks
* Hooks allow us to specify an operation which triggers the hook and logic that is executed when the hook is triggered
* 
* Sstore - opcode being hoooked
* s_listings[KEY address nftAddress][KEY uint256 tokenId].price - contract variable being hooked
* price - variable linked to our hooked variable for use in the hook logic
* STORAGE - tells Certora our hook is exclusively for storage
*/

hook Sstore gasBadMarketplace.s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price {
    listingUpdatesCount = listingUpdatesCount + 1;
}

hook LOG4(uint offset, uint length, bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) {
    log4Count = log4Count + 1;
}

invariant anytime_mapping_updated_emit_event()
    listingUpdatesCount <= log4Count;


rule calling_any_function_should_result_in_each_contract_having_the_same_state(method f, method f2) {
    // 1. Call the same function on NftMarketplace and GasBadNftMarketplace
    // 2. Compare the getter functions of both to conclude they are the same

    require(f.selector == f2.selector);
    env e;
    calldataarg args;
    address listingAddr;
    address seller;
    uint256 tokenId;

    require(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);


    // Act
    // It's an error to call same method on 2 diffn contracts
    gasBadMarketplace.f(e, args);
    marketplace.f2(e, args);

    // Assert
    assert(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);
}