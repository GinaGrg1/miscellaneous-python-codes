from lxml import etree
import os


class ExtractXML:
    def __init__(self, xml_file):
        self.tree = etree.iterparse(xml_file, recover=True)  # one tree per file

    @staticmethod
    def clean_prism_col_dict(temp_dict, keys_to_remove):
        """
        temp_dict :
            {'action': 'Create', 'databaseName': 'MART', 'name': 's_4280_key', 'tableName': 'PD_DIM_PRISM_1',
            'tableOwner': '', 'type': 'ValueList', 'valueType': 'Integer', 'value': 265934}
        We do not need ['action', 'tableOwner', 'type'] so we remove them.
        The final dictionary will have the 'name' as the key.

        final_dict:
            {'s_4280_key': {'databaseName': 'MART', 'tableName': 'PD_DIM_PRISM_1', 'valueType': 'Integer', 'value': 265934}}
        """
        final_dict = {}
        temp_dict = {key: temp_dict[key] for key in temp_dict if key not in keys_to_remove}
        final_dict[temp_dict.pop('name')] = temp_dict
        return final_dict

    def extract_cols_dim_prism(self, column_iter, temp_dict):
        """
        Parse through all the child elements of ColumnConditions.
        Returns temp_dict as:
            {'action': 'Create', 'databaseName': 'MART', 'name': 's_4280_key', 'tableName': 'PD_DIM_PRISM_1',
            'tableOwner': '', 'type': 'ValueList', 'valueType': 'Integer', 'value': 265934}

        """
        for child in column_iter:
            if child.tag == 'Value':
                temp_dict['value'] = int(child.text)
            if child.items():
                print(f'This child {child.tag} has items: {dict(child.items())}')
                temp_dict.update(dict(child.items()))
                self.extract_cols_dim_prism(child, temp_dict)
        return temp_dict

    @staticmethod
    def iter_level_child(child_iterator, temp_dict):  # {'4280':{}}
        """
        should return {'8516' : {'attr_name': 'Toothpaste', 'col_key': 's_4280_key', 'avp_key': 30000,
                                'table':'PRISM_PD_S_8516_1_O','attr_value': qname}}
        """
        key = ''.join(temp_dict.keys())

        attr_name_dict, col_name_dict, table_dict = {}, {}, {}
        for c in child_iterator:
            if c.text:
                if c.tag == 'DisplayName':
                    attr_name_dict = {'attr_name': c.text}
                if c.tag == 'KeyColumns':
                    for column in c.getchildren():
                        if ''.join(temp_dict.keys()) in dict(column.items()).get('name'):
                            col_name_dict = {'col_name': dict(column.items()).get('name')}
                if c.tag == 'MemberGeneration':
                    for member in c.iterchildren():
                        if member.tag == 'MemberName':
                            for mem in member.getchildren():
                                table_dict = {'table_name': dict(mem.items()).get('tableName'),
                                              'database_name': dict(mem.items()).get('databaseName')}
        temp_dict[key] = dict(**attr_name_dict, **col_name_dict, **table_dict)
        return temp_dict

    def extract_level_group(self, level_iter, main_dict):
        for child in level_iter:
            inner_dict = dict()
            key_num = dict(child.items()).get('name').split("_")[-1]
            inner_dict[key_num] = {}
            child_dict = self.iter_level_child(child.iterchildren(), inner_dict)
            main_dict.update(child_dict)
        return main_dict

    def main_extraction(self):
        dim_prism_col_dict, level_group_dict = {}, {}
        for _, elem in self.tree:
            if elem.tag == 'ColumnConditions':
                column_info_dict = self.extract_cols_dim_prism(elem.getchildren(), dict())
                dim_prism_col_dict = self.clean_prism_col_dict(column_info_dict, ['action', 'tableOwner', 'type'])
            if elem.tag == 'LevelGroups':
                level_group_dict = self.extract_level_group(elem.getchildren(), dict())
        return dim_prism_col_dict, level_group_dict


if __name__ == '__main__':
    curr_path = os.getcwd()
    print(curr_path)
    all_level_group_dict, all_prism_col_dict = {}, {}
    for file in curr_path:
        if file.endswith('.xml'):
            print(file)
        #print(f"Extracting from file {os.path.basename(file)}")
        # print(os.path.join(curr_path,file))

        # xml_extraction = ExtractXML(file)
        # prism_col_info_dict, level_info_dict = xml_extraction.main_extraction()
        # all_level_group_dict.update(level_info_dict)
        # all_prism_col_dict.update(prism_col_info_dict)
