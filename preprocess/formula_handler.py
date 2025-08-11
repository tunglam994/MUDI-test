import re

def process_formula(string):   
    """
    Processes a chemical formula string by expanding element abbreviations to full names
    and ensuring numeric subscripts are explicitly represented.

    The function takes a chemical formula string, identifies element symbols and their
    respective quantities, replaces element abbreviations with their full names, and
    ensures each element has an explicit numeric subscript. If a quantity is not specified
    for an element, it defaults to '1'.

    Args:
        string (str): The chemical formula string to process.

    Returns:
        str: A processed string with full element names and explicit quantities.
    """
    map_abrv_dict = {
        'Ag': 'Silver',
        'Al': 'Aluminum',
        'As': 'Arsenic',
        'Au': 'Gold',
        'B': 'Boron',
        'Ba': 'Barium',
        'Bi': 'Bismuth',
        'Br': 'Bromine',
        'C': 'Carbon',
        'Ca': 'Calcium',
        'Cl': 'Chlorine',
        'Co': 'Cobalt',
        'Cu': 'Copper',
        'F': 'Fluorine',
        'Fe': 'Iron',
        'H': 'Hydrogen',
        'Hg': 'Mercury',
        'I': 'Iodine',
        'K': 'Potassium',
        'Li': 'Lithium',
        'Mg': 'Magnesium',
        'N': 'Nitrogen',
        'Na': 'Sodium',
        'O': 'Oxygen',
        'P': 'Phosphorus',
        'Pt': 'Platinum',
        'S': 'Sulfur',
        'Se': 'Selenium',
        'Si': 'Silicon',
        'Tc': 'Technetium',
        'Ti': 'Titanium',
        'Zn': 'Zinc'
        }

    char_list = [c for c in string]
    char_list_new = list()
        
    tmp = ''
    for i in range(len(char_list)):
        if re.match('[0-9]', char_list[i]) and re.match('[0-9]', char_list[i-1]):
            tmp += char_list[i]
        elif re.match('[0-9]', char_list[i]):
            char_list_new.append(tmp)
            tmp = char_list[i]
        elif re.match('[a-z]', char_list[i]):
            tmp += char_list[i]
        elif re.match('[A-Z]', char_list[i]):
            char_list_new.append(tmp)
            tmp = char_list[i]
        
    char_list_new.append(tmp)
    char_list_new = char_list_new[1:]
    
    char_list_return = list()
    for i in range(len(char_list_new)):
        if i == len(char_list_new) - 1:
            if re.match('[a-zA-Z]+', char_list_new[i]):
                char_list_return.append(char_list_new[i])
                char_list_return.append('1')
            else:
                char_list_return.append(char_list_new[i])
        elif re.match('[a-zA-Z]+', char_list_new[i]) and re.match('[a-zA-Z]+', char_list_new[i+1]):
            char_list_return.append(char_list_new[i])
            char_list_return.append('1')
        else:
            char_list_return.append(char_list_new[i])

    for i in range(len(char_list_return)):
        if char_list_return[i] in map_abrv_dict.keys():
            char_list_return[i] = map_abrv_dict[char_list_return[i]]
            
    return ' '.join(char_list_return)