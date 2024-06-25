import yaml
import sys

def processVal(val):
    val['val'] = 888

def processVal2(val):
    processVal(val)
    val['val'] += 10
    # здесь могла бы быть отправка на сервер или ещё какая операция и функция могла бы соответсвующе называться

# processVal3 = lambda val: val['val'] * 10

def read_modules_config(yaml_path):
    with open(yaml_path, "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def element_exist(path, element):
    return element in path

def remove_if_exist_from_top(element, container):
    for v in container:
        if v == element:
            print(f"remove {v}\n")
            container.remove(v)
            return

def module_subtree(modules_name_list, modules_dict, processVal):
    subtree_list = []

    top_level_modules = modules_name_list.copy()
    visited_modules = []
    modules_dict = modules_dict['modules']

    last_index_for_level_in_list = {}

    def addDepFromModule(module_name, index_branch, level = 0):
        if module_name in visited_modules:
            remove_if_exist_from_top(module_name, top_level_modules)
            return
        
        visited_modules.append(module_name)
        if( not element_exist(subtree_list, module_name)):
            if(index_branch != 0):
                subtree_list.insert(last_index_for_level_in_list[level], module_name)
                for i in range(level ,len(last_index_for_level_in_list)):
                    last_index_for_level_in_list[i] += 1 
            else:
                subtree_list.append(module_name)
                last_index_for_level_in_list[level] = len(subtree_list)

        if 'depends' in modules_dict[module_name]:
            for dep in modules_dict[module_name]['depends']:
                addDepFromModule(dep, index_branch, level + 1)
        if 'val' in modules_dict[module_name]:
            processVal(modules_dict[module_name])

    for index, module in enumerate(modules_name_list):
        addDepFromModule( module, index )

    return subtree_list, top_level_modules


modules_dict = read_modules_config('no-recursive.yaml')
modules_name_list = sys.argv[1:]

print("before")
print(modules_dict)
modules_name_list, top_level_modules = module_subtree(modules_name_list, modules_dict, processVal2)
print("after")
print(modules_dict)

print(f"List dependency: { modules_name_list}")
print(f"Top Level: { top_level_modules }")