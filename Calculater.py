import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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

    return z.iloc[0]  # Возвращаем только одно значение

# Перевод текста
translations = {
    "en": {
        "title": "ABC Analysis, Lorenz Curve, and Bankruptcy Probability",
        "abc_label": "Enter data for ABC analysis",
        "headers": ["Material No.", "Annual Demand", "Price per Unit", "Total Material Cost"],
        "calculate_total_cost": "Calculate Total Material Cost",
        "calculate_abc": "Calculate ABC Analysis",
        "curve_color_label": "Curve Color:",
        "text_color_label": "Text Color:",
        "line_style_label": "Line Style (e.g., '-', '--', ':', '-.'):",
        "plot_lorenz_curve": "Plot Lorenz Curve",
        "bankruptcy_label": "Enter data for bankruptcy calculation",
        "bankruptcy_headers": ["Indicator", "Value"],
        "calculate_bankruptcy": "Calculate Bankruptcy Probability",
        "result_title": "Bankruptcy Calculation Result",
        "firm_stable": "The firm is stable and confident in its capabilities",
        "firm_may_fail": "The firm may go bankrupt",
        "firm_bankrupt": "The firm is bankrupt",
        "error": "Error"
    },
    "ua": {
        "title": "ABC Аналіз, Крива Лоренца та Можливість Банкрутства",
        "abc_label": "Введіть дані для ABC аналізу",
        "headers": ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартість матеріалу"],
        "calculate_total_cost": "Розрахувати Загальну вартість матеріалу",
        "calculate_abc": "Розрахувати ABC аналіз",
        "curve_color_label": "Колір кривої:",
        "text_color_label": "Колір тексту:",
        "line_style_label": "Стиль лінії (наприклад, '-', '--', ':', '-.'):",
        "plot_lorenz_curve": "Побудувати Криву Лоренца",
        "bankruptcy_label": "Вкажіть дані для розрахунку банкрутства",
        "bankruptcy_headers": ["Показник", "Значення"],
        "calculate_bankruptcy": "Розрахувати можливість банкрутства",
        "result_title": "Результат розрахунку банкрутства",
        "firm_stable": "Фірма тверда та впевнена у своїх можливостях",
        "firm_may_fail": "Фірма може збанкротіти",
        "firm_bankrupt": "Фірма банкрут",
        "error": "Помилка"
    }
}

