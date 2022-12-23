import numpy as np
import matplotlib.pyplot as plt


x = np.array([4, 6, 8])
y_trap = np.array([2.48819, 2.47322, 2.46878])
y_par = np.array([2.44976, 2.45967, 2.46231])
y_g = np.array([2.46491, 2.46364, 2.46368])

if __name__ == '__main__':
    plt.plot(x, y_trap, label='Метод трапеции')
    plt.plot(x, y_par, label='Метод параболы')
    plt.plot(x, y_g, label='Метод Гаусса')
    plt.legend()
    plt.grid()
    plt.show()