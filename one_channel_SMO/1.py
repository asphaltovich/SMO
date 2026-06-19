# одноканальная СМО с отказами

class SMOMenu:
    def __init__(self):
        self.lam = None
        self.mu = None
        self.data_entered = False

    def input_data(self):
        print("\n--- Ввод исходных данных ---")
        try:
            self.lam = float(input("Введите λ (интенсивность входящего потока): "))
            self.mu = float(input("Введите μ (интенсивность выходящего потока): "))
            if self.mu <= 0:
                print("Ошибка: μ должна быть больше 0.")
                return
            self.data_entered = True
            print("[✓] Данные успешно сохранены.")
        except ValueError:
            print("Ошибка: Введите числовое значение.")

    def calculate_param(self, choice):
        if not self.data_entered:
            print("\n[!] Сначала введите данные (Пункт 1)!")
            return

        # Предварительный расчет всех параметров строго по формулам из картинки
        t_serv = 1 / self.mu
        rho = self.lam / self.mu
        q = 1 / (rho + 1)
        A = self.lam * q
        p_serv = q
        p_otk = 1 - p_serv

        print("\n--- Результат расчета ---")
        if choice == '1':
            print(f"1. Среднее время обслуживания (t_serv = 1/μ): {t_serv:.4f}")
        elif choice == '2':
            print(f"2. Приведенная интенсивность (ρ = λ/μ): {rho:.4f}")
        elif choice == '3':
            print(f"3. Относительная пропускная способность (q = 1/(ρ+1)): {q:.4f}")
        elif choice == '4':
            print(f"4. Абсолютная пропускная способность (A = λ*q): {A:.4f}")
        elif choice == '5':
            print(f"5. Вероятность обслуживания (P_serv = q): {p_serv:.4f}")
        elif choice == '6':
            print(f"6. Вероятность отказа (P_otk = 1 - P_serv): {p_otk:.4f}")


def main():
    calc = SMOMenu()

    while True:
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        print("1. Ввести исходные данные (λ и μ)")
        print("2. Выбрать расчет конкретного параметра")
        print("0. Выход")
        print("==================================")

        main_choice = input("Выберите действие: ")

        if main_choice == '1':
            calc.input_data()

        elif main_choice == '2':
            if not calc.data_entered:
                print("\n[!] Сначала введите данные (Пункт 1)!")
                continue

            # Порядок изменен в соответствии с расположением формул на картинке
            print("\n--- ВЫБОР ПАРАМЕТРА ДЛЯ РАСЧЕТА ---")
            print("1. Среднее время обслуживания (t_serv = 1 / μ)")
            print("2. Приведенная интенсивность (ρ = λ / μ)")
            print("3. Относительная пропускная способность (q = 1 / (ρ + 1))")
            print("4. Абсолютная пропускная способность (A = λ * q)")
            print("5. Вероятность обслуживания (P_serv = q)")
            print("6. Вероятность отказа (P_otk = 1 - P_serv)")
            print("0. Назад в главное меню")
            print("------------------------------------")

            param_choice = input("Выберите номер параметра: ")

            if param_choice == '0':
                continue
            elif param_choice in ['1', '2', '3', '4', '5', '6']:
                calc.calculate_param(param_choice)
            else:
                print("Неверный выбор параметра.")

        elif main_choice == '0':
            print("Программа завершена.")
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
