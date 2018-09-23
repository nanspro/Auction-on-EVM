# Open Auction

# Auction params
# Beneficiary receives money from the highest bidder
Payment: event({amount: uint256(wei), arg2: indexed(address)})
Winners: event({count: int128})

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
    notary: address,
    isValid: bool
}[address])

notary: public({
    bidder: address,
    bid_input: int128[10][2],
    bid_value: int128[2],
    n: int128,
    isValid: bool,
    isAssigned: bool,
    fees: int128
}[address])

bidder_map: address[int128]



notary_map: address[int128]
notary_num: public(int128)
winners: public(int128)
winner_bidder: address[int128]
c: int128

# Create a simple auction with `_bidding_time`
# seconds bidding time on behalf of the
# beneficiary address `_beneficiary`.
@public
def __init__(bidding_time: timedelta, m: int128, Q: int128):
    self.M_items = m
    self.q = Q
    self.c = 2
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
    self.notary[msg.sender].isValid = True
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
    self.notary[self.notary_map[self.notary_num]].isAssigned = True
    self.bidder[sender].notary = self.notary_map[self.notary_num]
    self.bidder[msg.sender].isValid = True
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

    x: decimal = (ui - uj) / self.sqrt(ni)
    y: decimal = (vi - vj) / self.sqrt(nj)
    if r == 1:
        return x
    elif r == 2:
        return y

@public
def which_greater(j: int128, k: int128) -> bool:
    val1: decimal = self.get_value_notary(j, k, 1)
    val2: decimal = self.get_value_notary(j, k, 2)

    Q: decimal = convert(self.q, 'decimal')

    if val1 + val2 < Q / 2.0:
        return False
    return True

@public
def swap_bidders(j: int128, k: int128):
    temp: address = self.bidder_map[j]
    self.bidder_map[j] = self.bidder_map[j + 1]
    self.bidder_map[j + 1] = temp


# @public
# def get_winners() -> int128:
#     log.Winners(self.winners)
#     return self.winners

##### Quick Sort
# @public
# def partition(low: int128, high: int128) -> int128:
#     i: int128 = low      # index of smaller element
#     pivot: int128 = high    # pivot
 
#     for j in range(low , high):
 
#         # If current element is smaller than or
#         # equal to pivot
#         if self.which_greater(j, pivot):
         
#             # increment index of smaller element
#             i = i + 1
#             self.swap_bidders(i,j)
 
#     self.swap_bidders(i + 1, high)
#     return (i + 1) 

# @public
# def quickSort(low: int128, high: int128):
#     if low < high:
 
#         # pi is partitioning index, arr[p] is now
#         # at right place
#         pi = self.partition(low,high)
 
#         # Separately sort elements before
#         # partition and after partition
#         self.quickSort(low, pi - 1)
#         self.quickSort(pi + 1, high)

##### Insertion Sort
@public
def insertionSort():
    # Traverse through 1 to len(arr)
    for i in range(0, 100):
        if i == self.bidder_registered:
            break
        key: int128 = i

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j: int128 = i
        for k in range(100):
            if j >= 0 and self.which_greater(key, j):
                self.bidder_map[j + 1] = self.bidder_map[j]
                j -= 1
            
            else:
                break
        self.bidder_map[j+1] = self.bidder_map[key]

@public
def get_winners():
    self.insertionSort()
    
    # self.quickSort(0,bidder_registered-1)

    for i in range(0,10):
        if i == self.bidder_registered:
            return
        
        flag: int128 = 0
        
        for j in range(0,10):
            if j == self.notary[self.bidder_map[i]].n:
                return

            for k in range(10):
                if k == self.winners:
                    return
                for l in range(0,10):
                    if l == self.notary[self.winner_bidder[k]].n:
                        return
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


@public
def min_j2(idx: int128, ini: int128) -> bool:
    flag: int128 = 0
    for i in range(100):
        if i == idx:
            break
        if i != ini:
            for k in range(0, 10):
                if k == self.notary[self.winner_bidder[idx]].n:
                    break
                for l in range(0, 10):
                    if l == self.notary[self.winner_bidder[i]].n:
                        break
                    if (self.notary[self.winner_bidder[idx]].bid_input[k][0] + self.notary[self.winner_bidder[idx]].bid_input[k][1]) % self.q == (self.notary[self.winner_bidder[i]].bid_input[l][0] + self.notary[self.winner_bidder[i]].bid_input[l][1]) % self.q:
                        flag = 1
                        break
                
                if flag == 1:
                    break
            
            if flag == 1:
                break
    if flag == 1:
        return False
    else:
        return True
            

@public
def min_j(i: int128) -> int128:
    idx: int128 = 100
    for j in range(0,10):
        if j == self.winners:
            break

        flag: int128 = 0
        for k in range(0, 10):
            if k == self.notary[self.winner_bidder[i]].n:
                break
            for l in range(0, 10):
                if l == self.notary[self.winner_bidder[k]].n:
                    break
                if (self.notary[self.winner_bidder[i]].bid_input[k][0] + self.notary[self.winner_bidder[i]].bid_input[k][1]) % self.q == (self.notary[self.winner_bidder[j]].bid_input[l][0] + self.notary[self.winner_bidder[j]].bid_input[l][1]) % self.q:
                    flag = 1
                    break
            
            if flag == 1:
                break
        
        if flag == 0:
            if self.min_j2(idx, i) == True:
                idx = j -1
                break

    if idx != 100:
        return idx
    else:
        return -1
            

@public
def winners_payment(i: int128) -> decimal:
    payment: decimal  
    j: int128 = self.min_j(i)
    if j == -1:
        payment = 0
    else:
        payment = convert((self.notary[self.winner_bidder[j]].bid_value[0] + self.notary[self.winner_bidder[j]].bid_value[1] ) % self.q, 'decimal')
        payment = payment * self.sqrt(self.notary[self.winner_bidder[j]].n)
        payment = payment * self.sqrt(self.notary[self.winner_bidder[i]].n)
    return payment







