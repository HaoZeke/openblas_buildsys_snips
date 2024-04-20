# Additional Resources

The cannonical resources[^1] for OpenBLAS are of course the [OpenBLAS wiki] and
the the [Netlib BLAS] documentation, especially [the bibliography] and the
[final BLAS techincal forum standard].

- Naming conventions are [noted here]
- The reference documentation [has the scheme too]
- Also elaborated in the [embedded context here]

## Conventions and Implementations

Beyond the standard `netlib` reference, here are some more common
implementations of interest, with above average documentation[^2]:

- [Intel oneAPI MKL]
- [Arm performance library implementation] (`armpl.h`)
- The IBM [Engineering and Scientific Subroutine Library]
- SGI's [Scientific Computing Software Library](https://techpubs.jurassic.nl/library/manuals/4000/007-4325-001/sgi_html/ch02.html)

## Pedagogical Work

Here are some additional links for BLAS related information:

- Basic [scientific python tutorial], with a [notebook here]

- This lecture on [Numerical Linear Algebra Software]

- Another lecture on [Numerical Linear Algebra Background]

- Some [context on CPU performance]

[^1]: Barring the [wiki page], which can be a good place to start too.
[^2]: [This post] has some NumPy specific context, as does [the documentation]

[OpenBLAS wiki]: https://github.com/OpenMathLib/OpenBLAS/wiki
[Netlib BLAS]: https://netlib.org/blas/
[the bibliography]: https://www.netlib.org/lapack/lug/node151.html
[final BLAS techincal forum standard]: https://www.netlib.org/blas/blast-forum/
[noted here]:
  https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-c/2024-1/naming-conventions-for-blas-routines.html
[has the scheme too]: https://netlib.org/lapack/lug/node24.html
[embedded context here]: https://blasfeo.syscop.de/docs/naming/
[Intel oneAPI MKL]:
  https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-c/2024-1/blas-routines.html
[Arm performance library implementation]:
  https://developer.arm.com/documentation/101004/2310/BLAS-Basic-Linear-Algebra-Subprograms/BLAS-overview?lang=en
[Engineering and Scientific Subroutine Library]:
  https://www.ibm.com/docs/en/essl/6.2?topic=subprograms-overview-linear-algebra
[scientific python tutorial]:
  https://caam37830.github.io/book/02_linear_algebra/blas_lapack.html
[notebook here]:
  https://colab.research.google.com/github/caam37830/book/blob/master/02_linear_algebra/blas_lapack.ipynb
[Numerical Linear Algebra Software]:
  https://see.stanford.edu/materials/lsocoee364b/AdditionalLecture3-num-lin-alg-software.pdf
[Numerical Linear Algebra Background]:
  http://faculty.bicmr.pku.edu.cn/~wenzw/opt2015/09_num-lin-alg_new.pdf
[context on CPU performance]: https://cs.stanford.edu/people/shadjis/blas.html
[wiki page]: https://www.wikiwand.com/en/Basic_Linear_Algebra_Subprograms
[This post]: https://superfastpython.com/numpy-blas-lapack-libraries/
[the documentation]: https://numpy.org/devdocs/building/blas_lapack.html
