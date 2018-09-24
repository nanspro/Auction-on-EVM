const Auction = artifacts.require('code')
const assert = require('assert')
// const truffleAssert = require("truffle-assertions");

contract('Auction', accounts => {
    var address_array = new Array()
    const auctioneer = accounts[0];
    const firstBidder = accounts[1];
    const secondBidder = accounts[2];
    const thirdBidder = accounts[3];
    const firstNotary = accounts[4];
    const secondNotary = accounts[5];
    const thirdNotary = accounts[6];

    describe("Assert Contract is deployed", () => {
        let contractInstance;

        beforeEach(async () => {
            contractInstance = await Auction.new(100, 5, 137, { from: auctioneer });
        });

        it("should deploy this contract", async () => {

            var q = await contractInstance.q.call();
            var M = await contractInstance.M_items.call();

            assert.equal(q.toNumber(), 137, "prime no matched");
            assert.equal(M.toNumber(), 5, "no of bidding items matched");

        });
    });

    describe("Fail case", () => {
            it("should revert on invalid form address", async () => {
                try {
                    const instance = await Auction.new(19, 10, 123, {
                        from: "lol"
                    });
                    assert.fail(
                        "should have thrown an error in the above line"
                    );
                } catch (err) {
                    assert.equal(err.message, "invalid address");
                }
            });
    });

    describe("Tests for Notaries", () => {
        let contractInstance;

        beforeEach(async () => {
            contractInstance = await Auction.new(100, 5, 137, { from: auctioneer });
        });

        it("Check if one notary can register", async () => {
            var prevCount = await contractInstance.notary_registered.call();
            await contractInstance.register_notaries({ from: firstNotary });
            var notaryCount = await contractInstance.notary_registered.call();
            assert.equal( Number(notaryCount), Number(prevCount + 1), "num of notaries should be increased by 1" );
        });

        it("Check if multiple notaries can register", async () => {
            var prevCount = await contractInstance.notary_registered.call();
            await contractInstance.register_notaries({ from: firstNotary });
            await contractInstance.register_notaries({ from: secondNotary });
            await contractInstance.register_notaries({ from: thirdNotary });
            var notaryCount = await contractInstance.notary_registered.call();
            assert.equal( Number(notaryCount), Number(prevCount + 3), "3 more notaries should be registered" );
        });

        it("notary cannot register with auctioneer address", async () => {
            try {
                await contractInstance.register_notaries({ from: auctioneer });
            } catch (err) {
                assert.equal(
                    err.message,
                    "VM Exception while processing transaction: revert"
                );
            }
        });

        it("One notary can't register twice", async () => {
            await contractInstance.register_notaries({ from: firstNotary });
            try {
                await contractInstance.register_notaries({ from: firstNotary });
            } catch (err) {
                assert.equal(
                    err.message,
                    "VM Exception while processing transaction: revert"
                );
            }
        });
    });

    describe("Tests for Bidders", () => {
        let contractInstance;

        // since before registering bidders we have to have some notaries
        beforeEach(async () => {
            contractInstance = await Auction.new(100, 5, 137, { from: auctioneer });
            await contractInstance.register_notaries({ from: firstNotary });
            await contractInstance.register_notaries({ from: secondNotary });
            await contractInstance.register_notaries({ from: thirdNotary });
        });

        it("Check if a bidder can register", async () => {
            var prevCount = await contractInstance.bidder_registered.call();
            await contractInstance.register_bidders( [[1, 0], [2, 1]], [5, 6], 2,
                { from: firstBidder,
                    value: web3.toWei(1, "wei")
                }
            );
            // truffleAssert.eventEmitted(result, "bid");
            var bidderCount = await contractInstance.bidder_registered.call();
            assert.equal(Number(bidderCount), Number(prevCount + 1), "num of bidders should increase by 1" );
        });

        it("Check if multiple bidders can register", async () => {
            var prevCount = await contractInstance.bidder_registered.call();
            await contractInstance.register_bidders([[12, 8], [12, 9]], [5, 6], 2, {
                from: firstBidder,
                value: web3.toWei(1, "wei")
            });
            await contractInstance.register_bidders([[7, 1], [12, 9], [11,2]], [4, 6], 3, { 
                from: secondBidder,
                value: web3.toWei(1, "wei")
            });
            await contractInstance.register_bidders([[13, 10], [12, 8]], [3, 4], 2, {
                from: thirdBidder,
                value: web3.toWei(1, "wei")
            });
            var bidderCount = await contractInstance.bidder_registered.call();
            assert.equal( Number(bidderCount), 3, "num of bidders should increase by 3" );
        });

        it("One bidder can't register twice", async () => {
            await contractInstance.register_bidders( [[12, 8], [12, 9]], [5, 6], 2, 
                { from: firstBidder,
                    value: web3.toWei(1, "wei")
                });
            try {
                await contractInstance.register_bidders([[7, 1], [12, 9], [11, 11]], [4, 6], 3,
                    { from: firstBidder, 
                        value: web3.toWei(1, "wei")
                    });
            } catch (err) {
                assert.equal(
                    err.message,
                    "VM Exception while processing transaction: revert"
                );
            }
        });

        // it("bidder should deposit min value of w*sqrt(num_items) wei", async () => {
        //     try {
        //         await instance.register_bidders(
        //             [[12, 8], [12, 9]],
        //             [5, 6],
        //             2,
        //             {
        //                 from: accounts[5],
        //                 value: web3.toWei(1, "wei")
        //             }
        //         );
        //         assert.fail(
        //             "should have thrown an error in the above line"
        //         );
        //     } catch (err) {
        //         assert.equal(
        //             err.message,
        //             "VM Exception while processing transaction: revert"
        //         );
        //     }
        // });

        // it("no notary should register as bidder", async () => {
        //     try {
        //         await contractInstance.register_bidders( [[12, 8], [12, 9]], [5, 6], 2,
        //             {
        //                 from: firstNotary,
        //                 // value: web3.toWei(16, "wei")
        //             }
        //         );
        //         assert.fail( "should have thrown an error in the above line" );
        //     } catch (err) {
        //         assert.equal(
        //             err.message,
        //             "VM Exception while processing transaction: revert"
        //         );
        //     }
        // });
    // describe("Communicating with Notary", () => {
    //     let contractInstance;

    //     // since before registering bidders we have to have some notaries
    //     beforeEach(async () => {
    //         contractInstance = await Auction.new(100, 5, 137, { from: auctioneer });
    //         await contractInstance.register_notaries({ from: firstNotary });
    //         await contractInstance.register_notaries({ from: secondNotary });

    //         await contractInstance.register_bidders([[1, 0], [1, 1], [1, 4]], [20,40], 3, {
    //             from: firstBidder,
    //         });
    //         await contractInstance.register_bidders([[3, 0], [3, 1]], [15,30] 2, {
    //             from: secondBidder,
    //         });
    //     });

    //      it("Getting value about bidder", async () => {
    //         var x = await contractInstance.notary[.call();
    //         // truffleAssert.eventEmitted(result, "bid");
    //         var bidderCount = await contractInstance.bidder_registered.call();
    //         assert.equal(Number(bidderCount), Number(prevCount + 1), "num of bidders should increase by 1" );
    //     });
    });

})