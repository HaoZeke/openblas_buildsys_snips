from openblas_buildsys_snips.cmake.netlib import cmake_netlib_meson


def test_basic_netlib():
    lines = """set(DSLASRC
    sgetrf.f sgetrf2.f sgetrs.f sisnan.f slaisnan.f slaswp.f spotrf.f spotrf2.f
    spotrs.f)
    """
    meson_output = cmake_netlib_meson(lines.split("\n"))
    expect = """_dslasrc = [
    'sgetrf.f',
    'sgetrf2.f',
    'sgetrs.f',
    'sisnan.f',
    'slaisnan.f',
    'slaswp.f',
    'spotrf.f',
    'spotrf2.f',
    'spotrs.f'
]"""
    assert meson_output == expect
