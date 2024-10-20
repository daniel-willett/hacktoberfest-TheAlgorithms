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
    An address can have IPv4 embedding via the form x1:x2:x3:x4:x5:x6:d1.d2.d3.d4 where each xi is a 16 bit numebr and each dj is an 8 bit number. The same normal rules for double colon applies in the first 6 segmetns whilst the  

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
    
    if (len(blocks) < 3) or (len(blocks)>9):
        #The smallest address representation is "::" which is 3 blocks and the largest is 8 semicolons which gives 9 blocks)
        return False

    number_of_empty = 0 
    index = 0
    for segment in blocks:
        if (segment == ""):
            if (number_of_empty == 1) and (blocks[index-1]!=""): #If we've seen a double colon already and the previous block wasn't caused from "::" or "::x" or "x::"
                return False
            number_of_empty += 1
        else:
            if (is_16_bit_number(segment)==False):
                return False

        index += 1

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



print(is_16_bit_number(""))
print(is_16_bit_number("AFD2"))
print(is_16_bit_number("1"))
print(is_16_bit_number("001"))
print(is_16_bit_number("00001"))
print(is_16_bit_number("12345"))





