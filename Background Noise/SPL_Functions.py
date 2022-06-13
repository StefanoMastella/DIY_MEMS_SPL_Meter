"""
SPL_functions

@author: Stefano Mastella
"""

import pytta
from pytta.classes.filter import fractional_octave_frequencies as FOF
import numpy as np

#%% Octave Filter
def octfilter(obj,nth,bands,
            order: int = 4,
            minFreq: float = 20,
            maxFreq: float = 20000,
            refFreq: float = 1000,
            base: int = 2):
           of = pytta.OctFilter(order=order,
                       nthOct=nth,
                       samplingRate=obj.samplingRate,
                       minFreq=minFreq,
                       maxFreq=maxFreq,
                       refFreq=refFreq,
                       base=base)          
           result = of.filter(obj)
           filtered_sig = result[0] 
           
           # filtered_sig.plot_freq() # Plot the filtered signal
           
           Oct_level = np.zeros(np.size(bands))
           p_ref = 20e-6
           for n in range(np.size(bands)):
               Oct_level[n] = 20*np.log10(rms(filtered_sig.timeSignal[:,n])/p_ref)
           
           return Oct_level        

def band_freq_arr(nth):
    bands = FOF(nthOct=nth,
            freqRange=[20,
                        20000])[:, 1]
    return bands

#%% Root mean square function
def rms(a): 
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2)) 

#%%%%%%%%%%%%%%%%%%%%%% Weighting Filters %%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
splweighting

@author: https://github.com/SiggiGue/pyfilterbank
"""

from numpy import pi, convolve
from scipy.signal.filter_design import bilinear
from scipy.signal import lfilter


def weight_signal(data, sample_rate, weighting):
    """
    Returns filtered signal with a weighting filter.
    """
    b, a = _weighting_coeff_design_funsd[weighting](sample_rate)
    return lfilter(b, a, data,axis= 0)

def a_weighting_coeffs_design(sample_rate):
    """
    Returns b and a coeff of a A-weighting filter.
    """

    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997
    numerators = [(2*pi*f4)**2 * (10**(A1000 / 20.0)), 0., 0., 0., 0.];
    denominators = convolve(
        [1., +4*pi * f4, (2*pi * f4)**2],
        [1., +4*pi * f1, (2*pi * f1)**2]
    )
    denominators = convolve(
        convolve(denominators, [1., 2*pi * f3]),
        [1., 2*pi * f2]
    )
    return bilinear(numerators, denominators, sample_rate)

def b_weighting_coeffs_design(sample_rate):
    """
    Returns `b` and `a` coeff of a B-weighting filter.
    """

    f1 = 20.598997
    f2 = 158.5
    f4 = 12194.217
    B1000 = 0.17
    numerators = [(2*pi*f4)**2 * (10**(B1000 / 20)), 0, 0, 0];
    denominators = convolve(
        [1, +4*pi * f4, (2*pi * f4)**2],
        [1, +4*pi * f1, (2*pi * f1)**2]
    )
    denominators = convolve(denominators, [1, 2*pi * f2])
    return bilinear(numerators, denominators, sample_rate)


def c_weighting_coeffs_design(sample_rate):
    """
    Returns b and a coeff of a C-weighting filter.
    """

    f1 = 20.598997
    f4 = 12194.217
    C1000 = 0.0619
    numerators = [(2*pi * f4)**2 * (10**(C1000 / 20)), 0, 0]
    denominators = convolve(
        [1, +4*pi * f4, (2*pi * f4)**2],
        [1, +4*pi * f1, (2*pi * f1)**2]
    )
    return bilinear(numerators, denominators, sample_rate)


# This dictionary should contain all labels and functions
# for weighting coeff design functions:
_weighting_coeff_design_funsd = {
    'A': a_weighting_coeffs_design,
    'B': b_weighting_coeffs_design,
    'C': c_weighting_coeffs_design
}

def plot_weightings():
    """Plots all weighting functions defined in :module: splweighting."""
    from scipy.signal import freqz
    from pylab import plt, np

    sample_rate = 48000
    num_samples = 2*4096

    fig, ax = plt.subplots()

    for name, weight_design in sorted(
            _weighting_coeff_design_funsd.items()):
        b, a = weight_design(sample_rate)
        w, H = freqz(b, a, worN=num_samples)

        freq = w*sample_rate / (2*np.pi)

        ax.semilogx(freq, 20*np.log10(np.abs(H)+1e-20),
                    label='{}-Weighting'.format(name))

    plt.legend(loc='lower right')
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Damping / dB')
    plt.grid(True)
    plt.axis([10, 20000, -80, 5])
    return fig, ax


if __name__ == '__main__':
    fig, ax = plot_weightings()
    fig.show()
