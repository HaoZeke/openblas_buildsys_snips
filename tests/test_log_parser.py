from openblas_buildsys_snips.make.log_parser import (
    parse_cc_makelog,
    Define,
    CompilationInfo,
)



def test_single_command():
    log_data = """
    make[1]: Entering directory '/path/to/dir'
    cc -O2 -DDEFINE1 -DDEFINE2=value -Wall -UUNDEFINE1 -UUNDEFINE2 -c file.c -o file.o
    """
    result = parse_cc_makelog(log_data)
    assert len(result) == 1
    info = result[0]
    assert info.directory == '/path/to/dir'
    assert info.defines == [Define('DEFINE1'), Define('DEFINE2', 'value')]
    assert info.undefines == ['UNDEFINE1', 'UNDEFINE2']
    assert info.flags == ['-O2', '-Wall']
    assert info.input_files == ['file.c']
    assert info.output_symbol == 'file.o'


def test_multiple_commands():
    log_data = """
    make[1]: Entering directory '/path/to/dir1'
    cc -O2 -DDEFINE1 -Wall -UUNDEFINE1 -c file1.c -o file1.o
    make[1]: Leaving directory '/path/to/dir1'
    make[1]: Entering directory '/path/to/dir2'
    cc -O3 -DDEFINE2=value -g -UUNDEFINE2 -c file2.c -o file2.o
    """
    result = parse_cc_makelog(log_data)
    assert len(result) == 2
    info1 = result[0]
    assert info1.directory == '/path/to/dir1'
    assert info1.defines == [Define('DEFINE1')]
    assert info1.undefines == ['UNDEFINE1']
    assert info1.flags == ['-O2', '-Wall']
    assert info1.input_files == ['file1.c']
    assert info1.output_symbol == 'file1.o'

    info2 = result[1]
    assert info2.directory == '/path/to/dir2'
    assert info2.defines == [Define('DEFINE2', 'value')]
    assert info2.undefines == ['UNDEFINE2']
    assert info2.flags == ['-O3', '-g']
    assert info2.input_files == ['file2.c']
    assert info2.output_symbol == 'file2.o'


def test_no_flags():
    log_data = """
    make[1]: Entering directory '/path/to/dir'
    cc -c file.c -o file.o
    """
    result = parse_cc_makelog(log_data)
    assert len(result) == 1
    info = result[0]
    assert info.directory == '/path/to/dir'
    assert info.defines == []
    assert info.undefines == []
    assert info.flags == []
    assert info.input_files == ['file.c']
    assert info.output_symbol == 'file.o'


def test_with_includes():
    log_data = """
    make[1]: Entering directory '/path/to/dir'
    cc -Iinclude -O2 -DDEFINE1 -Wall -c file.c -o file.o
    """
    result = parse_cc_makelog(log_data)
    assert len(result) == 1
    info = result[0]
    assert info.directory == '/path/to/dir'
    assert info.defines == [Define('DEFINE1')]
    assert info.undefines == []
    assert info.flags == ['-Iinclude', '-O2', '-Wall']
    assert info.input_files == ['file.c']
    assert info.output_symbol == 'file.o'


def test_multiple_files():
    log_data = """
    make[1]: Entering directory '/path/to/dir'
    cc -O2 -DDEFINE1 -Wall -UUNDEFINE1 -c file1.c -c file2.c -o file.o
    """
    result = parse_cc_makelog(log_data)
    assert len(result) == 1
    info = result[0]
    assert info.directory == '/path/to/dir'
    assert info.defines == [Define('DEFINE1')]
    assert info.undefines == ['UNDEFINE1']
    assert info.flags == ['-O2', '-Wall']
    assert info.input_files == ['file1.c', 'file2.c']
    assert info.output_symbol == 'file.o'
