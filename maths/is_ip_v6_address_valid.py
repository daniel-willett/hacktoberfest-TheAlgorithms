"""
After seeing is_ip_v4_address_valid.py it only seems appropriate that there should exist an equivalent one for IPv6.
I am going off https://www.ibm.com/docs/en/i/7.4?topic=concepts-ipv6-address-formats and https://www.rfc-editor.org/rfc/rfc4291#section-2.2

Skeleton:
    Basic addresses are of the form x1:x2:x3:x4:x5:x6:x7:x8 where each xi is a 16 bit number in hexidecimal notation

Rules:
    Trailing 0's are ok so long as they dont' imply a number larger than 16 bits although if it becomes too hard to code then ideally we don't want trailing 0's
    Notation can be shortened where consecutive sets of 0's can be replaced with a `::` (replacing an arbitrary number of 0's). A `::` can only appear at most once. This can be used on leading or trailing 0's.
    An address can have IPv4 embedding via the form x1:x2:x3:x4:x5:x6:d1.d2.d3.d4 where each xi is a 16 bit numebr and each dj is an 8 bit number.

"""


def is_ip_v6_address_valid(ip_v6_address: str) -> bool:
    ip_v6_address = ip_v6_address.strip() #Remove any whitespace for formatting and reduce errors
    blocks = ip_v6_address.split(":")
    
    if (len(blocks) < 3) or (len(blocks)>9):
        #The smallest address representation is "::" which is 3 blocks and the largest is 8 semicolons which gives 9 blocks)
        return False





    def is_16_bit_number(x: str) -> bool:
        #Remember, this is in hexedecimal which means base 16 [0-F]
        try:
            n = int(x,16) #Convert from base 16 to integer
            return n < 2**16 #Being 16 bit means being less than 2^16 (in decimal)
        except:
            #It wasn't valid hex
            return False
