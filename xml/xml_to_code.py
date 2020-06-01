'''
<structure>
    <structure name="Stock">
        <field type="SizedRegexString" maxlen="8" pattern="'[A-Z]+$'">name</field>
        <field type="PositiveInteger">shares</field>
        <field type="PositiveFloat">price</field>
    </structure>
    <structure name="Point">
        <field type="Integer">x</field>
        <field type="Integer">y</field>
    </structure>
    <structure name="Address">
        <field type="String">hostname</field>
        <field type="Integer">port</field>
    </structure>
</structure>


class Stock(Structure):
    name = SizedRegexString(pattern='[A-Z]+$', maxlen=8)
    shares = PositiveInteger()
    price = PositiveFloat()

class Point(Structure):
    x = Integer()
    y = Integer()

class Address(Structure):
    #_fields = ['hostname', 'port']
    hostname = String()
    port = Integer()

'''
from xml.etree.ElementTree import parse

def _xml_to_code(filename):
    doc = parse(filename)
    code = ''
    for structure in doc.findall('structure'):  # There are 3 structure so this will run 3 times.
        clscode = _struct_to_class(structure)
        code += clscode
    return code

def _struct_to_class(structure):
    name = structure.get('name')
    code = 'class %s(Structure):\n' % name
    for field in structure.findall('field'):
        dtype = field.get('type')

        options = ['%s = %s'% (key,val) for key,val in field.items() if key != 'type']
        name = field.text.strip()
        code += '    %s = %s(%s)\n' % (name, dtype, ','.join(options))
    return code

