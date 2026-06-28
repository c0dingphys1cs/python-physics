

"""
Gravitational Wave Simulation - Phase 1
Binary merger chirp signal via post-Newtonian approximation

Based on GW150914 (first detected gravitational wave, LIGO 2015)

Install dependencies:
    pip install numpy matplotlib scipy

Run:
    python gw_phase1.py
        """
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Constants ──────────────────────────────────────────────────────────────────
G    = 6.674e-11      # Gravitational constant (m^3 kg^-1 s^-2)
c    = 3e8            # Speed of light (m/s)
Msun = 1.989e30       # Solar mass (kg)
Mpc  = 3.086e22       # 1 Megaparsec in meters

# ── Parameters (GW150914 defaults) ────────────────────────────────────────────
m1       = 36.0       # Mass 1 (solar masses)
m2       = 29.0       # Mass 2 (solar masses)
distance = 410.0      # Luminosity distance (Mpc)
f_start  = 20.0       # Starting GW frequency (Hz)
duration = 2.0        # Simulation duration (seconds)
fs       = 4096       # Sample rate (Hz)

# ── Derived quantities ─────────────────────────────────────────────────────────
M1 = m1 * Msun
M2 = m2 * Msun
Mc = (M1 * M2)**0.6 / (M1 + M2)**0.2      # Chirp mass (kg)
D  = distance * Mpc                         # Distance (m)

Mc_solar = (m1 * m2)**0.6 / (m1 + m2)**0.2

print("=" * 55)
print("  Gravitational Wave Phase 1 — Chirp Signal Generator")
print("=" * 55)
print(f"  Mass 1        : {m1} M☉")
print(f"  Mass 2        : {m2} M☉")
print(f"  Chirp Mass    : {Mc_solar:.2f} M☉")
print(f"  Distance      : {distance} Mpc")
print(f"  Start Freq    : {f_start} Hz")
print(f"  Sample Rate   : {fs} Hz")

# ── Time to coalescence from f_start ──────────────────────────────────────────
# t_coal = (5/256) * (c^5 / G^(5/3)) * Mc^(-5/3) * (pi * f_start)^(-8/3)
t_coal = (5.0 / 256.0) * (c**5 / G**(5/3)) * Mc**(-5/3) * (np.pi * f_start)**(-8/3)
print(f"  Coalescence   : {t_coal:.3f} s from f_start")
print("=" * 55)

# ── Generate waveform ──────────────────────────────────────────────────────────
N  = int(duration * fs)
dt = 1.0 / fs
t  = np.arange(N) * dt

# Time remaining until coalescence at each sample
tau = t_coal - t

# Only compute where tau > 0 (before merger)
valid = tau > 0
t_valid   = t[valid]
tau_valid = tau[valid]

# Instantaneous GW frequency (Hz)
# f(t) = f_start * (1 - t/t_coal)^(-3/8)
f_inst = f_start * (1.0 - t_valid / t_coal)**(-3.0/8.0)

# Stop at 2000 Hz (innermost stable circular orbit approximation)
mask   = f_inst < 2000
t_valid   = t_valid[mask]
tau_valid = tau_valid[mask]
f_inst    = f_inst[mask]

# Strain amplitude envelope
# h_amp = (4/D) * (G*Mc/c^2)^(5/4) * (pi*f/c)^(2/3) * c
h_amp = (4.0 / D) * (G * Mc / c**2)**(5.0/4.0) * (np.pi * f_inst / c)**(2.0/3.0) * c

# GW phase
# phi(t) = -2 * (5*G*Mc/c^3)^(-5/8) * tau^(5/8)
phi = -2.0 * (5.0 * G * Mc / c**3)**(-5.0/8.0) * tau_valid**(5.0/8.0)

# Plus polarization strain
h_plus = h_amp * np.cos(phi)

