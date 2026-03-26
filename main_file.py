from utils import loading_strumok_tables
from strumok import Strumok


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