class ABCApp:
    def __init__(self, root):
        self.root = root
        self.language = "en"  # По умолчанию английский
        self.root.title(translations[self.language]["title"])
        self.root.iconbitmap(r'D:\Spase IT\Python Develop\Python to LinkedIn\Universitet task\Icon')  # Nikita Golubev create icon
        self.create_widgets()
        
    def create_widgets(self):
        self.label = Label(self.root, text=translations[self.language]["abc_label"])
        self.label.grid(row=0, column=0, columnspan=4)

        # Заголовки колонок для ABC анализа
        self.headers = translations[self.language]["headers"]
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
        
        self.calculate_total_cost_button = Button(self.root, text=translations[self.language]["calculate_total_cost"], command=self.calculate_total_cost)
        self.calculate_total_cost_button.grid(row=12, column=0, columnspan=4)
        
        self.calculate_abc_button = Button(self.root, text=translations[self.language]["calculate_abc"], command=self.calculate_abc)
        self.calculate_abc_button.grid(row=13, column=0, columnspan=4)

        self.curve_color_label = Label(self.root, text=translations[self.language]["curve_color_label"])
        self.curve_color_label.grid(row=14, column=0)
        self.curve_color_entry = Entry(self.root)
        self.curve_color_entry.grid(row=14, column=1)
        
        self.text_color_label = Label(self.root, text=translations[self.language]["text_color_label"])
        self.text_color_label.grid(row=14, column=2)
        self.text_color_entry = Entry(self.root)
        self.text_color_entry.grid(row=14, column=3)

        self.line_style_label = Label(self.root, text=translations[self.language]["line_style_label"])
        self.line_style_label.grid(row=15, column=0)
        self.line_style_entry = Entry(self.root)
        self.line_style_entry.grid(row=15, column=1)
        
        self.plot_lorenz_curve_button = Button(self.root, text=translations[self.language]["plot_lorenz_curve"], command=self.plot_lorenz_curve)
        self.plot_lorenz_curve_button.grid(row=16, column=0, columnspan=4)

        # Заголовки колонок для расчета вероятности банкротства
        self.label_bankruptcy = Label(self.root, text=translations[self.language]["bankruptcy_label"])
        self.label_bankruptcy.grid(row=17, column=0, columnspan=4)

        self.bankruptcy_headers = translations[self.language]["bankruptcy_headers"]
        for col_num, header in enumerate(self.bankruptcy_headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=18, column=col_num)

        # Ввод данных для расчета вероятности банкротства
        self.bankruptcy_entries = []
        self.bankruptcy_data = ["Оборотні засоби", "Короткострокові зобовязання", "Загальний борг фірми", "Загальні активи", "Балансовий прибуток", "Загальний обсяг продаж", "Накопичений капітал", "Капітал фірми"]
        for i, label_text in enumerate(self.bankruptcy_data):
            label = Label(self.root, text=label_text)
            label.grid(row=19+i, column=0)
            entry = Entry(self.root)
            entry.grid(row=19+i, column=1)
            self.bankruptcy_entries.append(entry)

        self.calculate_bankruptcy_button = Button(self.root, text=translations[self.language]["calculate_bankruptcy"], command=self.calculate_bankruptcy)
        self.calculate_bankruptcy_button.grid(row=27, column=0, columnspan=2)

        # Индикатор выполнения
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress.grid(row=28, column=0, columnspan=2)
        
    def calculate_total_cost(self):
        try:
            total_cost = 0
            for row in self.data_entries:
                annual_demand = float(row[1].get())
                unit_price = float(row[2].get())
                total_cost += annual_demand * unit_price
            messagebox.showinfo("Total Cost", f"Total Cost: {total_cost:.2f} u.o.")
        except ValueError:
            messagebox.showerror(translations[self.language]["error"], "Invalid input for Total Cost calculation.")
    
    def calculate_abc(self):
        try:
            data = {
                "Material No.": [row[0].get() for row in self.data_entries],
                "Annual Demand": [float(row[1].get()) for row in self.data_entries],
                "Price per Unit": [float(row[2].get()) for row in self.data_entries],
                "Total Material Cost": [float(row[1].get()) * float(row[2].get()) for row in self.data_entries]
            }
            df = pd.DataFrame(data)
            df = abc_analysis(df)
            df.to_csv('abc_analysis_result.csv', index=False)
            messagebox.showinfo("ABC Analysis Result", "ABC Analysis result saved to 'abc_analysis_result.csv'.")
        except ValueError:
            messagebox.showerror(translations[self.language]["error"], "Invalid input for ABC Analysis.")

    def plot_lorenz_curve(self):
        try:
            curve_color = self.curve_color_entry.get()
            text_color = self.text_color_entry.get()
            line_style = self.line_style_entry.get()
            
            data = {
                "Material No.": [row[0].get() for row in self.data_entries],
                "Annual Demand": [float(row[1].get()) for row in self.data_entries],
                "Price per Unit": [float(row[2].get()) for row in self.data_entries],
                "Total Material Cost": [float(row[1].get()) * float(row[2].get()) for row in self.data_entries]
            }
            df = pd.DataFrame(data)
            df = abc_analysis(df)
            
            self.progress['value'] = 20
            self.root.update_idletasks()
            plot_lorenz_curve(df, curve_color=curve_color, text_color=text_color, line_style=line_style)
            
            self.progress['value'] = 100
            self.root.update_idletasks()
            messagebox.showinfo("Plot", "Lorenz Curve plotted successfully.")
        except ValueError:
            messagebox.showerror(translations[self.language]["error"], "Invalid input for Lorenz Curve plotting.")
        finally:
            self.progress['value'] = 0
    
    def calculate_bankruptcy(self):
        self.progress['value'] = 10
        self.root.update_idletasks()
        try:
            data = {name: float(entry.get()) for name, entry in zip(self.bankruptcy_data, self.bankruptcy_entries)}
            df = pd.DataFrame([data])
            probability = calculate_bankruptcy_probability(df)
            
            self.progress['value'] = 50
            self.root.update_idletasks()

            if probability > 2.5:
                result = translations[self.language]["firm_stable"]
            elif 1.8 < probability <= 2.5:
                result = translations[self.language]["firm_may_fail"]
            else:
                result = translations[self.language]["firm_bankrupt"]
            
            messagebox.showinfo(translations[self.language]["result_title"], result)
        except ValueError:
            messagebox.showerror(translations[self.language]["error"], "Invalid input for Bankruptcy calculation.")
        finally:
            self.progress['value'] = 100
            self.root.update_idletasks()
            self.progress['value'] = 0

root = Tk()
app = ABCApp(root)
root.mainloop()
