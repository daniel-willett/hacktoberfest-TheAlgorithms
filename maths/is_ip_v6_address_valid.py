"""
After seeing is_ip_v4_address_valid.py it only seems appropriate that there should exist an equivalent one for IPv6.
I am going off the following:
    https://www.ibm.com/docs/en/i/7.4?topic=concepts-ipv6-address-formats
    https://www.rfc-editor.org/rfc/rfc4291#section-2.2
    https://www.ibm.com/docs/en/ts4500-tape-library?topic=functionality-ipv4-ipv6-address-formats

Skeleton:
    Basic addresses are of the form x1:x2:x3:x4:x5:x6:x7:x8 where each xi segment is a 16 bit number in hexidecimal notation

Rules:
    Trailing 0's are ok so long as they dont' imply the segment to being a number larger than 16 bits although if it becomes too hard to code then ideally we don't want trailing 0's
    Notation can be shortened where consecutive segments of 0's can be replaced with a `::` (replacing an arbitrary number of 0's). A `::` can only appear at most once. This can be used on leading or trailing 0's of the address and includes the whole address being 0's.
    An address can have IPv4 embedding via the form x1:x2:x3:x4:x5:x6:d1.d2.d3.d4 where each xi is a 16 bit numebr and each dj is an 8 bit decimal number. The same normal rules for double colon applies in the first 6 segments. Please correct me if I'm wrong however to the best of my knoweldge through reading RFC 4291: IPv4 embeddings into IPv6 addresses are only the 'standard' IPv4 format people are used to seeing and none of the alternative formats are allowed both due to clashes with IPv6 but also part of the reason for IPv6's simple syntax is to do away with the complex possible formats that IPv4 could take.  

Valid cases:
    0:0:0:0:0:0:0:1
    ::1
    1::
    :: (is the same as all zeros)
    FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF
    98a:329:adae::23:0:0:1
    1f5e:8fbe:e550:7a07:4679:14fc:1.2.3.4
    ::1.2.3.4 (the implication is 6 segments of 0's and then the IPv4 embedding)
    1::1:1.2.3.4
    132::0.0.0.0


Invalid cases:
    0
    dasjkhdj
    0:0:0:0:0:0:0:0:0 (too many segments)
    0:0:0:0:0:0:0:1.2.3.4 (too many segments)
    0:0:0:0:0:0:1.2.3.4.5 (too many octets)
    12:12.12.32.4 (too few segments)
    10000:0:0:0:0:0:0:0 (too big value)
    


"""


def is_ip_v6_address_valid(ip_v6_address: str) -> bool:
    ip_v6_address = ip_v6_address.strip() #Remove any whitespace for formatting and reduce errors
    blocks = ip_v6_address.split(":")
    
    if (len(blocks)<3):
        #The smallest address representation is "::" which is 3 blocks
        return False

    if (blocks[-1].find(".") != -1): #If the last block contains dots then we should see if this is an IPv4 embdedded IPv6 address[...]
        ipv4_end = blocks[-1]
        ipv6_start = blocks[0:len(blocks)-1]
        if (len(ipv6_start)>6): 
            #The largest representation is 6 semicolons using a double colon on one end e.g. 1:2:3:4:5::(6.7.8.9) which gives 6 blocks as a possible maximum)
            return False
        else:
            from is_ip_v4_address_valid import is_ip_v4_address_valid #No point re-writing code which already exists on this codebase :P
            return (is_ip_v4_address_valid(ipv4_end) and test_blocks(ipv6_start,6))
    
    else: #[...]otherwise we just do a standard IPv6 test (without IPv4 embedding)
        if (len(blocks)>9):
            #The largest representation is 8 semicolons using a double colon on one end e.g. 1:2:3:4:5:6:7:: which gives 9 blocks as a possible maximum)
            return False
        else:
            return test_blocks(blocks,8)


def test_blocks(blocks: list, n: int) -> bool:
    #We want to ignore the case "::" because this is the exception to the rule as technically you have 3 positions empty instead of 2
    if (blocks == ['','','']):
        return True
    number_of_empty = 0 
    index = 0
    for segment in blocks:
        if (segment == ""):
            if ((number_of_empty == 1) and (blocks[index-1]!="") or (number_of_empty > 1)): #If we've seen a double colon already and the previous block wasn't caused from "::" or "::x" or "x::", or if we've seen too many empty blocks (which implies multiple double colons)
                return False
            number_of_empty += 1
        else:
            if (is_16_bit_number(segment)==False):
                return False
        index += 1

    if (number_of_empty==0) and (len(blocks)!=n): #If there was no shortening through double colons but we have less blocks than defined through n (only expected values are 6 and 8)
        return False
    else: #It's passed all the tests so we return true
        return True




def is_16_bit_number(x: str) -> bool:
    #Remember, this is in hexedecimal which means base 16 [0-F]
    try:
        n = int(x,16) #Convert from base 16 to integer
        return len(x) <= 4 
        """
        Being 16 bit in hex means at most 4 characters. e.g. 01234 implies a number which requires more than 16 bits to represent. Given 2*16 is FFFF which is the largest you can have for 4 characters we don't need to check n < 2**16 as this will always be the case if len(x) <= 4.
        If we were checking e.g. IPv4 octets we would need to make sure that n < 2**8 as well as e.g. x="256" would certainly give len(x) <= 3 but this isn't a valid octet value because n = int(x,10) = 2**8
        """
    except:
        #It wasn't valid hex
        return False
