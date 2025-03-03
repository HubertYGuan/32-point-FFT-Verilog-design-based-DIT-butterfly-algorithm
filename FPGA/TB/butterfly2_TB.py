from numfi import numfi
from math import sin, cos, pi
from random import randbytes
import cocotb as ctb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import os
from pathlib import Path
from cocotb.runner import get_runner

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

@ctb.test()
async def butterfly(butterfly):
    ctb.start_soon(Clock(butterfly.clk, 1, units="ns").start())
    butterfly.rst.value = 1
    
    for _ in range(2):
        await RisingEdge(butterfly.clk)
    
    butterfly.rst.value = 0
    
    for _ in range(2):
        await RisingEdge(butterfly.clk)
    # a is even input, b is odd input, probably has overflow issues
    a_r = f"{int.from_bytes(randbytes(2)):016b}"
    a_i = f"{int.from_bytes(randbytes(2)):016b}"
    b_r = f"{int.from_bytes(randbytes(2)):016b}"
    b_i = f"{int.from_bytes(randbytes(2)):016b}"
    for tw_r, tw_i in zip(twiddles_r, twiddles_i):
        print(fixtoint(a_r), fixtoint(a_i), fixtoint(b_r), fixtoint(b_i))
        print(tw_r)
        print(tw_i)
        butterfly.in0_r.value = fixtoint(a_r)
        butterfly.in0_i.value = fixtoint(a_i)
        butterfly.in1_r.value = fixtoint(b_r)
        butterfly.in1_i.value = fixtoint(b_i)
        butterfly.twiddle_r.value = int(tw_r[0] * (2**8))
        butterfly.twiddle_i.value = int(tw_i[0] * (2**8))
        for _ in range(2):
            await RisingEdge(butterfly.clk)
            
        print("butterfly in0_r", butterfly.in0_r.value)
        
        # + not - since using the form e^-iz not e^iz
        assert fixtonum(butterfly.out0_r.value) == numfi(fixtonum(a_r) + fixtonum(b_r) * tw_r + fixtonum(b_i) * tw_i, 1, 16, 8)

def test_my_design_runner():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path.parent / "RTL" / "butterfly2_n.v", proj_path.parent / "RTL" / "adder3_n.v", proj_path.parent / "RTL" / "get_negative_n.v", proj_path.parent / "RTL" / "multiplier_n.v"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="butterfly2",
    )

    runner.test(hdl_toplevel="butterfly2", test_module="butterfly2_TB,")


if __name__ == "__main__":
    test_my_design_runner()