#многоканальная СМО с отказами число каналов 5
import math
class SMOMultiChannel:
    def __init__(self):
        self.lam = None
        self.mu = None
        self.n = None
        self.data_entered = False

    def input_data(self):
        print("\n--- Ввод исходных данных ---")
        try:
            self.lam = float(input("Введите λ (интенсивность входящего потока): "))
            self.mu = float(input("Введите μ (интенсивность обслуживания одного канала): "))
            self.n = int(input("Введите n (число каналов обслуживания, например, 5): "))

            if self.mu <= 0:
                print("Ошибка: μ должна быть больше 0.")
                return
            if self.n <= 0:
                print("Ошибка: число каналов n должно быть больше 0.")
                return

            self.data_entered = True
            print("[✓] Данные успешно сохранены.")
        except ValueError:
            print("Ошибка: Введите корректные числовые значения (n должно быть целым).")

    def calculate_param(self, choice):
        if not self.data_entered:
            print("\n[!] Сначала введите данные (Пункт 1)!")
            return

        # 1. Приведенная интенсивность
        rho = self.lam / self.mu

        # Скрытый расчет P0 в точном соответствии с формулой: (Сумма(rho^k / k!))^-1
        p0 = sum((rho ** k) / math.factorial(k) for k in range(self.n + 1)) ** -1

        # Расчет остальных параметров строго по формулам с картинок
        p_otk = ((rho ** self.n) / math.factorial(self.n)) * p0
        q = 1 - p_otk
        A = self.lam * q
        p_serv = q
        k_bar = A / self.mu  # или rho * (1 - p_otk)

        print("\n--- Результат расчета ---")
        if choice == '1':
            print(f"1. Приведенная интенсивность (ρ = λ/μ): {rho:.4f}")
        elif choice == '2':
            print(f"2. Вероятность отказа (P_otk = (ρ^n / n!) * P0): {p_otk:.4f}")
        elif choice == '3':
            print(f"3. Относительная пропускная способность (q = 1 - P_otk): {q:.4f}")
        elif choice == '4':
            print(f"4. Абсолютная пропускная способность (A = λ * q): {A:.4f}")
        elif choice == '5':
            print(f"5. Вероятность обслуживания (P_serv = q): {p_serv:.4f}")
        elif choice == '6':
            print(f"6. Среднее число занятых каналов (k_bar = A/μ): {k_bar:.4f}")


def main():
    calc = SMOMultiChannel()

    while True:
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        print("1. Ввести исходные данные (λ, μ и n)")
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

            print("\n--- ВЫБОР ПАРАМЕТРА ДЛЯ РАСЧЕТА ---")
            print("1. Приведенная интенсивность (ρ)")
            print("2. Вероятность отказа (P_otk)")
            print("3. Относительная пропускная способность (q)")
            print("4. Абсолютная пропускная способность (A)")
            print("5. Вероятность обслуживания (P_serv)")
            print("6. Среднее число занятых каналов (k_bar)")
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