print(f"\n  Signal length : {len(t_valid)} samples ({t_valid[-1]:.3f} s)")
print(f"  Peak strain   : {np.max(h_amp):.3e}")
print(f"  Peak freq     : {f_inst[-1]:.0f} Hz")
print(f"  Max strain ×10^21: {np.max(h_amp)*1e21:.2f}")

# ── Plot ───────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 10), facecolor="#0d1117")
fig.suptitle(
    f"Gravitational Wave — Binary Merger Chirp\n"
    f"m₁={m1} M☉, m₂={m2} M☉,  Mc={Mc_solar:.1f} M☉,  D={distance} Mpc",
    color="#e6edf3", fontsize=14, y=0.98
                    )

gs = gridspec.GridSpec(3, 1, hspace=0.45, top=0.91, bottom=0.07, left=0.09, right=0.97)

ax_style = dict(facecolor="#161b22")
tick_kw  = dict(colors="#8b949e", labelsize=9)
label_kw = dict(color="#c9d1d9", fontsize=10)
grid_kw  = dict(color="#21262d", linewidth=0.7)

# ── Plot 1: Strain h(t) ────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0], **ax_style)
ax1.plot(t_valid, h_plus * 1e21, color="#388bfd", linewidth=0.8, label="h₊(t)")
ax1.plot(t_valid,  h_amp * 1e21, color="#d29922", linewidth=1.2, linestyle="--", alpha=0.7, label="Envelope")
ax1.plot(t_valid, -h_amp * 1e21, color="#d29922", linewidth=1.2, linestyle="--", alpha=0.7)
ax1.axhline(0, color="#30363d", linewidth=0.5)
ax1.set_ylabel("Strain h(t)  [×10⁻²¹]", **label_kw)
ax1.set_title("Gravitational Wave Strain  h₊(t)", color="#e6edf3", fontsize=10, pad=4)
ax1.tick_params(**tick_kw)
ax1.grid(**grid_kw)
ax1.legend(fontsize=9, facecolor="#0d1117", edgecolor="#30363d", labelcolor="#c9d1d9")
for spine in ax1.spines.values():
    spine.set_edgecolor("#30363d")

# ── Plot 2: Instantaneous frequency ───────────────────────────────────────────
ax2 = fig.add_subplot(gs[1], **ax_style)
ax2.plot(t_valid, f_inst, color="#3fb950", linewidth=1.5)
ax2.set_ylabel("Frequency  [Hz]", **label_kw)
ax2.set_title("Instantaneous GW Frequency  f(t)  — the 'chirp'", color="#e6edf3", fontsize=10, pad=4)
ax2.tick_params(**tick_kw)
ax2.grid(**grid_kw)
for spine in ax2.spines.values():
    spine.set_edgecolor("#30363d")

# ── Plot 3: Spectrogram ────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2], **ax_style)
Pxx, freqs, bins, im = ax3.specgram(
    h_plus, Fs=fs, NFFT=256, noverlap=240,
    cmap="inferno", xextent=(0, t_valid[-1])
                            )
ax3.set_ylim(0, 500)
ax3.set_ylabel("Frequency  [Hz]", **label_kw)
ax3.set_xlabel("Time  [s]", **label_kw)
ax3.set_title("Spectrogram  — frequency sweep over time", color="#e6edf3", fontsize=10, pad=4)
ax3.tick_params(**tick_kw)
for spine in ax3.spines.values():
    spine.set_edgecolor("#30363d")

cb = fig.colorbar(im, ax=ax3, pad=0.01)
cb.set_label("Power [dB]", color="#8b949e", fontsize=9)
cb.ax.yaxis.set_tick_params(colors="#8b949e", labelsize=8)

plt.savefig("gw_phase1_output.png", dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("\n  Plot saved → gw_phase1_output.png")
plt.savefig("gw_phase1_output.png", dpi=150, bbox_inches="tight", facecolor="#0d1117")

from IPython.display import Image
Image("gw_phase1_output.png")
