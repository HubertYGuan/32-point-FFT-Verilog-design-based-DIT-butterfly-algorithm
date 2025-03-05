from numfi import numfi
from math import sin, cos, pi
from random import randbytes
import cocotb as ctb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from cocotb.runner import get_runner

from scipy.fft import fft
import numpy as np

def fixtonum(bn):
    bn = str(bn)
    intpart = -((int(bn[0:8], 2) ^ int("11111111", 2)) + 1) if (bn[0] == '1') else int(bn[0:8], 2)
    
    fracpart = int(bn[8:16], 2)
    fracpart /= (2**8)
    
    return intpart + fracpart

def numtofix(num):
    num *= (2**8)
    if num < 0:
        num = (1 << 16) + num
    return f"{num:016b}"

def fixtoint(bn):
    return int(fixtonum(bn) * (2**8))

# Real
twiddles_r = numfi([cos(2 * pi * i / 32) for i in range(0, 16)], 1, 16, 8)

# Imaginary
twiddles_i = numfi([sin(2 * pi * i / 32) for i in range(0, 16)], 1, 16, 8)

print(twiddles_r)
print(twiddles_i)

y = [2, 0, -4] * 10 + [1, 0]
y_bits = [num * (2**8) if num >= 0 else (2**16)+(num * (2**8)) for num in y]

fft_y = fft(y)
fft_y_r = numfi(np.real(fft_y), 1, 16, 8)
fft_y_i = numfi(np.imag(fft_y), 1, 16, 8)

