from numfi import numfi
from math import sin, cos, pi
import cocotb as ctb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import os
from pathlib import Path
from cocotb.runner import get_runner

def fixtoint(bn):
    bn = str(bn)
    intpart = -((int(bn[0:8], 2) ^ int("11111111", 2)) + 1) if (bn[0] == '1') else int(bn[0:8], 2)
    print(intpart, int(bn[0:8], 2), 255 ^ int("11111111", 2))
    
    intpart *= (2**8)
    
    fracpart = int(bn[8:16], 2)
    
    return intpart + fracpart

# Real
# twiddles = numfi([cos(2 * pi * i / 32) for i in range(0, 16)], 1, 16, 8)

# Imaginary
twiddles = numfi([sin(2 * pi * i / 32) for i in range(0, 16)], 1, 16, 8)

twiddles *= (2**8)
print(twiddles)

@ctb.test()
async def rom(rom):
    ctb.start_soon(Clock(rom.clk, 1, units="ns").start())
    rom.rst.value = 1
    
    for _ in range(2):
        await RisingEdge(rom.clk)
        
    rom.rst.value = 0
    
    for _ in range(2):
        await RisingEdge(rom.clk)
    print(twiddles[0], type(twiddles[0]))
    '''
    assert (fixtoint(rom.reg0_r.value ) == twiddles[0])
    assert (fixtoint(rom.reg1_r.value ) == twiddles[1])
    assert (fixtoint(rom.reg2_r.value ) == twiddles[2])
    assert (fixtoint(rom.reg3_r.value ) == twiddles[3])
    assert (fixtoint(rom.reg4_r.value ) == twiddles[4])
    assert (fixtoint(rom.reg5_r.value ) == twiddles[5])
    assert (fixtoint(rom.reg6_r.value ) == twiddles[6])
    assert (fixtoint(rom.reg7_r.value ) == twiddles[7])
    assert (fixtoint(rom.reg8_r.value ) == twiddles[8])
    assert (fixtoint(rom.reg9_r.value ) == twiddles[9])
    assert (fixtoint(rom.reg10_r.value) == twiddles[10])
    assert (fixtoint(rom.reg11_r.value) == twiddles[11])
    assert (fixtoint(rom.reg12_r.value) == twiddles[12])
    assert (fixtoint(rom.reg13_r.value) == twiddles[13])
    assert (fixtoint(rom.reg14_r.value) == twiddles[14])
    assert (fixtoint(rom.reg15_r.value) == twiddles[15])
    '''
    assert (fixtoint(rom.reg0_i.value ) == twiddles[0])
    assert (fixtoint(rom.reg1_i.value ) == twiddles[1])
    assert (fixtoint(rom.reg2_i.value ) == twiddles[2])
    assert (fixtoint(rom.reg3_i.value ) == twiddles[3])
    assert (fixtoint(rom.reg4_i.value ) == twiddles[4])
    assert (fixtoint(rom.reg5_i.value ) == twiddles[5])
    assert (fixtoint(rom.reg6_i.value ) == twiddles[6])
    assert (fixtoint(rom.reg7_i.value ) == twiddles[7])
    assert (fixtoint(rom.reg8_i.value ) == twiddles[8])
    assert (fixtoint(rom.reg9_i.value ) == twiddles[9])
    assert (fixtoint(rom.reg10_i.value) == twiddles[10])
    assert (fixtoint(rom.reg11_i.value) == twiddles[11])
    assert (fixtoint(rom.reg12_i.value) == twiddles[12])
    assert (fixtoint(rom.reg13_i.value) == twiddles[13])
    assert (fixtoint(rom.reg14_i.value) == twiddles[14])
    assert (fixtoint(rom.reg15_i.value) == twiddles[15])
    
def test_my_design_runner():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    # sources = [proj_path / "RTL" / "twiddle_rom_real_n.v"]
    sources = [proj_path.parent / "RTL" / "twiddle_rom_imag_n.v"]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        # hdl_toplevel="twiddle_rom_real",
        hdl_toplevel="twiddle_rom_imag",
    )

    # runner.test(hdl_toplevel="twiddle_rom_real", test_module="twiddle_rom_TB,")
    runner.test(hdl_toplevel="twiddle_rom_imag", test_module="twiddle_rom_TB,")


if __name__ == "__main__":
    test_my_design_runner()