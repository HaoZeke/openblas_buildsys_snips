#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <complex.h>
#ifdef complex
#undef complex
#endif
#ifdef I
#undef I
#endif

#if defined(_WIN64)
typedef long long BLASLONG;
typedef unsigned long long BLASULONG;
#else
typedef long BLASLONG;
typedef unsigned long BLASULONG;
#endif

#ifdef LAPACK_ILP64
typedef BLASLONG blasint;
#if defined(_WIN64)
#define blasabs(x) llabs(x)
#else
#define blasabs(x) labs(x)
#endif
#else
typedef int blasint;
#define blasabs(x) abs(x)
#endif

typedef blasint integer;

typedef unsigned int uinteger;
typedef char *address;
typedef short int shortint;
typedef float real;
typedef double doublereal;
typedef struct { real r, i; } complex;
typedef struct { doublereal r, i; } doublecomplex;
#ifdef _MSC_VER
static inline _Fcomplex Cf(complex *z) {_Fcomplex zz={z->r , z->i}; return zz;}
static inline _Dcomplex Cd(doublecomplex *z) {_Dcomplex zz={z->r , z->i};return zz;}
static inline _Fcomplex * _pCf(complex *z) {return (_Fcomplex*)z;}
static inline _Dcomplex * _pCd(doublecomplex *z) {return (_Dcomplex*)z;}
#else
static inline _Complex float Cf(complex *z) {return z->r + z->i*_Complex_I;}
static inline _Complex double Cd(doublecomplex *z) {return z->r + z->i*_Complex_I;}
static inline _Complex float * _pCf(complex *z) {return (_Complex float*)z;}
static inline _Complex double * _pCd(doublecomplex *z) {return (_Complex double*)z;}
#endif
#define pCf(z) (*_pCf(z))
#define pCd(z) (*_pCd(z))
typedef char integer1;

#define TRUE_ (1)
#define FALSE_ (0)

/* Extern is for use with -E */
#ifndef Extern
#define Extern extern
#endif

/* I/O stuff */

typedef int flag;
typedef int ftnlen;
typedef int ftnint;

/*external read, write*/
typedef struct
{	flag cierr;
	ftnint ciunit;
	flag ciend;
	char *cifmt;
	ftnint cirec;
} cilist;

/*internal read, write*/
typedef struct
{	flag icierr;
	char *iciunit;
	flag iciend;
	char *icifmt;
	ftnint icirlen;
	ftnint icirnum;
} icilist;

/*open*/
typedef struct
{	flag oerr;
	ftnint ounit;
	char *ofnm;
	ftnlen ofnmlen;
	char *osta;
	char *oacc;
	char *ofm;
	ftnint orl;
	char *oblnk;
} olist;

/*close*/
typedef struct
{	flag cerr;
	ftnint cunit;
	char *csta;
} cllist;

/*rewind, backspace, endfile*/
typedef struct
{	flag aerr;
	ftnint aunit;
} alist;

/* inquire */
typedef struct
{	flag inerr;
	ftnint inunit;
	char *infile;
	ftnlen infilen;
	ftnint	*inex;	/*parameters in standard's order*/
	ftnint	*inopen;
	ftnint	*innum;
	ftnint	*innamed;
	char	*inname;
	ftnlen	innamlen;
	char	*inacc;
	ftnlen	inacclen;
	char	*inseq;
	ftnlen	inseqlen;
	char 	*indir;
	ftnlen	indirlen;
	char	*infmt;
	ftnlen	infmtlen;
	char	*inform;
	ftnint	informlen;
	char	*inunf;
	ftnlen	inunflen;
	ftnint	*inrecl;
	ftnint	*innrec;
	char	*inblank;
	ftnlen	inblanklen;
} inlist;

#define VOID void

union Multitype {	/* for multiple entry points */
	integer1 g;
	shortint h;
	integer i;
	/* longint j; */
	real r;
	doublereal d;
	complex c;
	doublecomplex z;
	};

typedef union Multitype Multitype;

struct Vardesc {	/* for Namelist */
	char *name;
	char *addr;
	ftnlen *dims;
	int  type;
	};
typedef struct Vardesc Vardesc;

