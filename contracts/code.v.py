# Open Auction

# Auction params
# Beneficiary receives money from the highest bidder
Payment: event({amount: uint256(wei), arg2: indexed(address)})

# beneficiary: public(address)
auction_start: public(timestamp)
auction_end: public(timestamp)

# Items
M_items: public(int128)

# Large prime no
q: public(int128)

bidder_registered: public(int128)

notary_registered: public(int128)

# Current state of auction
# highest_bidder: public(address)
# highest_bid: public(wei_value)

# Set to true at the end, disallows any change
# ended: public(bool)

bidder: public({
    n: int128,
    notary: address
}[address])

notary: public({
    bidder: address,
    bid_input: int128[10][2],
    bid_value: int128[2],
    n: int128
}[address])

bidder_map: address[int128]



notary_map: address[int128]
notary_num: public(int128)
winners: public(int128)
winner_bidder: address[int128]

bidders_sort_val: decimal[int128]

# Create a simple auction with `_bidding_time`
# seconds bidding time on behalf of the
# beneficiary address `_beneficiary`.
@public
def __init__(bidding_time: timedelta, m: int128, Q: int128):
    self.M_items = m
    self.q = Q
    self.bidder_registered = 0
    self.notary_registered = 0
    self.notary_num = 0
    self.auction_start = block.timestamp
    self.auction_end = self.auction_start + bidding_time 


@public
@payable
def __default__():
    send(msg.sender, msg.value)
    log.Payment(msg.value, msg.sender)

@public
def register_notaries():
    self.notary_map[self.notary_registered] = msg.sender
    self.notary_registered += 1

@public
def assignee(notary_idx: int128) -> int128:
    x: int128
    x = notary_idx + 1
    return x

@public
def sqrt(_val: decimal) -> decimal :
    z: decimal = (_val +1.0) / 2.0
    y: decimal = _val
    for i in range(100):
        if z < y:
            break
        y = z
        z = (_val/ z + z) / 2.0
    return y

@public
def assign_notary(sender: address, bid_items: int128[10][2], bid_amount: int128[2], num_items: int128):
    self.notary[self.notary_map[self.notary_num]].bidder = sender
    self.bidder[sender].notary = self.notary_map[self.notary_num]
    self.notary_num = self.assignee(self.notary_num)

    self.bidder[sender].n = num_items
    
    self.notary[self.bidder[sender].notary].bid_value = bid_amount
    self.notary[self.bidder[sender].notary].bid_input = bid_items
    self.notary[self.bidder[sender].notary].n = num_items


@public
@payable
def register_bidders(bid_items: int128[10][2], bid_amount: int128[2], num_items: int128):
    self.bidder_map[self.bidder_registered] = msg.sender
    self.bidder_registered += 1
    sender: address = msg.sender
    self.assign_notary(sender, bid_items, bid_amount, num_items)



@public
def get_value_notary(j: int128, k: int128, r: int128) -> decimal:
    ui: decimal = convert(self.notary[self.bidder_map[j]].bid_value[0], 'decimal')
    uj: decimal = convert(self.notary[self.bidder_map[k]].bid_value[0], 'decimal')
    vi: decimal = convert(self.notary[self.bidder_map[j]].bid_value[1], 'decimal')
    vj: decimal = convert(self.notary[self.bidder_map[k]].bid_value[1], 'decimal')

    ni: decimal = convert(self.notary[self.bidder_map[j]].n, 'decimal')
    nj: decimal = convert(self.notary[self.bidder_map[k]].n, 'decimal')

    x: decimal = (ui - uj) / ni
    y: decimal = (vi - vj) / nj
    if r == 1:
        return x
    elif r == 2:
        return y

@public
def compareIndex(j: int128, k: int128) -> bool:
    val1: decimal = self.get_value_notary(j, k, 1)
    val2: decimal = self.get_value_notary(j, k, 2)

    Q: decimal = convert(self.q, 'decimal')

    if val1 + val2 < Q / 2.0:
        return False
    return True

@public
def swap_bidders(j: int128, k: int128) -> bool:
    # temp: int128[2] = self.notary[self.bidder_map[j]].bid_value
    # self.notary[self.bidder_map[j]].bid_value = self.notary[self.bidder_map[j + 1]].bid_value
    # self.notary[self.bidder_map[j + 1]].bid_value = temp

    temp: address = self.bidder_map[j]
    self.bidder_map[j] = self.bidder_map[j + 1]
    self.bidder_map[j + 1] = temp

    return True

@public
def winnerDetermine():
    # for i in range(0,self.bidder_registered):
    #     u: decimal = convert(self.notary[self.bidder_map[i]].bid_value[0], 'decimal')
    #     v: decimal = convert(self.notary[self.bidder_map[i]].bid_value[1], 'decimal')
    #     w: decimal = (u + v) % self.q
    #     s: decimal = convert(self.notary[self.bidder_map[i]].n, 'decimal')

    #     self.bidder_sort_val[i] = w * sqrt(s)  
    for i in range(10): 
        if i >= self.bidder_registered:
            return
        
        for j in range(10):
            if j == self.bidder_registered -i - 1:
                break

            if self.compareIndex(j, j + 1):
                self.swap_bidders(j, j + 1)

    for i in range(0,10):
        if i >= self.bidder_registered:
            return
        
        flag: int128 = 0
        
        for j in range(0,10):
            if j >= self.winners:
                return

            for k in range(10):
                for l in range(0,10):
                    
                    if (self.notary[self.bidder_map[i]].bid_input[j][0] + self.notary[self.bidder_map[i]].bid_input[j][1]) % self.q == (self.notary[self.winner_bidder[k]].bid_input[l][0] + self.notary[self.winner_bidder[k]].bid_input[l][1]) % self.q:
                        flag = 1
                        break
                
                if flag == 1:
                    break
            
            if flag == 1:
                break
        
        if flag == 0:
            l:int128 = self.winners
            self.winner_bidder[l] = self.bidder_map[i]
            self.winners = self.winners + 1



