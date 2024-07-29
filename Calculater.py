import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

# Функция для АВС анализа
def abc_analysis(df):
    df['Total Cost'] = df['Річна потреба'] * df['Ціна за одиницю, у.о.']
    df = df.sort_values(by='Total Cost', ascending=False)
    df['Cumulative Cost'] = df['Total Cost'].cumsum()
    df['Cumulative Cost %'] = 100 * df['Cumulative Cost'] / df['Total Cost'].sum()
    df['ABC Category'] = pd.cut(df['Cumulative Cost %'], bins=[0, 70, 90, 100], labels=['A', 'B', 'C'])
    return df

# Функция для построения кривой Лоренца
def plot_lorenz_curve(df, curve_color='blue', text_color='black', line_style='-'):
    sorted_df = df.sort_values(by='Total Cost')
    cumulative_cost = sorted_df['Total Cost'].cumsum()
    cumulative_cost_percent = cumulative_cost / cumulative_cost.iloc[-1]
    cumulative_items_percent = np.arange(1, len(df) + 1) / len(df)

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_items_percent, cumulative_cost_percent, label='Lorenz Curve', color=curve_color, linestyle=line_style)
    plt.plot([0,1], [0,1], 'k--', label='Equality Line')
    plt.xlabel('Cumulative Share of Items', color=text_color)
    plt.ylabel('Cumulative Share of Costs', color=text_color)
    plt.title('Lorenz Curve', color=text_color)
    plt.legend()
    plt.show()

# Функция для расчета вероятности банкротства по модели Альтмана z
def calculate_bankruptcy_probability(data):
    current_ratio = data['Оборотні засоби'] / data['Короткострокові зобовязання']
    debt_ratio = data['Загальний борг фірми'] / data['Загальні активи']
    profitability_ratio = data['Балансовий прибуток'] / data['Загальний обсяг продаж']
    accumulated_capital_ratio = data['Накопичений капітал'] / data['Капітал фірми']

    # Расчет модели Альтмана z
    z = 1.2 * current_ratio + 1.4 * accumulated_capital_ratio + 3.3 * profitability_ratio + 0.6 * debt_ratio

    return z

