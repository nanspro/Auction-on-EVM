var Auction = artifacts.require("code");

module.exports = function(deployer) {
  deployer.deploy(Auction, 5, 10, 137);
};
