ssmod = import('sourceset')

laswp_ss = ssmod.source_set()
zlaswp_ss = ssmod.source_set()

laswp_ss.add(when: ['ARCH_X86_64', 'HASWELL'], if_true: files('laswp_k.c'))
zlaswp_ss.add(when: ['ARCH_X86_64', 'HASWELL'], if_true: files('zlaswp_k.c'))

laswp_ss.add(when: ['ARCH_X86_64', 'CORE2'], if_true: files('laswp_k_2.c'))
zlaswp_ss.add(when: ['ARCH_X86_64', 'CORE2'], if_true: files('zlaswp_k_2.c'))

# So the targets don't have to be explicitly false
laswap_conf = laswp_ss.apply(conf_hdat, strict: false)
zlaswap_conf = zlaswp_ss.apply(conf_hdat, strict: false)

_lapack_roots += {
    'base': '?laswp_*',
    '_types': ['s', 'd'],
    '_meth': {'plus': ['-UMINUS'], 'minus': ['-DMINUS']},
    'ss': laswap_conf.sources(),
}
_lapack_roots += {
    'base': '?laswp_*',
    '_types': ['c', 'z'],
    '_meth': {'plus': ['-UMINUS'], 'minus': ['-DMINUS']},
    'ss': zlaswap_conf.sources(),
}