# Класс для графического интерфейса
class ABCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ABC Analysis, Lorenz Curve, and Bankruptcy Probability")
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        self.label = Label(self.root, text="Введите данные для ABC анализа")
        self.label.grid(row=0, column=0, columnspan=4)

        # Заголовки колонок для ABC анализа
        self.headers = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартість матеріалу"]
        for col_num, header in enumerate(self.headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=1, column=col_num)

        # Ввод данных для ABC анализа
        self.data_entries = []
        for i in range(10):
            entry_row = []
            for j in range(4):
                entry = Entry(self.root)
                entry.grid(row=i+2, column=j)
                entry_row.append(entry)
            self.data_entries.append(entry_row)
        
        self.calculate_total_cost_button = Button(self.root, text="Рассчитать Загальна вартість матеріалу", command=self.calculate_total_cost)
        self.calculate_total_cost_button.grid(row=12, column=0, columnspan=4)
        
        self.calculate_abc_button = Button(self.root, text="Рассчитать ABC анализ", command=self.calculate_abc)
        self.calculate_abc_button.grid(row=13, column=0, columnspan=4)

        self.curve_color_label = Label(self.root, text="Цвет кривой:")
        self.curve_color_label.grid(row=14, column=0)
        self.curve_color_entry = Entry(self.root)
        self.curve_color_entry.grid(row=14, column=1)
        
        self.text_color_label = Label(self.root, text="Цвет текста:")
        self.text_color_label.grid(row=14, column=2)
        self.text_color_entry = Entry(self.root)
        self.text_color_entry.grid(row=14, column=3)

        self.line_style_label = Label(self.root, text="Стиль линии (например, '-', '--', ':', '-.'):")
        self.line_style_label.grid(row=15, column=0)
        self.line_style_entry = Entry(self.root)
        self.line_style_entry.grid(row=15, column=1)
        
        self.plot_lorenz_curve_button = Button(self.root, text="Побудова Кривої Лоренца", command=self.plot_lorenz_curve)
        self.plot_lorenz_curve_button.grid(row=16, column=0, columnspan=4)

        # Заголовки колонок для расчета вероятности банкротства
        self.label_bankruptcy = Label(self.root, text="Вкажіть данні для розрахування банкрутства фірми")
        self.label_bankruptcy.grid(row=17, column=0, columnspan=4)

        self.bankruptcy_headers = ["Показник", "Значення"]
        for col_num, header in enumerate(self.bankruptcy_headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=18, column=col_num)

        # Ввод данных для расчета вероятности банкротства
        self.bankruptcy_entries = []
        self.bankruptcy_data = ["Оборотні засоби", "Короткострокові зобовязання", "Загальний борг фірми", "Загальні активи", "Балансовий прибуток", "Загальний обсяг продаж", "Накопичений капітал", "Капітал фірми"]
        for i, label_text in enumerate(self.bankruptcy_data):
            label = Label(self.root, text=label_text)
            label.grid(row=i+19, column=0)
            entry = Entry(self.root)
            entry.grid(row=i+19, column=1)
            self.bankruptcy_entries.append(entry)
        
        self.calculate_bankruptcy_button = Button(self.root, text="Розрахувати можливість банкрутства", command=self.calculate_bankruptcy)
        self.calculate_bankruptcy_button.grid(row=27, column=0, columnspan=4)
        
    def calculate_total_cost(self):
        for entry_row in self.data_entries:
            try:
                need = float(entry_row[1].get())
                price = float(entry_row[2].get())
                total_cost = need * price
                entry_row[3].delete(0, END)
                entry_row[3].insert(0, total_cost)
            except ValueError:
                entry_row[3].delete(0, END)
                entry_row[3].insert(0, "Ошибка")

    def calculate_abc(self):
        data = []
        for entry_row in self.data_entries:
            row = [entry.get() for entry in entry_row]
            data.append(row)
        
        # Преобразование данных в DataFrame
        columns = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартысть матерыалу"]
        df = pd.DataFrame(data, columns=columns)
        df['Річна потреба'] = df['Річна потреба'].astype(float)
        df['Ціна за одиницю, у.о.'] = df['Ціна за одиницю, у.о.'].astype(float)
        
        # Выполнение АВС анализа
        df = abc_analysis(df)
        
        # Отображение результатов в новом окне
        result_window = Toplevel(self.root)
        result_window.title("Результаты ABC анализа")
        
        a_category = df[df['ABC Category'] == 'A']
        b_category = df[df['ABC Category'] == 'B']
        c_category = df[df['ABC Category'] == 'C']
        
        # Отображение данных для категории A
        Label(result_window, text="A category").grid(row=0, column=0)
        for i, row in a_category.iterrows():
            Label(result_window, text=row['№ матеріалу']).grid(row=i+1, column=0)
        
        # Отображение данных для категории B
        Label(result_window, text="B category").grid(row=0, column=1)
        for i, row in b_category.iterrows():
            Label(result_window, text=row['№ матеріалу']).grid(row=i+1, column=1)
        
        # Отображение данных для категории C
        Label(result_window, text="C category").grid(row=0, column=2)
        for i, row in c_category.iterrows():
            Label(result_window, text=row['№ матеріалу']).grid(row=i+1, column=2)
        
    def plot_lorenz_curve(self):
        data = []
        for entry_row in self.data_entries:
            row = [entry.get() for entry in entry_row]
            data.append(row)
        
        # Преобразование данных в DataFrame
        columns = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартысть матерыалу"]
        df = pd.DataFrame(data, columns=columns)
        df['Річна потреба'] = df['Річна потреба'].astype(float)
        df['Ціна за одиницю, у.о.'] = df['Ціна за одиницю, у.о.'].astype(float)
        
        # Выполнение АВС анализа
        df = abc_analysis(df)
        
        # Получение цветов для графика
        curve_color = self.curve_color_entry.get() or 'blue'
        text_color = self.text_color_entry.get() or 'black'
        line_style = self.line_style_entry.get() or '-'
        
        # Построение кривой Лоренца
        plot_lorenz_curve(df, curve_color, text_color, line_style)
    
def calculate_bankruptcy(self):
    data = {}
    for i, entry in enumerate(self.bankruptcy_entries):
        try:
            data[self.bankruptcy_data[i]] = float(entry.get())
        except ValueError:
            result_label = Label(self.root, text="Ошибка ввода данных")
            result_label.grid(row=28, column=0, columnspan=4)
            return
    
    # Преобразование данных в DataFrame
    df = pd.DataFrame([data])
    
    # Расчет вероятности банкротства
    z = calculate_bankruptcy_probability(df)
    
    # Вывод результата
    if z > 2.99:
        result_text = "Фірма тверда та впевнена у своїх можливостях"
    elif 1.81 < z <= 2.99:
        result_text = "Фірма може збанкротіти"
    else:
        result_text = "Фірма банкрут"
    
    result_label = Label(self.root, text=result_text)
    result_label.grid(row=28, column=0, columnspan=4)
    
if __name__ == "__main__":
    root = Tk()
    app = ABCApp(root)
    root.mainloop()
