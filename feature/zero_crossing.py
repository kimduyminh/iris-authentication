import numpy as np
import pywt
import matplotlib.pyplot as plt


def zero_crossings_1d_wavelet(signal):
    """
    Find zero-crossing points in a 1D signal using a wavelet transform.
    """
    # Apply Haar wavelet transform
    coeffs = pywt.wavedec(signal, 'haar', level=1)
    detail_coeffs = coeffs[1]  # Detail coefficients (high frequency components)

    # Find zero-crossings
    zero_crossings = np.where(np.diff(np.sign(detail_coeffs)))[0]
    return detail_coeffs, zero_crossings


# Simulated 1D signal
x = np.linspace(0, 4 * np.pi, 100)
signal = np.sin(x) + np.sin(2 * x)  # Example signal with two frequencies

# Find zero crossings
detail_coeffs, zero_crossings = zero_crossings_1d_wavelet(signal)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(detail_coeffs, label="Wavelet Detail Coefficients")
plt.scatter(zero_crossings, detail_coeffs[zero_crossings], color='red', label="Zero-Crossings")
plt.title("Zero-Crossings of 1D Wavelet Transform")
plt.legend()
plt.grid()
plt.show()