struct Namelist {
	char *name;
	Vardesc **vars;
	int nvars;
	};
typedef struct Namelist Namelist;

#define abs(x) ((x) >= 0 ? (x) : -(x))
#define dabs(x) (fabs(x))
#define f2cmin(a,b) ((a) <= (b) ? (a) : (b))
#define f2cmax(a,b) ((a) >= (b) ? (a) : (b))
#define dmin(a,b) (f2cmin(a,b))
#define dmax(a,b) (f2cmax(a,b))
#define bit_test(a,b)	((a) >> (b) & 1)
#define bit_clear(a,b)	((a) & ~((uinteger)1 << (b)))
#define bit_set(a,b)	((a) |  ((uinteger)1 << (b)))

#define abort_() { sig_die("Fortran abort routine called", 1); }
#define c_abs(z) (cabsf(Cf(z)))
#define c_cos(R,Z) { pCf(R)=ccos(Cf(Z)); }
#ifdef _MSC_VER
#define c_div(c, a, b) {Cf(c)._Val[0] = (Cf(a)._Val[0]/Cf(b)._Val[0]); Cf(c)._Val[1]=(Cf(a)._Val[1]/Cf(b)._Val[1]);}
#define z_div(c, a, b) {Cd(c)._Val[0] = (Cd(a)._Val[0]/Cd(b)._Val[0]); Cd(c)._Val[1]=(Cd(a)._Val[1]/df(b)._Val[1]);}
#else
#define c_div(c, a, b) {pCf(c) = Cf(a)/Cf(b);}
#define z_div(c, a, b) {pCd(c) = Cd(a)/Cd(b);}
#endif
#define c_exp(R, Z) {pCf(R) = cexpf(Cf(Z));}
#define c_log(R, Z) {pCf(R) = clogf(Cf(Z));}
#define c_sin(R, Z) {pCf(R) = csinf(Cf(Z));}
//#define c_sqrt(R, Z) {*(R) = csqrtf(Cf(Z));}
#define c_sqrt(R, Z) {pCf(R) = csqrtf(Cf(Z));}
#define d_abs(x) (fabs(*(x)))
#define d_acos(x) (acos(*(x)))
#define d_asin(x) (asin(*(x)))
#define d_atan(x) (atan(*(x)))
#define d_atn2(x, y) (atan2(*(x),*(y)))
#define d_cnjg(R, Z) { pCd(R) = conj(Cd(Z)); }
#define r_cnjg(R, Z) { pCf(R) = conjf(Cf(Z)); }
#define d_cos(x) (cos(*(x)))
#define d_cosh(x) (cosh(*(x)))
#define d_dim(__a, __b) ( *(__a) > *(__b) ? *(__a) - *(__b) : 0.0 )
#define d_exp(x) (exp(*(x)))
#define d_imag(z) (cimag(Cd(z)))
#define r_imag(z) (cimagf(Cf(z)))
#define d_int(__x) (*(__x)>0 ? floor(*(__x)) : -floor(- *(__x)))
#define r_int(__x) (*(__x)>0 ? floor(*(__x)) : -floor(- *(__x)))
#define d_lg10(x) ( 0.43429448190325182765 * log(*(x)) )
#define r_lg10(x) ( 0.43429448190325182765 * log(*(x)) )
#define d_log(x) (log(*(x)))
#define d_mod(x, y) (fmod(*(x), *(y)))
#define u_nint(__x) ((__x)>=0 ? floor((__x) + .5) : -floor(.5 - (__x)))
#define d_nint(x) u_nint(*(x))
#define u_sign(__a,__b) ((__b) >= 0 ? ((__a) >= 0 ? (__a) : -(__a)) : -((__a) >= 0 ? (__a) : -(__a)))
#define d_sign(a,b) u_sign(*(a),*(b))
#define r_sign(a,b) u_sign(*(a),*(b))
#define d_sin(x) (sin(*(x)))
#define d_sinh(x) (sinh(*(x)))
#define d_sqrt(x) (sqrt(*(x)))
#define d_tan(x) (tan(*(x)))
#define d_tanh(x) (tanh(*(x)))
#define i_abs(x) abs(*(x))
#define i_dnnt(x) ((integer)u_nint(*(x)))
#define i_len(s, n) (n)
#define i_nint(x) ((integer)u_nint(*(x)))
#define i_sign(a,b) ((integer)u_sign((integer)*(a),(integer)*(b)))
#define pow_dd(ap, bp) ( pow(*(ap), *(bp)))
#define pow_si(B,E) spow_ui(*(B),*(E))
#define pow_ri(B,E) spow_ui(*(B),*(E))
#define pow_di(B,E) dpow_ui(*(B),*(E))
#define pow_zi(p, a, b) {pCd(p) = zpow_ui(Cd(a), *(b));}
#define pow_ci(p, a, b) {pCf(p) = cpow_ui(Cf(a), *(b));}
#define pow_zz(R,A,B) {pCd(R) = cpow(Cd(A),*(B));}
#define s_cat(lpp, rpp, rnp, np, llp) { 	ftnlen i, nc, ll; char *f__rp, *lp; 	ll = (llp); lp = (lpp); 	for(i=0; i < (int)*(np); ++i) {         	nc = ll; 	        if((rnp)[i] < nc) nc = (rnp)[i]; 	        ll -= nc;         	f__rp = (rpp)[i]; 	        while(--nc >= 0) *lp++ = *(f__rp)++;         } 	while(--ll >= 0) *lp++ = ' '; }
#define s_cmp(a,b,c,d) ((integer)strncmp((a),(b),f2cmin((c),(d))))
#define s_copy(A,B,C,D) { int __i,__m; for (__i=0, __m=f2cmin((C),(D)); __i<__m && (B)[__i] != 0; ++__i) (A)[__i] = (B)[__i]; }
#define sig_die(s, kill) { exit(1); }
#define s_stop(s, n) {exit(0);}
#define z_abs(z) (cabs(Cd(z)))
#define z_exp(R, Z) {pCd(R) = cexp(Cd(Z));}
#define z_sqrt(R, Z) {pCd(R) = csqrt(Cd(Z));}
#define myexit_() break;
#define mycycle() continue;
#define myceiling(w) {ceil(w)}
#define myhuge(w) {HUGE_VAL}
//#define mymaxloc_(w,s,e,n) {if (sizeof(*(w)) == sizeof(double)) dmaxloc_((w),*(s),*(e),n); else dmaxloc_((w),*(s),*(e),n);}
#define mymaxloc(w,s,e,n) {dmaxloc_(w,*(s),*(e),n)}

