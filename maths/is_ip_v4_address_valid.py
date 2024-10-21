"""
Is IP v4 address valid?
Many people don't realise that IPv4 is a significantly harder syntax than IPv6 (another reason why IPv6 is better than IPv4 is a more rigid syntax).
The 'standard' way people are used to IPv4 is d1.d2.d3.d4 where each octet di is a number between 0 and 255. A previous itteration of this python file incorrectly listed it as 254 which is partially the reason I decided to re-write thise whole file rather than just make a small change only for me to later re-write this file anyway.

"""


def is_ip_v4_address_valid(ip_v4_address: str) -> bool:
    octets = [int(i) for i in ip_v4_address.split(".") if i.isdigit()]
    return len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets)

