import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def test1():
    d = pd.DataFrame([range(1, 8), range(2, 9)])
    print(d)
    print(d.sum())
    print(d.mean())
    print(d.describe())


def test_sin():
    x = np.linspace(0, 2 * np.pi, 50);
    y = np.sin(x);
    plt.plot(x, y, 'bp--');
    plt.show();


def test_pie():
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 60];
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0);
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show()


def test_hist():
    x = np.random.randn(1000)
    plt.hist(x, 10)
    plt.show()


def test_boxplot():
    x = np.random.randn(1000)
    D = pd.DataFrame(x, x + 1);
    D.plot(kind='box');
    plt.show();


test_boxplot()