@ctb.test()
async def top(top):
    ctb.start_soon(Clock(top.clk2, 1, units="ns").start())
    top.rst.value = 1
    
    for _ in range(2):
        await RisingEdge(top.clk2)
    
    top.rst.value = 0
    
    for _ in range(2):
        await RisingEdge(top.clk2)
        
    top.in0_r.value = y_bits[0]
    top.in1_r.value = y_bits[1]
    top.in2_r.value = y_bits[2]
    top.in3_r.value = y_bits[3]
    top.in4_r.value = y_bits[4]
    top.in5_r.value = y_bits[5]
    top.in6_r.value = y_bits[6]
    top.in7_r.value = y_bits[7]
    top.in8_r.value = y_bits[8]
    top.in9_r.value = y_bits[9]
    top.in10_r.value = y_bits[10]
    top.in11_r.value = y_bits[11]
    top.in12_r.value = y_bits[12]
    top.in13_r.value = y_bits[13]
    top.in14_r.value = y_bits[14]
    top.in15_r.value = y_bits[15]
    top.in16_r.value = y_bits[16]
    top.in17_r.value = y_bits[17]
    top.in18_r.value = y_bits[18]
    top.in19_r.value = y_bits[19]
    top.in20_r.value = y_bits[20]
    top.in21_r.value = y_bits[21]
    top.in22_r.value = y_bits[22]
    top.in23_r.value = y_bits[23]
    top.in24_r.value = y_bits[24]
    top.in25_r.value = y_bits[25]
    top.in26_r.value = y_bits[26]
    top.in27_r.value = y_bits[27]
    top.in28_r.value = y_bits[28]
    top.in29_r.value = y_bits[29]
    top.in30_r.value = y_bits[30]
    top.in31_r.value = y_bits[31]
    
    for _ in range(2):
        await RisingEdge(top.clk2)
    
    for _ in range(2):
        print(fixtonum(top.out0_r.value), fft_y_r[0], ':', fixtonum(top.out0_i.value), fft_y_i[0])
        print(fixtonum(top.out1_r.value), fft_y_r[1], ':', fixtonum(top.out1_i.value), fft_y_i[1])
        print(fixtonum(top.out2_r.value), fft_y_r[2], ':', fixtonum(top.out2_i.value), fft_y_i[2])
        print(fixtonum(top.out3_r.value), fft_y_r[3], ':', fixtonum(top.out3_i.value), fft_y_i[3])
        print(fixtonum(top.out4_r.value), fft_y_r[4], ':', fixtonum(top.out4_i.value), fft_y_i[4])
        print(fixtonum(top.out5_r.value), fft_y_r[5], ':', fixtonum(top.out5_i.value), fft_y_i[5])
        print(fixtonum(top.out6_r.value), fft_y_r[6], ':', fixtonum(top.out6_i.value), fft_y_i[6])
        print(fixtonum(top.out7_r.value), fft_y_r[7], ':', fixtonum(top.out7_i.value), fft_y_i[7])
        print(fixtonum(top.out8_r.value), fft_y_r[8], ':', fixtonum(top.out8_i.value), fft_y_i[8])
        print(fixtonum(top.out9_r.value), fft_y_r[9], ':', fixtonum(top.out9_i.value), fft_y_i[9])
        print(fixtonum(top.out10_r.value), fft_y_r[10], ':', fixtonum(top.out10_i.value), fft_y_i[10])
        print(fixtonum(top.out11_r.value), fft_y_r[11], ':', fixtonum(top.out11_i.value), fft_y_i[11])
        print(fixtonum(top.out12_r.value), fft_y_r[12], ':', fixtonum(top.out12_i.value), fft_y_i[12])
        print(fixtonum(top.out13_r.value), fft_y_r[13], ':', fixtonum(top.out13_i.value), fft_y_i[13])
        print(fixtonum(top.out14_r.value), fft_y_r[14], ':', fixtonum(top.out14_i.value), fft_y_i[14])
        print(fixtonum(top.out15_r.value), fft_y_r[15], ':', fixtonum(top.out15_i.value), fft_y_i[15])
        print(fixtonum(top.out16_r.value), fft_y_r[16], ':', fixtonum(top.out16_i.value), fft_y_i[16])
        print(fixtonum(top.out17_r.value), fft_y_r[17], ':', fixtonum(top.out17_i.value), fft_y_i[17])
        print(fixtonum(top.out18_r.value), fft_y_r[18], ':', fixtonum(top.out18_i.value), fft_y_i[18])
        print(fixtonum(top.out19_r.value), fft_y_r[19], ':', fixtonum(top.out19_i.value), fft_y_i[19])
        print(fixtonum(top.out20_r.value), fft_y_r[20], ':', fixtonum(top.out20_i.value), fft_y_i[20])
        print(fixtonum(top.out21_r.value), fft_y_r[21], ':', fixtonum(top.out21_i.value), fft_y_i[21])
        print(fixtonum(top.out22_r.value), fft_y_r[22], ':', fixtonum(top.out22_i.value), fft_y_i[22])
        print(fixtonum(top.out23_r.value), fft_y_r[23], ':', fixtonum(top.out23_i.value), fft_y_i[23])
        print(fixtonum(top.out24_r.value), fft_y_r[24], ':', fixtonum(top.out24_i.value), fft_y_i[24])
        print(fixtonum(top.out25_r.value), fft_y_r[25], ':', fixtonum(top.out25_i.value), fft_y_i[25])
        print(fixtonum(top.out26_r.value), fft_y_r[26], ':', fixtonum(top.out26_i.value), fft_y_i[26])
        print(fixtonum(top.out27_r.value), fft_y_r[27], ':', fixtonum(top.out27_i.value), fft_y_i[27])
        print(fixtonum(top.out28_r.value), fft_y_r[28], ':', fixtonum(top.out28_i.value), fft_y_i[28])
        print(fixtonum(top.out29_r.value), fft_y_r[29], ':', fixtonum(top.out29_i.value), fft_y_i[29])
        print(fixtonum(top.out30_r.value), fft_y_r[30], ':', fixtonum(top.out30_i.value), fft_y_i[30])
        print(fixtonum(top.out31_r.value), fft_y_r[31], ':', fixtonum(top.out31_i.value), fft_y_i[31])
        print(" ")
        print(" ")
        for _ in range(8):
            await RisingEdge(top.clk2)
    
    assert 0 == 0

def test_my_design_runner():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    
    sources = [f for f in listdir(proj_path.parent / "RTL") if isfile(join(proj_path.parent / "RTL", f))]
    print(sources)
    

    sources = [proj_path.parent / "RTL" / f"{file}" for file in sources]
    print(sources)

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="top",
    )

    runner.test(hdl_toplevel="top", test_module="top_TB,")


if __name__ == "__main__":
    test_my_design_runner()