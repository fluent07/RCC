import sympy as smp
from sympy.interactive.printing import init_printing
import numpy as np

init_printing(use_unicode=False, wrap_line=False)
P, L, A, E, EI = smp.symbols("P L A E EI", real=True)

no_of_spans = 4
span_lengths = smp.Array([5, 7, 3, 4])
# phi = smp.MutableDenseNDimArray(np.zeros((no_of_spans - 1, no_of_spans - 1)))
phi0 = smp.zeros(no_of_spans, 1)
phi = smp.zeros(no_of_spans - 1, no_of_spans - 1)
print(span_lengths, phi, len(phi), phi0)
