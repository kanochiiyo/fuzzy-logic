import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import math


class CustomLine:
    @staticmethod
    def render(axes, x, y):
        axes.plot([x, x], [0, y], linestyle="dashed", linewidth=0.7)
        axes.plot([0, x], [y, y], linestyle="dashed", linewidth=0.7)

        xticks = axes.get_xticks()
        new_xticks = list(xticks) + [x]
        axes.set_xticks(new_xticks)

        yticks = axes.get_yticks()
        new_yticks = list(yticks) + [y]
        axes.set_yticks(new_yticks)


mhs_max = 40
mhs_min = 5
kom_max = 50
kom_min = 10
kebutuhan_max = 100
kebutuhan_min = 50


def on_submit():
    global mhs, kom
    try:
        mhs = int(entry_mhs.get())
        kom = int(entry_kom.get())

        if mhs_min <= mhs <= mhs_max and kom_min <= kom <= kom_max:
            root.destroy()  # Close the input window and proceed to processing
        else:
            messagebox.showerror(
                "Input Error", "Input tidak valid, silahkan masukkan kembali"
            )
    except ValueError:
        messagebox.showerror("Input Error", "Masukkan angka yang valid.")


root = tk.Tk()
root.title("Penghitungan Kebutuhan Komputer")

label_mhs = tk.Label(root, text="Masukkan jumlah mahasiswa yang hadir per sesi (5-40):")
label_mhs.pack()

entry_mhs = tk.Entry(root)
entry_mhs.pack()

label_kom = tk.Label(root, text="Masukkan jumlah komputer yang siap digunakan (10-50):")
label_kom.pack()

entry_kom = tk.Entry(root)
entry_kom.pack()

submit_btn = tk.Button(root, text="Submit", command=on_submit)
submit_btn.pack()

root.mainloop()


# Membership functions
def mhs_sedikit(x):
    if x <= mhs_min:
        return 1
    elif mhs_min < x < mhs_max:
        return (mhs_max - x) / (mhs_max - mhs_min)
    else:
        return 0


def mhs_banyak(x):
    if x <= mhs_min:
        return 0
    elif mhs_min < x <= mhs_max:
        return (x - mhs_min) / (mhs_max - mhs_min)
    else:
        return 1


# ======== Criteria 2: Waktu kom
# Fuzzy set: banyak (0 ke 1) sedikit (1 ke 0)


def kom_banyak(y):
    if y <= kom_min:
        return 0
    elif kom_min < y <= kom_max:
        return (y - kom_min) / (kom_max - kom_min)
    else:
        return 1


def kom_sedikit(y):
    if y <= kom_min:
        return 1
    elif kom_min < y < kom_max:
        return (kom_max - y) / (kom_max - kom_min)
    else:
        return 0


# ======== Criteria 3: Tingkat kebutuhan
# Fuzzy set: Tinggi (0 ke 1) Rendah (1 ke 0)


def kebutuhan_tinggi(α):
    return ((kebutuhan_max - kebutuhan_min) * α) + kebutuhan_min


def kebutuhan_rendah(α):
    return kebutuhan_max - ((kebutuhan_max - kebutuhan_min) * α)


# ======== DERAJAT KEANGGOTAAN
μ_mhs_sedikit = mhs_sedikit(mhs)
μ_mhs_banyak = mhs_banyak(mhs)
μ_kom_banyak = kom_banyak(kom)
μ_kom_sedikit = kom_sedikit(kom)

print(μ_mhs_sedikit, μ_mhs_banyak, μ_kom_banyak, μ_kom_sedikit)

# ======== RULE BASE
# mhs sedikit dan kom banyak = kebutuhan rendah
# mhs sedikit dan kom sedikit = kebutuhan rendah
# mhs banyak dan kom sedikit = kebutuhan tinggi
# mhs banyak dan kom banyak = kebutuhan tinggi

# ======== INFERENSI
α1 = min(μ_mhs_sedikit, μ_kom_banyak)
z1 = kebutuhan_rendah(α1)
α2 = min(μ_mhs_sedikit, μ_kom_sedikit)
z2 = kebutuhan_rendah(α2)
α3 = min(μ_mhs_banyak, μ_kom_banyak)
z3 = kebutuhan_tinggi(α3)  # ????
α4 = min(μ_mhs_banyak, μ_kom_sedikit)
z4 = kebutuhan_tinggi(α4)

print(α1, α2, α3, α4)
print(z1, z2, z3, z4)

# ======== CRISP OUTPUT
z = math.ceil(((α1 * z1) + (α2 * z2) + (α3 * z3) + (α4 * z4)) / (α1 + α2 + α3 + α4))

# Grafik MAHASISWA
# MHS SEDIKIT
x1 = [1, mhs_min, mhs_max]
y1 = [1, 1, 0]

# MHS BANYAK
x2 = [mhs_min, mhs_max, 300]
y2 = [0, 1, 1]

# KOM DIKI
x3 = [1, kom_min, kom_max]
y3 = [1, 1, 0]

# KOM BANYAK
x4 = [kom_min, kom_max, 300]
y4 = [0, 1, 1]

# KEBUTUHAN SEDIKIT
x5 = [0, kebutuhan_min, kebutuhan_max]
y5 = [1, 1, 0]

# KEBUTUHAN BANYAK
x6 = [kebutuhan_min, kebutuhan_max, 500]
y6 = [0, 1, 1]

fig, axs = plt.subplots(3, 1)

axs[0].plot(x1, y1, label="SEDIKIT", color="orange")
axs[0].plot(x2, y2, label="BANYAK", color="blue")
axs[0].set_xlim([mhs_min, mhs_max])
axs[0].set_ylim([0, 1])

CustomLine.render(axs[0], mhs, μ_mhs_sedikit)
CustomLine.render(axs[0], mhs, μ_mhs_banyak)

axs[0].set_title("Mahasiswa")
axs[0].legend()

axs[1].plot(x3, y3, label="SEDIKIT", color="orange")
axs[1].plot(x4, y4, label="BANYAK", color="blue")
axs[1].set_xlim([kom_min, kom_max])
axs[1].set_ylim([0, 1])

CustomLine.render(axs[1], kom, μ_kom_sedikit)
CustomLine.render(axs[1], kom, μ_kom_banyak)

axs[1].set_title("Komputer")
axs[1].legend()

axs[2].plot(x5, y5, label="TURUN", color="orange")
axs[2].plot(x6, y6, label="NAIK", color="blue")
axs[2].set_xlim([kebutuhan_min, kebutuhan_max])
axs[2].set_ylim([0, 1])

CustomLine.render(axs[2], z, 1)
axs[2].set_title("Kebutuhan")
axs[2].legend()

plt.tight_layout()
plt.show()
