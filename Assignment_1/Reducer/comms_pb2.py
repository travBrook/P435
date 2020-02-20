# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: comms.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='comms.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x0b\x63omms.proto\"\xac\x02\n\x08\x41Message\x12\x18\n\x10\x66unctionFileName\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\x12\'\n\ttheSender\x18\x03 \x01(\x0b\x32\x14.AMessage.InfoOnSelf\x12%\n\x06others\x18\x04 \x03(\x0b\x32\x15.AMessage.InfoOnOther\x12(\n\ttheFriend\x18\x05 \x01(\x0b\x32\x15.AMessage.InfoOnOther\x1a\x36\n\nInfoOnSelf\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04host\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x1a\x46\n\x0bInfoOnOther\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04host\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\r\n\x05range\x18\x04 \x01(\t'
)




_AMESSAGE_INFOONSELF = _descriptor.Descriptor(
  name='InfoOnSelf',
  full_name='AMessage.InfoOnSelf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='AMessage.InfoOnSelf.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='AMessage.InfoOnSelf.host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='AMessage.InfoOnSelf.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=244,
)

_AMESSAGE_INFOONOTHER = _descriptor.Descriptor(
  name='InfoOnOther',
  full_name='AMessage.InfoOnOther',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='AMessage.InfoOnOther.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='AMessage.InfoOnOther.host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='AMessage.InfoOnOther.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='range', full_name='AMessage.InfoOnOther.range', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=246,
  serialized_end=316,
)

_AMESSAGE = _descriptor.Descriptor(
  name='AMessage',
  full_name='AMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='functionFileName', full_name='AMessage.functionFileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='AMessage.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='theSender', full_name='AMessage.theSender', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='others', full_name='AMessage.others', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='theFriend', full_name='AMessage.theFriend', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_AMESSAGE_INFOONSELF, _AMESSAGE_INFOONOTHER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=316,
)

_AMESSAGE_INFOONSELF.containing_type = _AMESSAGE
_AMESSAGE_INFOONOTHER.containing_type = _AMESSAGE
_AMESSAGE.fields_by_name['theSender'].message_type = _AMESSAGE_INFOONSELF
_AMESSAGE.fields_by_name['others'].message_type = _AMESSAGE_INFOONOTHER
_AMESSAGE.fields_by_name['theFriend'].message_type = _AMESSAGE_INFOONOTHER
DESCRIPTOR.message_types_by_name['AMessage'] = _AMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AMessage = _reflection.GeneratedProtocolMessageType('AMessage', (_message.Message,), {

  'InfoOnSelf' : _reflection.GeneratedProtocolMessageType('InfoOnSelf', (_message.Message,), {
    'DESCRIPTOR' : _AMESSAGE_INFOONSELF,
    '__module__' : 'comms_pb2'
    # @@protoc_insertion_point(class_scope:AMessage.InfoOnSelf)
    })
  ,

  'InfoOnOther' : _reflection.GeneratedProtocolMessageType('InfoOnOther', (_message.Message,), {
    'DESCRIPTOR' : _AMESSAGE_INFOONOTHER,
    '__module__' : 'comms_pb2'
    # @@protoc_insertion_point(class_scope:AMessage.InfoOnOther)
    })
  ,
  'DESCRIPTOR' : _AMESSAGE,
  '__module__' : 'comms_pb2'
  # @@protoc_insertion_point(class_scope:AMessage)
  })
_sym_db.RegisterMessage(AMessage)
_sym_db.RegisterMessage(AMessage.InfoOnSelf)
_sym_db.RegisterMessage(AMessage.InfoOnOther)


# @@protoc_insertion_point(module_scope)
