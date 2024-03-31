import openblas_buildsys_snips.make.blas_kernel as opbk
import openblas_buildsys_snips._utils as oputil


class TestMakefileToSym:
    def test_l2_with_base(self, datadir):
        lines = (datadir / "Makefile.L2").read_text()
        expected_ger = {
            "base": "ger",
            "modes": {
                "s": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
                "d": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
                "q": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
                "c": {
                    "dir": "generic",
                    "kernel": "ger_k.c",
                    "exts": ["u_k", "c_k", "v_k", "d_k"],
                },
                "z": {
                    "dir": "generic",
                    "kernel": "ger_k.c",
                    "exts": ["u_k", "c_k", "v_k", "d_k"],
                },
                "x": {
                    "dir": "generic",
                    "kernel": "ger_k.c",
                    "exts": ["u_k", "c_k", "v_k", "d_k"],
                },
            },
        }
        expected_geru = {
            "base": "geru",
            "modes": {
                "c": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
                "z": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
                "x": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            },
        }
        expected_gerc = {
            "base": "gerc",
            "modes": {
                "c": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
                "z": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
                "x": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            },
        }
        assert (
            opbk.parse_makefile_to_sym(
                lines.split("\n"), "generic", "ger_k.c", base="ger"
            )
            == expected_ger
        )
        assert (
            opbk.parse_makefile_to_sym(
                lines.split("\n"), "generic", "zger.c", base="geru"
            )
            == expected_geru
        )
        assert (
            opbk.parse_makefile_to_sym(
                lines.split("\n"), "generic", "zger.c", base="gerc"
            )
            == expected_gerc
        )

    def test_l1_with_base(self, datadir):
        lines = (datadir / "Makefile.L1").read_text()
        expected = {
            "base": "axpby",
            "modes": {
                "s": {"dir": "arm", "kernel": "axpby.c", "exts": ["_k"]},
                "d": {"dir": "arm", "kernel": "axpby.c", "exts": ["_k"]},
                "c": {"dir": "arm", "kernel": "axpby.c", "exts": ["_k"]},
                "z": {"dir": "arm", "kernel": "axpby.c", "exts": ["_k"]},
            },
        }
        assert (
            opbk.parse_makefile_to_sym(
                lines.split("\n"), "arm", "axpby.c", base="axpby"
            )
            == expected
        )

    def test_l2_without_base(self):
        lines = [
            "$(KDIR)zsymv_U$(TSUFFIX).$(SUFFIX)  $(KDIR)zsymv_U$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZSYMV_U_KERNEL)   $(ZSYMV_U_PARAM)",
            "$(KDIR)ssymv_L$(TSUFFIX).$(SUFFIX)  $(KDIR)ssymv_L$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SSYMV_L_KERNEL)  $(SSYMV_L_PARAM)",
        ]
        expected = {
            "base": "symv",
            "modes": {
                "z": {"dir": "generic", "kernel": "zsymv_k.c", "exts": ["_U"]},
                "s": {"dir": "generic", "kernel": "zsymv_k.c", "exts": ["_L"]},
            },
        }
        assert opbk.parse_makefile_to_sym(lines, "generic", "zsymv_k.c") == expected


class TestParseCompile:
    def test_basic_parse(self):
        expected = [
            {
                "name": "srot_k",
                "undef": ["COMPLEX", "COMPLEX", "DOUBLE"],
                "def": [],
                "addl": ["FMAFLAG"],
            },
            {
                "name": "drot_k",
                "undef": ["COMPLEX", "COMPLEX"],
                "def": ["DOUBLE"],
                "addl": ["FMAFLAG"],
            },
            {
                "name": "qrot_k",
                "undef": ["COMPLEX", "COMPLEX"],
                "def": ["XDOUBLE"],
                "addl": [],
            },
            {
                "name": "csrot_k",
                "undef": ["DOUBLE"],
                "def": ["COMPLEX", "COMPLEX"],
                "addl": [],
            },
        ]

        lines = """
        $(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL)
        	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@

        $(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL)
        	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@

        $(KDIR)qrot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)qrot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(QROTKERNEL)
        	$(CC) -c $(CFLAGS) -UCOMPLEX -UCOMPLEX -DXDOUBLE $< -o $@

        $(KDIR)csrot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)csrot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CROTKERNEL)
        	$(CC) -c $(CFLAGS) -DCOMPLEX -DCOMPLEX -UDOUBLE  $< -o $@
        """.strip().split(
            "\n"
        )

        results = opbk.parse_compilation_commands(oputil.pair_suffix_lines(lines), "rot")

        assert len(results) == len(
            expected
        ), "The number of configurations does not match the expected count."

        for exp in expected:
            assert exp in results, f"Expected configuration not found in results: {exp}"

    def test_define_with_num_and_eq(self):
        lines = [
            "$(KDIR)cgemm_small_kernel_b0_cr$(TSUFFIX).$(SUFFIX) : $(KERNELDIR)/$(CGEMM_SMALL_K_B0_TN)	$(CC) $(CFLAGS) -c -UDOUBLE -DCOMPLEX -DCR=CR -DB0 $< -o $@",
        ]
        expected = [
            {
                "name": "cgemm_small_kernel_b0_cr",
                "undef": ["DOUBLE"],
                "def": ["COMPLEX", "CR=CR", "B0"],
                "addl": [],
            }
        ]
        assert opbk.parse_compilation_commands(lines, "gemm") == expected
