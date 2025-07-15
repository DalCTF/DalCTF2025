flag = b"c4n7_b83113v3_1!_y0u_134rn3d_h0w_70_p47ch_4_p14n3"
K    = 0xEB ^ 0x74   # 0x9F
enc  = [(b ^ K) for b in flag]
print(", ".join(f"0x{x:02X}" for x in enc))