/* procedure parameter types for -A and -C++ */




/* Table of constant values */

static complex c_b1 = {0.f,0.f};
static complex c_b2 = {1.f,0.f};
static integer c__3 = 3;
static integer c__1 = 1;

/* > \brief \b CLAGGE */

/*  =========== DOCUMENTATION =========== */

/* Online html documentation available at */
/*            http://www.netlib.org/lapack/explore-html/ */

/*  Definition: */
/*  =========== */

/*       SUBROUTINE CLAGGE( M, N, KL, KU, D, A, LDA, ISEED, WORK, INFO ) */

/*       INTEGER            INFO, KL, KU, LDA, M, N */
/*       INTEGER            ISEED( 4 ) */
/*       REAL               D( * ) */
/*       COMPLEX            A( LDA, * ), WORK( * ) */


/* > \par Purpose: */
/*  ============= */
/* > */
/* > \verbatim */
/* > */
/* > CLAGGE generates a complex general m by n matrix A, by pre- and post- */
/* > multiplying a real diagonal matrix D with random unitary matrices: */
/* > A = U*D*V. The lower and upper bandwidths may then be reduced to */
/* > kl and ku by additional unitary transformations. */
/* > \endverbatim */

/*  Arguments: */
/*  ========== */

/* > \param[in] M */
/* > \verbatim */
/* >          M is INTEGER */
/* >          The number of rows of the matrix A.  M >= 0. */
/* > \endverbatim */
/* > */
/* > \param[in] N */
/* > \verbatim */
/* >          N is INTEGER */
/* >          The number of columns of the matrix A.  N >= 0. */
/* > \endverbatim */
/* > */
/* > \param[in] KL */
/* > \verbatim */
/* >          KL is INTEGER */
/* >          The number of nonzero subdiagonals within the band of A. */
/* >          0 <= KL <= M-1. */
/* > \endverbatim */
/* > */
/* > \param[in] KU */
/* > \verbatim */
/* >          KU is INTEGER */
/* >          The number of nonzero superdiagonals within the band of A. */
/* >          0 <= KU <= N-1. */
/* > \endverbatim */
/* > */
/* > \param[in] D */
/* > \verbatim */
/* >          D is REAL array, dimension (f2cmin(M,N)) */
/* >          The diagonal elements of the diagonal matrix D. */
/* > \endverbatim */
/* > */
/* > \param[out] A */
/* > \verbatim */
/* >          A is COMPLEX array, dimension (LDA,N) */
/* >          The generated m by n matrix A. */
/* > \endverbatim */
/* > */
/* > \param[in] LDA */
/* > \verbatim */
/* >          LDA is INTEGER */
/* >          The leading dimension of the array A.  LDA >= M. */
/* > \endverbatim */
/* > */
/* > \param[in,out] ISEED */
/* > \verbatim */
/* >          ISEED is INTEGER array, dimension (4) */
/* >          On entry, the seed of the random number generator; the array */
/* >          elements must be between 0 and 4095, and ISEED(4) must be */
/* >          odd. */
/* >          On exit, the seed is updated. */
/* > \endverbatim */
/* > */
/* > \param[out] WORK */
/* > \verbatim */
/* >          WORK is COMPLEX array, dimension (M+N) */
/* > \endverbatim */
/* > */
/* > \param[out] INFO */
/* > \verbatim */
/* >          INFO is INTEGER */
/* >          = 0: successful exit */
/* >          < 0: if INFO = -i, the i-th argument had an illegal value */
/* > \endverbatim */

