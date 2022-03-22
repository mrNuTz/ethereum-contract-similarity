from contract.opcodes import opcode_by_name

_highFOps = (
  # based on solc-versions-testset
  # top 30 f-stat values
  'ADDRESS', 'LOG3', 'TIMESTAMP', 'ORIGIN', 'LOG4', 'SHA3', 'SWAP14', 'CALLDATASIZE',
  'CALLDATACOPY', 'SIGNEXTEND', 'CALL', 'LOG2', 'RETURNDATASIZE', 'CALLER', 'EXTCODESIZE', 'JUMPI',
  'STATICCALL', 'RETURNDATACOPY', 'GAS', 'DUP13', 'DUP5', 'DUP8', 'GASPRICE', 'SHR', 'PUSH4',
  'ISZERO', 'DUP7', 'ADD', 'DUP9', 'MUL',

  # occurred in only one group
  'MOD', 'MULMOD', 'XOR', 'BYTE', 'CALLVALUE', 'DELEGATECALL', 'SELFDESTRUCT',

  # never occurred
  'SDIV', 'SAR', 'EXTCODECOPY', 'EXTCODEHASH', 'BLOCKHASH', 'LOG0', 'CREATE',
)

_highFOps = { opcode_by_name(name).code for name in _highFOps }

def highFStatPred(b: int) -> bool:
  return b in _highFOps

_highFOpsV2 = (
  # based on solc-versions-testset
  # top 30 f-stat values
  'ADDRESS', 'LOG3', 'TIMESTAMP', 'ORIGIN', 'LOG4', 'SHA3', 'SWAP14', 'CALLDATASIZE',
  'CALLDATACOPY', 'SIGNEXTEND', 'CALL', 'LOG2', 'RETURNDATASIZE', 'CALLER', 'EXTCODESIZE', 'JUMPI',
  'STATICCALL', 'RETURNDATACOPY', 'GAS', 'DUP13', 'DUP5', 'DUP8', 'GASPRICE', 'SHR', 'PUSH4',
  'ISZERO', 'DUP7', 'ADD', 'DUP9', 'MUL',

  # occurred in only one group
  'XOR', 'CALLVALUE', 'DELEGATECALL', 'SELFDESTRUCT',

  # never occurred
  'SAR', 'LOG0', 'CREATE',
)

_highFOpsV2 = { opcode_by_name(name).code for name in _highFOpsV2 }

def highFStatV2Pred(b: int) -> bool:
  return b in _highFOpsV2
