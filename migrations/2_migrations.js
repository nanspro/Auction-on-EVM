var Auction = artifacts.require("code");

module.exports = function(deployer) {
  deployer.deploy(Auction, 0x627306090abab3a6e1400e9345bc60c78a8bef57,10);
};
