# -*- coding: utf-8 -*-
""""ЛР_№6.ipynb"

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NIso-iB44im-AszkHM_45t0K4xD7Xa6f

#ЛР №6

Основные понятия ООП. Инкапсуляция. Классы. Декораторы.

##Основная задача "Эксперимент"

Нужно написать класс "Эксперимент", который производит работу с данными.

Вы получили данные в виде словаря. Словарь имеет следующую структуру {'date': '2023-01-05', 'signal': 'path_to_ecg_signal', 'parameters':{}}

**Интерфейс**

Нужно написать класс, где должны поддерживаться следующие методы:

* _конструктор_ — принимает словарь и создает соответствующие поля (self.data, self.path_signal, self.parameters)
* `get_datе()` — возвращает дату записи сигнала.
* `get_signal_length()` — возвращает длину сигнала.
* `plot_signal()` — выводит график сигнала.
* `_signal_filtration(signal, filtration_parametres)` — производит фильтрацию сигнала.
* `_signal_find_peaks(signal, find_peaks_parametres)` — находит точки максимума сигнала и возвращает их в виде списка.
* `_calculate_RR_intervals()` — производит расчет длительности RR интервалов и возвращает длины RR интервалов в виде списка.
В этом методе вызываются методы _signal_filtration и _signal_find_peak.
* `get_RR_statistics()` — возвращает статистические характеристики RR интервалов на записи ECG - среднее, std, min, max (в виде словаря).
В этом методе вызывается метод _calculate_RR_intervals.


*можно добавить свои методы
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install heartpy

"""Файл с ЭКГ сигналом (ecg.csv) в папке"""

#модули, которые нам понадобятся
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# import wfdb
import heartpy as hp
from scipy.signal import find_peaks

#загрузка сигнала из .csv файла с pandas
df = pd.read_csv('/ecg.csv')
plt.plot(df['MLII'])
plt.show()

#фильтрация сигнала с библиотекой heartpy
filtered = hp.filter_signal(df['MLII'], cutoff = [0.75, 3.5], sample_rate = 100, order = 3, filtertype='bandpass')
plt.plot(filtered)
plt.show()

#поиск точек максимума с библиотекой scipy
peaks, _ = find_peaks(filtered, height=20)
plt.plot(filtered)
plt.plot(peaks, filtered[peaks], "p")
plt.show()

class Experiment:
    def __init__(self, data_dict):
        self.data = data_dict
        self.path_signal = data_dict['signal']
        self.parameters = data_dict['parameters']
        self.signal = self._load_signal()

    def _load_signal(self):
        # Загрузка сигнала из файла
        df = pd.read_csv(self.path_signal)
        signal = df['MLII'].values  # Предполагаем, что сигнал находится в столбце 'MLII'
        return signal

    def get_date(self):
        return self.data['date']

    def get_signal_length(self):
        return len(self.signal)

    def plot_signal(self):
        plt.plot(self.signal)
        plt.title("ECG Signal")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.show()

    def _signal_filtration(self, signal, filtration_parameters):
        # Фильтрация сигнала с использованием heartpy
        filtered_signal = hp.filter_signal(signal, **filtration_parameters)
        return filtered_signal

    def _signal_find_peaks(self, signal, find_peaks_parameters):
        # Поиск пиков в сигнале
        peaks, _ = find_peaks(signal, **find_peaks_parameters)
        return peaks

    def _calculate_RR_intervals(self):
        # Фильтрация сигнала
        filtered_signal = self._signal_filtration(self.signal, self.parameters.get('filtration', {}))
        # Поиск пиков
        peaks = self._signal_find_peaks(filtered_signal, self.parameters.get('find_peaks', {}))
        # Расчет RR интервалов
        rr_intervals = np.diff(peaks)
        return rr_intervals

    def get_RR_statistics(self):
        rr_intervals = self._calculate_RR_intervals()
        return {
            'mean': np.mean(rr_intervals),
            'std': np.std(rr_intervals),
            'min': np.min(rr_intervals),
            'max': np.max(rr_intervals)
        }

# Пример использования класса
data_dict = {
    'date': '2023-01-05',
    'signal': '/ecg.csv',  # Путь к файлу с сигналом
    'parameters': {
        'filtration': {'cutoff': [0.75, 3.5], 'sample_rate': 100, 'order': 3, 'filtertype': 'bandpass'},
        'find_peaks': {'height': 20}
    }
}

experiment = Experiment(data_dict)
print("Date:", experiment.get_date())
print("Signal Length:", experiment.get_signal_length())
experiment.plot_signal()
print("RR Statistics:", experiment.get_RR_statistics())

"""##Задача ** "Минигольф"

 в папке на githab
"""