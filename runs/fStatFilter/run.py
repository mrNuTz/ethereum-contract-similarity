import sys, os, re, random
from typing import Callable, NamedTuple
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis, test
import contract.opcodes as opcodes
import pandas as pd
from common import Id1Id2FloatT, IdCodeT, IdFloatT, IdStrT

highFOps = [
  # top 30 f-stat values
  'ADDRESS', 'LOG3', 'TIMESTAMP', 'ORIGIN', 'LOG4', 'SHA3', 'SWAP14', 'CALLDATASIZE',
  'CALLDATACOPY', 'SIGNEXTEND', 'CALL', 'LOG2', 'RETURNDATASIZE', 'CALLER', 'EXTCODESIZE', 'JUMPI',
  'STATICCALL', 'RETURNDATACOPY', 'GAS', 'DUP13', 'DUP5', 'DUP8', 'GASPRICE', 'SHR', 'PUSH4',
  'ISZERO', 'DUP7', 'ADD', 'DUP9', 'MUL',

  # occurred in only one group
  'MOD', 'MULMOD', 'XOR', 'BYTE', 'CALLVALUE', 'MISSING', 'DELEGATECALL', 'SELFDESTRUCT',

  # never occurred
  'SDIV', 'SAR', 'EXTCODECOPY', 'EXTCODEHASH', 'BLOCKHASH', 'LOG0', 'CREATE',
]

highFOps = [ opcodes.opcode_by_name(name) for name in highFOps ]

