
#Cut redundant bites (for using in a_mul)
correct_mask64 = 0xFFFFFFFFFFFFFFFF 

#Return bites + cut redundant
def invert(value):
    return (~value) & correct_mask64


#Rewrited example into Python from use-example.c
def a_mul(x, tables):
    return ((x << 8) & correct_mask64) ^ tables['alpha_mul'][x >> 56]

def ainv_mul(x, tables):
    return (x >> 8) ^ tables['alphainv_mul'][x & 0xff]

def transform_T(x, tables):
    return (tables['T0'][x & 0xff] ^
            tables['T1'][(x >> 8) & 0xff] ^
            tables['T2'][(x >> 16) & 0xff] ^
            tables['T3'][(x >> 24) & 0xff] ^
            tables['T4'][(x >> 32) & 0xff] ^
            tables['T5'][(x >> 40) & 0xff] ^
            tables['T6'][(x >> 48) & 0xff] ^
            tables['T7'][(x >> 56) & 0xff])

def fsm_func(x, y, z):
    return ((x + y) & correct_mask64) ^ z




# Preparation
def loading_strumok_tables(filename="strumok_tables.c"):
    tables = {}
    
    try:
        file = open(filename, "r", encoding="utf-8")
        all_lines = file.readlines() 
        file.close()
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено!")
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


#Strumok and Initialization

class Strumok:
  def __init__(self, tables):
      self.s = [0] * 16 
      self.r1 = 0        
      self.r2 = 0       
      self.tables = tables


  def change_state(self, is_mixing):
    prev_r1  = self.r1
    prev_r2  = self.r2
    prev_s0  = self.s[0]
    prev_s11 = self.s[11]
    prev_s13 = self.s[13]
    prev_s15 = self.s[15]

    self.r2 = transform_T(prev_r1, self.tables)
    self.r1 = (prev_r2 + prev_s13) & correct_mask64

    
    part_1 = a_mul(prev_s0, self.tables)
    part_2 = ainv_mul(prev_s11, self.tables)
    part_3 = prev_s13
    
    calculate_parts = part_1 ^ part_2 ^ part_3
    
    if is_mixing == True: #in case if Strumok is only warming up
        calculate_parts = calculate_parts ^ fsm_func(prev_s15, prev_r1, prev_r2)

    for i in range(15):
        self.s[i] = self.s[i + 1]

    self.s[15] = calculate_parts


  def init_256(self, key, IV):
        self.r1 = 0
        self.r2 = 0
        
        self.s[0]  = key[3] ^ IV[0]
        self.s[1]  = key[2]
        self.s[2]  = key[1] ^ IV[1]
        self.s[3]  = key[0] ^ IV[2]
        self.s[4]  = key[3]
        self.s[5]  = key[2] ^ IV[3]
        self.s[6]  = invert(key[1])
        self.s[7]  = invert(key[0])
        self.s[8]  = key[3]
        self.s[9]  = key[2]
        self.s[10] = invert(key[1])
        self.s[11] = key[0]
        self.s[12] = key[3]
        self.s[13] = invert(key[2])
        self.s[14] = key[1]
        self.s[15] = invert(key[0])
        
        for i in range(32):
            self.change_state(is_mixing=True)
            
        self.change_state(is_mixing=False)

  def get_number64(self):
        blend_last_cell = fsm_func(self.s[15], self.r1, self.r2)
  
        z = blend_last_cell ^ self.s[0]
        
        self.change_state(is_mixing=False)
        return z


#Check if everything is okey
if __name__ == "__main__":
    print("Loading data from teacher...")
    my_tables = loading_strumok_tables("strumok_tables.c")
    
    if my_tables:
        new_cypher_machine = Strumok(my_tables)
        test_key = [0, 0, 0, 0x8000000000000000]
        test_iv  = [0, 0, 0, 0]
        
        print("Warming up...32 revs...")
        new_cypher_machine.init_256(test_key, test_iv)
        
        print("Results:")
        for i in range(10):
            z_result = new_cypher_machine.get_number64()
            print(f"Z_{i}: {z_result:016x}")
            
        print("Everything is okey!")