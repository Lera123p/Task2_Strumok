
#Cut redundant bites (for using in a_mul)
correct_mask64 = 0xFFFFFFFFFFFFFFFF 

#Return bites + cut redundant
def invert(value):
    return (~value) & correct_mask64




# Preparation
def loading_strumok_tables(filename="strumok_tables.c"):
    tables = {}
    
    try:
        file = open(filename, "r", encoding="utf-8")
        all_lines = file.readlines() 
        file.close()
    except FileNotFoundError:
        print(f"Error: file {filename} not found!")
        return None
    
    find_table_names = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'alpha_mul', 'alphainv_mul']

    for name in find_table_names:
        all_table_numbers = []  
        check_finding_state = False     
        find_word = "strumok_" + name
        
        for line in all_lines:
            if check_finding_state == False: #in case if we find header firstly than table
                if find_word in line:
                    check_finding_state = True 
            
            elif check_finding_state == True: #in case if we find table firstly than header

                delete_redundant = line.replace("ULL", "").replace("}", "").replace(";", "").replace("\n", "").strip()
                delete_redundant = delete_redundant.split("//")[0]
                into_pieces = delete_redundant.split(",")
       
                for item in into_pieces: #cut finding pieces into numbers
                    item = item.strip()
                    
                    if item != "": 
                        change_to_number = int(item, 16)
                        all_table_numbers.append(change_to_number)

                if "}" in line:
                    check_finding_state = False
                    break
       
        tables[name] = all_table_numbers
        
    return tables
