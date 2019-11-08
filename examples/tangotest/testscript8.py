import tango
import pytest
import numpy as np
from tango import DevState

dev = tango.DeviceProxy('sys/tg_test/1')
cfg = dev.get_pipe_config()
assert cfg[0].description == u'This is a test pipe'
assert cfg[0].disp_level == tango.DispLevel.OPERATOR
assert cfg[0].label == u'Test pipe'
assert cfg[0].name == u'TestPipe'
assert cfg[0].writable == tango.PipeWriteType.PIPE_READ_WRITE

# read the blob stored in TangoTest.py
read_blob = dev.read_pipe('TestPipe')
assert read_blob[0] == "theBlob"
blob_data = read_blob[1]
assert blob_data[0]['name'] == 'double'
assert blob_data[0]['value'] == 3.142
assert blob_data[1]['name'] == 'integer64'
assert blob_data[1]['value'] == 32767
assert blob_data[2]['name'] == 'string'
assert blob_data[2]['value'] == "abcdefghjklmno"
assert blob_data[3]['name'] == 'bool'
assert blob_data[3]['value'] == True
inner_blob = blob_data[4]['value']
assert inner_blob[0] == "Inner"
inner_blob_data = inner_blob[1]
assert inner_blob_data[0]['name'] == "double_list"
assert inner_blob_data[0]['value'] == [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]
assert inner_blob_data[1]['name'] == "np_array"
assert inner_blob_data[1]['value'] == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
assert inner_blob_data[2]['name'] == "int_list"
assert inner_blob_data[2]['value'] == [1,2,3,4,5,6,7,8,9,10,11,12]
assert inner_blob_data[3]['name'] == "string_list"
assert inner_blob_data[3]['value'] == ["abc","def","ghi","jkl","mno"]
assert blob_data[5]['name'] == 'encoded'
format,data = blob_data[5]['value']
assert format == "format"
assert data == [0x00, 0x01, 0x02,0xfd, 0xfe, 0xff]
 
blob = ('pipeWriteTest0', dict(double=56.98, long64=-169, str="write test",
                               bool=False, state=DevState.FAULT))
dev.write_pipe('TestPipe', blob)
read_blob = dev.read_pipe('TestPipe')
assert read_blob[0] == "pipeWriteTest0"
blob_data = read_blob[1]
assert blob_data[0]['name'] == 'double'
assert blob_data[0]['value'] == 56.98
assert blob_data[1]['name'] == 'state'
assert blob_data[1]['value'] == tango.DevState.FAULT
assert blob_data[2]['name'] == 'bool'
assert blob_data[2]['value'] == False
assert blob_data[3]['name'] == 'long64'
assert blob_data[3]['value'] == -169
assert blob_data[4]['name'] == 'str'
assert blob_data[4]['value'] == "write test"

inner_blob =  ("Inner", [("double_list",[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]),
                         ("np_array", np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17], np.int64)),
                         ("int_list", [1,2,3,4,5,6,7,8,9,10,11,12]),
                         ("string_list", ["abc","def","ghi","jkl","mno"])
                         ])
blob = ("theBlob", [("double",3.142), 
                    ("integer64", 32767),
                    ("string", "abcdefghjklmno"),
                    ("bool", True),
                    ("innerblob", inner_blob),
# uncomment this when cpp pipe write has been tested
#                     {"name":"encoded", "value":("format", 
#                                                 [0x00, 0x01, 0x02,0xfd, 0xfe, 0xff]),
#                                                 "dtype":tango.CmdArgType.DevEncoded},
                    ])
# re-write the original blob stored in TangoTest.py and check
dev.write_pipe('TestPipe', blob)
read_blob = dev.read_pipe('TestPipe')
assert read_blob[0] == "theBlob"
blob_data = read_blob[1]
assert blob_data[0]['name'] == 'double'
assert blob_data[0]['value'] == 3.142
assert blob_data[1]['name'] == 'integer64'
assert blob_data[1]['value'] == 32767
assert blob_data[2]['name'] == 'string'
assert blob_data[2]['value'] == "abcdefghjklmno"
assert blob_data[3]['name'] == 'bool'
assert blob_data[3]['value'] == True
inner_blob = blob_data[4]['value']
assert inner_blob[0] == "Inner"
inner_blob_data = inner_blob[1]
assert inner_blob_data[0]['name'] == "double_list"
assert inner_blob_data[0]['value'] == [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]
assert inner_blob_data[1]['name'] == "np_array"
assert inner_blob_data[1]['value'] == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
assert inner_blob_data[2]['name'] == "int_list"
assert inner_blob_data[2]['value'] == [1,2,3,4,5,6,7,8,9,10,11,12]
assert inner_blob_data[3]['name'] == "string_list"
assert inner_blob_data[3]['value'] == ["abc","def","ghi","jkl","mno"]
assert blob_data[5]['name'] == 'encoded'
format,data = blob_data[5]['value']
assert format == "format"
assert data == [0x00, 0x01, 0x02,0xfd, 0xfe, 0xff]

print("passed")