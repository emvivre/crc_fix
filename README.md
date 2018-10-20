# crc_fix
Change the content of a buffer to set the computed CRC to an arbitrary value.

Two functions are provided :
 - ``new_s = crc_fix( s, crc_dst )`` : return a string with 4 bytes added at the end of ``s`` to have ``CRC(s + 4bytes) == crc_dst``, with ``crc_dst`` the CRC target.
 - ``new_s = crc_fix_pos( s, crc_dst, pos )`` : modify the content of ``s`` at the position ``pos`` to have ``CRC(s[:pos] + 4bytes + s[pos+4:]) == crc_dst``, with ``crc_dst`` the CRC target.
 