/*  Authors: */
/*  ======== */

/* > \author Univ. of Tennessee */
/* > \author Univ. of California Berkeley */
/* > \author Univ. of Colorado Denver */
/* > \author NAG Ltd. */

/* > \date December 2016 */

/* > \ingroup complex_matgen */

/*  ===================================================================== */
/* Subroutine */ void clagge_(integer *m, integer *n, integer *kl, integer *ku,
	 real *d__, complex *a, integer *lda, integer *iseed, complex *work, 
	integer *info)
{
    /* System generated locals */
    integer a_dim1, a_offset, i__1, i__2, i__3;
    real r__1;
    complex q__1;

    /* Local variables */
    integer i__, j;
    extern /* Subroutine */ void cgerc_(integer *, integer *, complex *, 
	    complex *, integer *, complex *, integer *, complex *, integer *),
	     cscal_(integer *, complex *, complex *, integer *), cgemv_(char *
	    , integer *, integer *, complex *, complex *, integer *, complex *
	    , integer *, complex *, complex *, integer *);
    extern real scnrm2_(integer *, complex *, integer *);
    complex wa, wb;
    extern /* Subroutine */ void clacgv_(integer *, complex *, integer *);
    real wn;
    extern /* Subroutine */ int xerbla_(char *, integer *, ftnlen);
    extern void clarnv_(
	    integer *, integer *, integer *, complex *);
    complex tau;


/*  -- LAPACK auxiliary routine (version 3.7.0) -- */
/*  -- LAPACK is a software package provided by Univ. of Tennessee,    -- */
/*  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..-- */
/*     December 2016 */


/*  ===================================================================== */


/*     Test the input arguments */

    /* Parameter adjustments */
    --d__;
    a_dim1 = *lda;
    a_offset = 1 + a_dim1 * 1;
    a -= a_offset;
    --iseed;
    --work;

    /* Function Body */
    *info = 0;
    if (*m < 0) {
	*info = -1;
    } else if (*n < 0) {
	*info = -2;
    } else if (*kl < 0 || *kl > *m - 1) {
	*info = -3;
    } else if (*ku < 0 || *ku > *n - 1) {
	*info = -4;
    } else if (*lda < f2cmax(1,*m)) {
	*info = -7;
    }
    if (*info < 0) {
	i__1 = -(*info);
	xerbla_("CLAGGE", &i__1, 6);
	return;
    }

/*     initialize A to diagonal matrix */

    i__1 = *n;
    for (j = 1; j <= i__1; ++j) {
	i__2 = *m;
	for (i__ = 1; i__ <= i__2; ++i__) {
	    i__3 = i__ + j * a_dim1;
	    a[i__3].r = 0.f, a[i__3].i = 0.f;
/* L10: */
	}
/* L20: */
    }
    i__1 = f2cmin(*m,*n);
    for (i__ = 1; i__ <= i__1; ++i__) {
	i__2 = i__ + i__ * a_dim1;
	i__3 = i__;
	a[i__2].r = d__[i__3], a[i__2].i = 0.f;
/* L30: */
    }

/*     Quick exit if the user wants a diagonal matrix */

    if (*kl == 0 && *ku == 0) {
	return;
    }

/*     pre- and post-multiply A by random unitary matrices */

    for (i__ = f2cmin(*m,*n); i__ >= 1; --i__) {
	if (i__ < *m) {

/*           generate random reflection */

	    i__1 = *m - i__ + 1;
	    clarnv_(&c__3, &iseed[1], &i__1, &work[1]);
	    i__1 = *m - i__ + 1;
	    wn = scnrm2_(&i__1, &work[1], &c__1);
	    r__1 = wn / c_abs(&work[1]);
	    q__1.r = r__1 * work[1].r, q__1.i = r__1 * work[1].i;
	    wa.r = q__1.r, wa.i = q__1.i;
	    if (wn == 0.f) {
		tau.r = 0.f, tau.i = 0.f;
	    } else {
		q__1.r = work[1].r + wa.r, q__1.i = work[1].i + wa.i;
		wb.r = q__1.r, wb.i = q__1.i;
		i__1 = *m - i__;
		c_div(&q__1, &c_b2, &wb);
		cscal_(&i__1, &q__1, &work[2], &c__1);
		work[1].r = 1.f, work[1].i = 0.f;
		c_div(&q__1, &wb, &wa);
		r__1 = q__1.r;
		tau.r = r__1, tau.i = 0.f;
	    }

/*           multiply A(i:m,i:n) by random reflection from the left */

	    i__1 = *m - i__ + 1;
	    i__2 = *n - i__ + 1;
	    cgemv_("Conjugate transpose", &i__1, &i__2, &c_b2, &a[i__ + i__ * 
		    a_dim1], lda, &work[1], &c__1, &c_b1, &work[*m + 1], &
		    c__1);
	    i__1 = *m - i__ + 1;
	    i__2 = *n - i__ + 1;
	    q__1.r = -tau.r, q__1.i = -tau.i;
	    cgerc_(&i__1, &i__2, &q__1, &work[1], &c__1, &work[*m + 1], &c__1,
		     &a[i__ + i__ * a_dim1], lda);
	}
	if (i__ < *n) {

/*           generate random reflection */

	    i__1 = *n - i__ + 1;
	    clarnv_(&c__3, &iseed[1], &i__1, &work[1]);
	    i__1 = *n - i__ + 1;
	    wn = scnrm2_(&i__1, &work[1], &c__1);
	    r__1 = wn / c_abs(&work[1]);
	    q__1.r = r__1 * work[1].r, q__1.i = r__1 * work[1].i;
	    wa.r = q__1.r, wa.i = q__1.i;
	    if (wn == 0.f) {
		tau.r = 0.f, tau.i = 0.f;
	    } else {
		q__1.r = work[1].r + wa.r, q__1.i = work[1].i + wa.i;
		wb.r = q__1.r, wb.i = q__1.i;
		i__1 = *n - i__;
		c_div(&q__1, &c_b2, &wb);
		cscal_(&i__1, &q__1, &work[2], &c__1);
		work[1].r = 1.f, work[1].i = 0.f;
		c_div(&q__1, &wb, &wa);
		r__1 = q__1.r;
		tau.r = r__1, tau.i = 0.f;
	    }

/*           multiply A(i:m,i:n) by random reflection from the right */

	    i__1 = *m - i__ + 1;
	    i__2 = *n - i__ + 1;
	    cgemv_("No transpose", &i__1, &i__2, &c_b2, &a[i__ + i__ * a_dim1]
		    , lda, &work[1], &c__1, &c_b1, &work[*n + 1], &c__1);
	    i__1 = *m - i__ + 1;
	    i__2 = *n - i__ + 1;
	    q__1.r = -tau.r, q__1.i = -tau.i;
	    cgerc_(&i__1, &i__2, &q__1, &work[*n + 1], &c__1, &work[1], &c__1,
		     &a[i__ + i__ * a_dim1], lda);
	}
/* L40: */
    }

/*     Reduce number of subdiagonals to KL and number of superdiagonals */
/*     to KU */

/* Computing MAX */
    i__2 = *m - 1 - *kl, i__3 = *n - 1 - *ku;
    i__1 = f2cmax(i__2,i__3);
    for (i__ = 1; i__ <= i__1; ++i__) {
	if (*kl <= *ku) {

/*           annihilate subdiagonal elements first (necessary if KL = 0) */

/* Computing MIN */
	    i__2 = *m - 1 - *kl;
	    if (i__ <= f2cmin(i__2,*n)) {

/*              generate reflection to annihilate A(kl+i+1:m,i) */

		i__2 = *m - *kl - i__ + 1;
		wn = scnrm2_(&i__2, &a[*kl + i__ + i__ * a_dim1], &c__1);
		r__1 = wn / c_abs(&a[*kl + i__ + i__ * a_dim1]);
		i__2 = *kl + i__ + i__ * a_dim1;
		q__1.r = r__1 * a[i__2].r, q__1.i = r__1 * a[i__2].i;
		wa.r = q__1.r, wa.i = q__1.i;
		if (wn == 0.f) {
		    tau.r = 0.f, tau.i = 0.f;
		} else {
		    i__2 = *kl + i__ + i__ * a_dim1;
		    q__1.r = a[i__2].r + wa.r, q__1.i = a[i__2].i + wa.i;
		    wb.r = q__1.r, wb.i = q__1.i;
		    i__2 = *m - *kl - i__;
		    c_div(&q__1, &c_b2, &wb);
		    cscal_(&i__2, &q__1, &a[*kl + i__ + 1 + i__ * a_dim1], &
			    c__1);
		    i__2 = *kl + i__ + i__ * a_dim1;
		    a[i__2].r = 1.f, a[i__2].i = 0.f;
		    c_div(&q__1, &wb, &wa);
		    r__1 = q__1.r;
		    tau.r = r__1, tau.i = 0.f;
		}

/*              apply reflection to A(kl+i:m,i+1:n) from the left */

		i__2 = *m - *kl - i__ + 1;
		i__3 = *n - i__;
		cgemv_("Conjugate transpose", &i__2, &i__3, &c_b2, &a[*kl + 
			i__ + (i__ + 1) * a_dim1], lda, &a[*kl + i__ + i__ * 
			a_dim1], &c__1, &c_b1, &work[1], &c__1);
		i__2 = *m - *kl - i__ + 1;
		i__3 = *n - i__;
		q__1.r = -tau.r, q__1.i = -tau.i;
		cgerc_(&i__2, &i__3, &q__1, &a[*kl + i__ + i__ * a_dim1], &
			c__1, &work[1], &c__1, &a[*kl + i__ + (i__ + 1) * 
			a_dim1], lda);
		i__2 = *kl + i__ + i__ * a_dim1;
		q__1.r = -wa.r, q__1.i = -wa.i;
		a[i__2].r = q__1.r, a[i__2].i = q__1.i;
	    }

/* Computing MIN */
	    i__2 = *n - 1 - *ku;
	    if (i__ <= f2cmin(i__2,*m)) {

/*              generate reflection to annihilate A(i,ku+i+1:n) */

		i__2 = *n - *ku - i__ + 1;
		wn = scnrm2_(&i__2, &a[i__ + (*ku + i__) * a_dim1], lda);
		r__1 = wn / c_abs(&a[i__ + (*ku + i__) * a_dim1]);
		i__2 = i__ + (*ku + i__) * a_dim1;
		q__1.r = r__1 * a[i__2].r, q__1.i = r__1 * a[i__2].i;
		wa.r = q__1.r, wa.i = q__1.i;
		if (wn == 0.f) {
		    tau.r = 0.f, tau.i = 0.f;
		} else {
		    i__2 = i__ + (*ku + i__) * a_dim1;
		    q__1.r = a[i__2].r + wa.r, q__1.i = a[i__2].i + wa.i;
		    wb.r = q__1.r, wb.i = q__1.i;
		    i__2 = *n - *ku - i__;
		    c_div(&q__1, &c_b2, &wb);
		    cscal_(&i__2, &q__1, &a[i__ + (*ku + i__ + 1) * a_dim1], 
			    lda);
		    i__2 = i__ + (*ku + i__) * a_dim1;
		    a[i__2].r = 1.f, a[i__2].i = 0.f;
		    c_div(&q__1, &wb, &wa);
		    r__1 = q__1.r;
		    tau.r = r__1, tau.i = 0.f;
		}

/*              apply reflection to A(i+1:m,ku+i:n) from the right */

		i__2 = *n - *ku - i__ + 1;
		clacgv_(&i__2, &a[i__ + (*ku + i__) * a_dim1], lda);
		i__2 = *m - i__;
		i__3 = *n - *ku - i__ + 1;
		cgemv_("No transpose", &i__2, &i__3, &c_b2, &a[i__ + 1 + (*ku 
			+ i__) * a_dim1], lda, &a[i__ + (*ku + i__) * a_dim1],
			 lda, &c_b1, &work[1], &c__1);
		i__2 = *m - i__;
		i__3 = *n - *ku - i__ + 1;
		q__1.r = -tau.r, q__1.i = -tau.i;
		cgerc_(&i__2, &i__3, &q__1, &work[1], &c__1, &a[i__ + (*ku + 
			i__) * a_dim1], lda, &a[i__ + 1 + (*ku + i__) * 
			a_dim1], lda);
		i__2 = i__ + (*ku + i__) * a_dim1;
		q__1.r = -wa.r, q__1.i = -wa.i;
		a[i__2].r = q__1.r, a[i__2].i = q__1.i;
	    }
	} else {

/*           annihilate superdiagonal elements first (necessary if */
/*           KU = 0) */

/* Computing MIN */
	    i__2 = *n - 1 - *ku;
	    if (i__ <= f2cmin(i__2,*m)) {

/*              generate reflection to annihilate A(i,ku+i+1:n) */

		i__2 = *n - *ku - i__ + 1;
		wn = scnrm2_(&i__2, &a[i__ + (*ku + i__) * a_dim1], lda);
		r__1 = wn / c_abs(&a[i__ + (*ku + i__) * a_dim1]);
		i__2 = i__ + (*ku + i__) * a_dim1;
		q__1.r = r__1 * a[i__2].r, q__1.i = r__1 * a[i__2].i;
		wa.r = q__1.r, wa.i = q__1.i;
		if (wn == 0.f) {
		    tau.r = 0.f, tau.i = 0.f;
		} else {
		    i__2 = i__ + (*ku + i__) * a_dim1;
		    q__1.r = a[i__2].r + wa.r, q__1.i = a[i__2].i + wa.i;
		    wb.r = q__1.r, wb.i = q__1.i;
		    i__2 = *n - *ku - i__;
		    c_div(&q__1, &c_b2, &wb);
		    cscal_(&i__2, &q__1, &a[i__ + (*ku + i__ + 1) * a_dim1], 
			    lda);
		    i__2 = i__ + (*ku + i__) * a_dim1;
		    a[i__2].r = 1.f, a[i__2].i = 0.f;
		    c_div(&q__1, &wb, &wa);
		    r__1 = q__1.r;
		    tau.r = r__1, tau.i = 0.f;
		}

/*              apply reflection to A(i+1:m,ku+i:n) from the right */

		i__2 = *n - *ku - i__ + 1;
		clacgv_(&i__2, &a[i__ + (*ku + i__) * a_dim1], lda);
		i__2 = *m - i__;
		i__3 = *n - *ku - i__ + 1;
		cgemv_("No transpose", &i__2, &i__3, &c_b2, &a[i__ + 1 + (*ku 
			+ i__) * a_dim1], lda, &a[i__ + (*ku + i__) * a_dim1],
			 lda, &c_b1, &work[1], &c__1);
		i__2 = *m - i__;
		i__3 = *n - *ku - i__ + 1;
		q__1.r = -tau.r, q__1.i = -tau.i;
		cgerc_(&i__2, &i__3, &q__1, &work[1], &c__1, &a[i__ + (*ku + 
			i__) * a_dim1], lda, &a[i__ + 1 + (*ku + i__) * 
			a_dim1], lda);
		i__2 = i__ + (*ku + i__) * a_dim1;
		q__1.r = -wa.r, q__1.i = -wa.i;
		a[i__2].r = q__1.r, a[i__2].i = q__1.i;
	    }

/* Computing MIN */
	    i__2 = *m - 1 - *kl;
	    if (i__ <= f2cmin(i__2,*n)) {

/*              generate reflection to annihilate A(kl+i+1:m,i) */

		i__2 = *m - *kl - i__ + 1;
		wn = scnrm2_(&i__2, &a[*kl + i__ + i__ * a_dim1], &c__1);
		r__1 = wn / c_abs(&a[*kl + i__ + i__ * a_dim1]);
		i__2 = *kl + i__ + i__ * a_dim1;
		q__1.r = r__1 * a[i__2].r, q__1.i = r__1 * a[i__2].i;
		wa.r = q__1.r, wa.i = q__1.i;
		if (wn == 0.f) {
		    tau.r = 0.f, tau.i = 0.f;
		} else {
		    i__2 = *kl + i__ + i__ * a_dim1;
		    q__1.r = a[i__2].r + wa.r, q__1.i = a[i__2].i + wa.i;
		    wb.r = q__1.r, wb.i = q__1.i;
		    i__2 = *m - *kl - i__;
		    c_div(&q__1, &c_b2, &wb);
		    cscal_(&i__2, &q__1, &a[*kl + i__ + 1 + i__ * a_dim1], &
			    c__1);
		    i__2 = *kl + i__ + i__ * a_dim1;
		    a[i__2].r = 1.f, a[i__2].i = 0.f;
		    c_div(&q__1, &wb, &wa);
		    r__1 = q__1.r;
		    tau.r = r__1, tau.i = 0.f;
		}

/*              apply reflection to A(kl+i:m,i+1:n) from the left */

		i__2 = *m - *kl - i__ + 1;
		i__3 = *n - i__;
		cgemv_("Conjugate transpose", &i__2, &i__3, &c_b2, &a[*kl + 
			i__ + (i__ + 1) * a_dim1], lda, &a[*kl + i__ + i__ * 
			a_dim1], &c__1, &c_b1, &work[1], &c__1);
		i__2 = *m - *kl - i__ + 1;
		i__3 = *n - i__;
		q__1.r = -tau.r, q__1.i = -tau.i;
		cgerc_(&i__2, &i__3, &q__1, &a[*kl + i__ + i__ * a_dim1], &
			c__1, &work[1], &c__1, &a[*kl + i__ + (i__ + 1) * 
			a_dim1], lda);
		i__2 = *kl + i__ + i__ * a_dim1;
		q__1.r = -wa.r, q__1.i = -wa.i;
		a[i__2].r = q__1.r, a[i__2].i = q__1.i;
	    }
	}

	if (i__ <= *n) {
	    i__2 = *m;
	    for (j = *kl + i__ + 1; j <= i__2; ++j) {
		i__3 = j + i__ * a_dim1;
		a[i__3].r = 0.f, a[i__3].i = 0.f;
/* L50: */
	    }
	}

	if (i__ <= *m) {
	    i__2 = *n;
	    for (j = *ku + i__ + 1; j <= i__2; ++j) {
		i__3 = i__ + j * a_dim1;
		a[i__3].r = 0.f, a[i__3].i = 0.f;
/* L60: */
	    }
	}
/* L70: */
    }
    return;

/*     End of CLAGGE */

} /* clagge_ */

