from utils import loading_strumok_tables
from strumok import Strumok

def testing(tables):
    print("Starting running tests")
    
    #Cтрумок-256 (ДСТУ - Додаток Д.1.1)
    print("Testing Strumok-256...")
    cypher_256 = Strumok(tables)
    
    key_256 = [0, 0, 0, 0x8000000000000000]
    iv_256  = [0, 0, 0, 0]
    
    #Expected hamma results from standart
    z_256 = [
        0xe442d15345dc66ca, 0xf47d700ecc66408a,
        0xb4cb284b5477e641, 0xa2afc9092e4124b0,
        0x728e5fa26b11a7d9, 0xe6a7b9288c68f972,
        0x70eb3606de8ba44c, 0xaced7956bd3e3de7
    ]
    
    cypher_256.init_256(key_256, iv_256)
    
    for i in range(8):
        z_result = cypher_256.get_number64()
        expected_results = z_256[i]
        
        # Handling error if results are not equal
        if z_result != expected_results:
            print(f"Error within Z_{i}!")
            print(f"Expected: {hex(expected_results)}")
            print(f"Got:  {hex(z_result)}")
            return
            
    print("Congratulations! All results are equal\n")


    #Струмок-512 (ДСТУ - Додаток Д.2.1)
    print("Testing Strumok-512...")
    cypher_512 = Strumok(tables)
    
    key_512 = [0, 0, 0, 0, 0, 0, 0, 0x8000000000000000]
    iv_512  = [0, 0, 0, 0]
    
    #Expected hamma results from standart
    z_512 = [
        0xf5b9ab51100f8317, 0x898ef2086a4af395,
        0x59571fecb5158d0b, 0xb7c45b6744c71fbb,
        0xff2efcf05d8d8db9, 0x7a585871e5c419c0,
        0x6b5c4691b9125e71, 0xa55be7d2b358ec6e
    ]
    
    
    cypher_512.init_512(key_512, iv_512)
        
    for i in range(8):
        z_result = cypher_512.get_number64()
        expected_results = z_512[i]
            
    # Handling error if results are not equal
    if z_result != expected_results:
        print(f"Error within Z_{i}!")
        print(f"Expected: {hex(expected_results)}")
        print(f"Got:  {hex(z_result)}")
        return
                
    print("Congratulations! All results are equal\n")
        

if __name__ == "__main__":
    print("Loading data...")
    my_tables = loading_strumok_tables("strumok_tables.c")
    
    if my_tables:
        testing(my_tables)
    else:
        print("Data loading error")