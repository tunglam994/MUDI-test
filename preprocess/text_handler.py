import json
from formula_handler import process_formula

def process_drug_info(file_path):
    """
    Load and process drug information from JSON file.
    """
    
    with open(file_path, 'r') as f:
        drug_dict = json.load(f)
    
    for drug_id, drug_info in drug_dict.items():
        
        if 'description' in drug_info:
            if isinstance(drug_info['description'], dict):
                desc_text = []
                for section, content in drug_info['description'].items():
                    if isinstance(content, str):
                        desc_text.append(content)
                    elif isinstance(content, dict):
                        desc_text.extend(content.values())
                drug_dict[drug_id]['description'] = ' '.join(desc_text)
        
        if 'formula' in drug_info:
            try:
                drug_dict[drug_id]['formula'] = process_formula(drug_info['formula'])
            except:
                continue
                
    return drug_dict

if __name__ == "__main__":
    # Example usage
    file_path = 'drug_info.json'
    drug_info = process_drug_info(file_path)

    print(drug_info['DB00014'])
    
    
    
