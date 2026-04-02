from utils import correct_mask64, invert
from main_math import a_mul, ainv_mul, transform_T, fsm_func


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
        
        for _ in range(32):
            self.change_state(is_mixing=True)
            
        self.change_state(is_mixing=False)

  def init_512(self, key, IV):
        self.r1 = 0
        self.r2 = 0
        
        self.s[0]  = key[7] ^ IV[0]
        self.s[1]  = key[6]
        self.s[2]  = key[5] ^ IV[1]
        self.s[3]  = key[4] ^ IV[2]
        self.s[4]  = key[3]
        self.s[5]  = key[2] ^ IV[3]
        self.s[6]  = invert(key[1])
        self.s[7]  = invert(key[0])
        
        self.s[8]  = key[7]
        self.s[9]  = key[6]
        self.s[10] = invert(key[5])
        self.s[11] = key[4]
        self.s[12] = key[3]
        self.s[13] = invert(key[2])
        self.s[14] = key[1]
        self.s[15] = invert(key[0])
        
        for _ in range(32):
            self.change_state(is_mixing=True)
            
        self.change_state(is_mixing=False)

  def get_number64(self):
        blend_last_cell = fsm_func(self.s[15], self.r1, self.r2)
  
        z = blend_last_cell ^ self.s[0]
        
        self.change_state(is_mixing=False)
        return z


