import time
from utils import loading_strumok_tables
from strumok import Strumok

def testing_speed(cypher, name):
    print(f"Starting of test speed {name}...")
    
    start = time.time()
    for i in range(500000):
        cypher.get_number64()
    
    end = time.time()
    
    seconds = end - start
    megabytes = (500000 * 8) / 1048576 # 1 bit = 8 bytes, 1 megabyte = 1048575 bytes 
    
    print(f"Speed results: {megabytes / seconds:.2f} Mb/s")


if __name__ == "__main__":
    tables = loading_strumok_tables("strumok_tables.c")
    
    if tables:
        # Струмок-256
        c_256 = Strumok(tables)
        c_256.init_256([0, 0, 0, 0], [0, 0, 0, 0])
        testing_speed(c_256, "Струмок-256")
        
        # Струмок-512
        c_512 = Strumok(tables)
        c_512.init_512([0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0])
        testing_speed(c_512, "Струмок-512")