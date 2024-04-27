# Additional Design Issues

Some other points which are to be resolved eventually.

## ILP64 Convetions

One of the major issues with building BLAS interfaces has to do with the
ILP64 interface.

- [Debian mailing list RFC]
- [Intel usage instructions]

  [Debian mailing list RFC]: https://lists.debian.org/debian-science/2018/10/msg00030.html
  [Intel usage instructions]: https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2024-1/using-the-ilp64-interface-vs-lp64-interface.html

## Build duplication

This is primarily a [packaging / UX issue](https://pypackaging-native.github.io/key-issues/native-dependencies/blas_openmp/).
