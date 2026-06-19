import math

class SMOMultiChannelInfiniteQueue:
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

            # Проверка на стабильность системы (ρ < n)
            rho = self.lam / self.mu
            if rho >= self.n:
                print(f"\n[!] ОШИБКА: Система нестабильна!")
                print(f"Приведенная интенсивность ρ ({rho:.2f}) должна быть меньше числа каналов n ({self.n}).")
                print("Иначе очередь будет расти до бесконечности. Введите другие данные.")
                self.data_entered = False
                return

            self.data_entered = True
            print("[✓] Данные успешно сохранены. Система стабильна.")
        except ValueError:
            print("Ошибка: Введите корректные числовые значения (n должно быть целым).")

    def calculate_param(self, choice):
        if not self.data_entered:
            print("\n[!] Сначала введите корректные данные (Пункт 1)!")
            return

        # 1. Приведенная интенсивность
        rho = self.lam / self.mu

        # Расчет P0 по формуле со слайда 1
        sum_part = sum((rho ** k) / math.factorial(k) for k in range(self.n + 1))
        last_term = (rho ** (self.n + 1)) / (math.factorial(self.n) * (self.n - rho))
        p0 = (sum_part + last_term) ** -1

        # Вероятность образования очереди (слайд 2)
        p_och = ((rho ** (self.n + 1)) / (math.factorial(self.n) * (self.n - rho))) * p0

        # Среднее число заявок в очереди (слайд 3)
        l_och = (self.n / (self.n - rho)) * p_och

        # Абсолютная пропускная способность (для СМО с неограниченной очередью A = λ, так как отказов нет)
        A = self.lam

        # Среднее время ожидания в очереди (слайд 3)
        t_och = l_och / A

        # Среднее число занятых каналов (слайд 3)
        n_z = rho

        # Среднее число свободных каналов (слайд 3)
        n_sv = self.n - rho

        # Коэффициент занятости каналов (слайд 3)
        k_z = rho / self.n

        print("\n--- Результат расчета ---")
        if choice == '1':
            print(f"1. Приведенная интенсивность (ρ = λ/μ): {rho:.4f}")
        elif choice == '2':
            print(f"2. Вероятность простоя системы (P0): {p0:.4f}")
        elif choice == '3':
            print(f"3. Вероятность образования очереди (P_och): {p_och:.4f}")
        elif choice == '4':
            print(f"4. Среднее число заявок в очереди (L_och): {l_och:.4f}")
        elif choice == '5':
            print(f"5. Среднее время ожидания в очереди (T_och): {t_och:.4f}")
        elif choice == '6':
            print(f"6. Среднее число занятых каналов (n_z = ρ): {n_z:.4f}")
        elif choice == '7':
            print(f"7. Среднее число свободных каналов (n_sv = n - ρ): {n_sv:.4f}")
        elif choice == '8':
            print(f"8. Коэффициент занятости каналов (K_z = ρ/n): {k_z:.4f}")
        elif choice == '9':
            print(f"ρ = {rho:.4f}")
            print(f"P0 = {p0:.4f}")
            print(f"P_och = {p_och:.4f}")
            print(f"L_och = {l_och:.4f}")
            print(f"T_och = {t_och:.4f}")
            print(f"n_z = {n_z:.4f}")
            print(f"n_sv = {n_sv:.4f}")
            print(f"K_z = {k_z:.4f}")


def main():
    calc = SMOMultiChannelInfiniteQueue()

    while True:
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        print("СМО: Многоканальная с неограниченной очередью")
        print("1. Ввести исходные данные (λ, μ и n)")
        print("2. Выбрать расчет параметра")
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
            print("2. Вероятность простоя системы (P0)")
            print("3. Вероятность образования очереди (P_och)")
            print("4. Среднее число заявок в очереди (L_och)")
            print("5. Среднее время ожидания в очереди (T_och)")
            print("6. Среднее число занятых каналов (n_z)")
            print("7. Среднее число свободных каналов (n_sv)")
            print("8. Коэффициент занятости каналов (K_z)")
            print("9. Вывести ВСЕ параметры сразу")
            print("0. Назад в главное меню")
            print("------------------------------------")

            param_choice = input("Выберите номер параметра: ")

            if param_choice == '0':
                continue
            elif param_choice in [str(i) for i in range(1, 10)]:
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