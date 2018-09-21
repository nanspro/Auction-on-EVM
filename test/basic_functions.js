var hello = artifacts.require('code')
contract('hello:GetMessage', function(accounts) {
  it("should assert true", function(done) {
    var basic_functions = basic_functions.deployed();
    basic_functions.then(function(contract){
    	return contract.GetMessage.call();
    }).then(function(result){
    	assert.isTrue(result === 'Hello World');
    	done();
    })
  });
});
