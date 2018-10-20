#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

"""
  ===========================================================================

  Copyright (C) 2018 Emvivre

  This file is part of CRC32_PADDING_FORCE.

  CRC32_PADDING_FORCE is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  CRC32_PADDING_FORCE is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with CRC32_PADDING_FORCE.  If not, see <http://www.gnu.org/licenses/>.

  ===========================================================================
*/
"""

'''
Translation of code from Reversing CRC - Theory and Pratice
'''

import binascii
import struct

CRC32_POLY     = 0xEDB88320
CRC32_INV      = 0x5B358FD3
CRC32_INITXOR  = 0xFFFFFFFF
CRC32_FINALXOR = 0xFFFFFFFF

def crc32( s ):
    crc = CRC32_INITXOR
    for c in s:
        x = ord(c)
        for _ in xrange(8):
            carry = crc & 1
            crc >>= 1
            if carry ^ (x & 1):
                crc ^= CRC32_POLY
            x >>= 1
    crc ^= CRC32_FINALXOR
    return crc

def crc_fix( s, crc_dst ):
    crcreg = crc32(s) ^ CRC32_FINALXOR
    tcrcreg = crc_dst ^ CRC32_FINALXOR
    new_content = 0
    for i in range(32):
        if new_content & 1:
            new_content = (new_content >> 1) ^ CRC32_POLY
        else:
            new_content >>= 1
        if tcrcreg & 1:
            new_content ^= CRC32_INV
        tcrcreg >>= 1
    new_content ^= crcreg
    s += struct.pack('<I', new_content)
    return s

def make_crc_revtable():
    table = []
    for n in range(256):
        c = n << 3*8;
        for k in range(8):
            if ( c & 0x80000000 ) != 0:
                c = (( c ^ CRC32_POLY ) << 1) | 1;
            else:
                c <<= 1
        table.append( c )
    return table

def crc_fix_pos( s, crc_dst, pos ):
    crc_revtable = make_crc_revtable()
    crcreg = crc32(s[:pos]) ^ CRC32_FINALXOR
    s = s[:pos] + struct.pack('<I', crcreg) + s[pos+4:]
    tcrcreg = crc_dst ^ CRC32_FINALXOR
    for i in range(len(s)-1,pos-1,-1):
        tcrcreg = (tcrcreg << 8) ^ crc_revtable[tcrcreg >> 3*8] ^ ord(s[i])
        tcrcreg &= 0xffffffff
    s = s[:pos] + struct.pack('<I', tcrcreg) + s[pos+4:]
    return s


if __name__ == '__main__':
    CRC_DST =  0xCAFEBABE
    s = 'cafebabe'
    crcreg = crc32(s)
    print 'before: %08X' % crcreg
    s = crc_fix( s, crc_dst=CRC_DST )
    crcreg = crc32(s)
    print 'after:  %08X' % crcreg

    print '---------'

    s = 'cafebabeXXXXCOCO'
    crcreg = crc32(s)
    print 'before: %08X' % crcreg
    s = crc_fix_pos( s, crc_dst=CRC_DST, pos=len('cafebabe') )
    crcreg = crc32(s)
    print 'after:  %08X' % crcreg
    print s
