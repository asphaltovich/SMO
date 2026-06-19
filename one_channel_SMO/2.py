# одноканальная СМО с ограниченной очередью равной 5;
class SMOMenu:
    def __init__(self):
        self.lam = None
        self.mu = None
        self.m = None
        self.data_entered = False

    def input_data(self):
        print("\n--- Ввод исходных данных ---")
        try:
            self.lam = float(input("Введите λ (интенсивность входящего потока): "))
            self.mu = float(input("Введите μ (интенсивность выходящего потока): "))
            self.m = int(input("Введите m (длина очереди, m > 0): "))

            if self.mu <= 0:
                print("Ошибка: μ должна быть больше 0.")
                return
            if self.m <= 0:
                print("Ошибка: длина очереди m должна быть больше 0.")
                return

            self.data_entered = True
            print("[✓] Данные успешно сохранены.")
        except ValueError:
            print("Ошибка: Введите числовое значение.")

    def _auto_calc_base(self):
        """Внутренний метод для автоматического расчета базовых параметров,
        необходимых для сложных формул (k, t_wait, t_smo)"""
        rho = self.lam / self.mu

        # Авто-расчет P0
        if abs(rho - 1.0) < 1e-9:
            p0 = 1 / (self.m + 2)
        else:
            p0 = (1 - rho) / (1 - rho ** (self.m + 2))

        # Авто-расчет r (средняя длина очереди)
        if abs(rho - 1.0) < 1e-9:
            r_bar = (self.m * (self.m + 1)) / (2 * (self.m + 2))
        else:
            r_bar = (rho ** 2 * (1 - rho ** self.m * (self.m + 1 - self.m * rho))) / (
                        (1 - rho ** (self.m + 2)) * (1 - rho))

        p_otk = (rho ** (self.m + 1)) * p0
        q = 1 - p_otk

        return rho, p0, p_otk, q, r_bar

    def calculate_p0_pk_menu(self, rho):
        """Меню выбора формулы для P0 и расчет всех Pk (Фото 1)"""
        print(f"\n--- РАСЧЕТ ВЕРОЯТНОСТЕЙ СОСТОЯНИЙ (P0 и Pk) ---")
        print(f"Текущая приведенная интенсивность ρ = {rho:.4f}")
        print("Выберите формулу для расчета P0:")
        print("1. Для ρ ≠ 1: P0 = (1 - ρ) / (1 - ρ^(m+2))")
        print("2. Для ρ = 1: P0 = 1 / (m + 2)")
        print("3. Автоматический выбор по значению ρ")
        print("0. Назад")

        choice = input("Ваш выбор: ")
        p0 = None

        if choice == '1':
            if abs(rho - 1.0) < 1e-9:
                print("\n[!] ОШИБКА: ρ = 1. Формула приведет к делению на ноль!")
            else:
                p0 = (1 - rho) / (1 - rho ** (self.m + 2))
        elif choice == '2':
            p0 = 1 / (self.m + 2)
            if abs(rho - 1.0) > 1e-9:
                print("\n[!] Предупреждение: ρ ≠ 1. Результат математически некорректен.")
        elif choice == '3':
            if abs(rho - 1.0) < 1e-9:
                print("\n[Авто] Применена формула для ρ = 1.")
                p0 = 1 / (self.m + 2)
            else:
                print("\n[Авто] Применена формула для ρ ≠ 1.")
                p0 = (1 - rho) / (1 - rho ** (self.m + 2))
        elif choice == '0':
            return
        else:
            print("Неверный выбор.")
            return

        if p0 is not None:
            print(f"\n[Результат] Вероятность простоя (P0): {p0:.6f}")
            print(f"--- Расчет Pk = ρ^k * P0 (k от 1 до {self.m + 1}) ---")
            for k in range(1, self.m + 2):
                pk = (rho ** k) * p0
                print(f"P_{k} = {pk:.6f}")

    def calculate_r_menu(self, rho):
        """Меню выбора формулы для r (Фото 3)"""
        print(f"\n--- РАСЧЕТ СРЕДНЕГО ЧИСЛА ЗАЯВОК В ОЧЕРЕДИ (r) ---")
        print(f"Текущая приведенная интенсивность ρ = {rho:.4f}")
        print("Выберите формулу:")
        print("1. Для ρ ≠ 1: r = (ρ^2 * [1 - ρ^m * (m + 1 - m*ρ)]) / ((1 - ρ^(m+2)) * (1 - ρ))")
        print("2. Для ρ = 1: r = m * (m + 1) / (2 * (m + 2))")
        print("3. Автоматический выбор по значению ρ")
        print("0. Назад")

        choice = input("Ваш выбор: ")

        if choice == '1':
            if abs(rho - 1.0) < 1e-9:
                print("\n[!] ОШИБКА: ρ = 1. Формула приведет к делению на ноль!")
            else:
                r = (rho ** 2 * (1 - rho ** self.m * (self.m + 1 - self.m * rho))) / (
                            (1 - rho ** (self.m + 2)) * (1 - rho))
                print(f"\n[Результат] Среднее число заявок в очереди (r): {r:.4f}")
        elif choice == '2':
            r = (self.m * (self.m + 1)) / (2 * (self.m + 2))
            print(f"\n[Результат] Среднее число заявок в очереди (r): {r:.4f}")
            if abs(rho - 1.0) > 1e-9:
                print("[!] Предупреждение: ρ ≠ 1. Результат математически некорректен.")
        elif choice == '3':
            if abs(rho - 1.0) < 1e-9:
                print("\n[Авто] Применена формула для ρ = 1.")
                r = (self.m * (self.m + 1)) / (2 * (self.m + 2))
            else:
                print("\n[Авто] Применена формула для ρ ≠ 1.")
                r = (rho ** 2 * (1 - rho ** self.m * (self.m + 1 - self.m * rho))) / (
                            (1 - rho ** (self.m + 2)) * (1 - rho))
            print(f"[Результат] Среднее число заявок в очереди (r): {r:.4f}")

    def calculate_param(self, choice):
        if not self.data_entered:
            print("\n[!] Сначала введите данные (Пункт 1)!")
            return

        # Получаем базовые параметры для расчетов
        rho, p0, p_otk, q, r_bar = self._auto_calc_base()

        if choice == '1':
            print(f"\n1. Приведенная интенсивность (ρ = λ/μ): {rho:.4f}")
        elif choice == '2':
            self.calculate_p0_pk_menu(rho)
        elif choice == '3':
            # Фото 2: P_otk = P_m+1
            print(f"\n3. Вероятность отказа (P_otk = P_m+1): {p_otk:.6f}")
        elif choice == '4':
            # Фото 2: q = 1 - P_otk, A = λ * q
            A = self.lam * q
            print(f"\n4. Относительная пропускная способность (q = 1 - P_otk): {q:.6f}")
            print(f"   Абсолютная пропускная способность (A = λ * q): {A:.4f}")
        elif choice == '5':
            self.calculate_r_menu(rho)
        elif choice == '6':
            # Фото 3: k = r + 1 - p0
            k_bar = r_bar + 1 - p0
            print(f"\n6. Среднее число заявок в СМО (k = r + 1 - P0): {k_bar:.4f}")
        elif choice == '7':
            # Фото 3: t_wait = r / λ
            t_wait = r_bar / self.lam
            print(f"\n7. Среднее время ожидания в очереди (t_wait = r / λ): {t_wait:.4f}")
        elif choice == '8':
            # Фото 3: t_smo = r / λ + q / μ
            t_smo = (r_bar / self.lam) + (q / self.mu)
            print(f"\n8. Среднее время пребывания в СМО (t_smo = r / λ + q / μ): {t_smo:.4f}")


def main():
    calc = SMOMenu()

    while True:
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        print("Одноканальная СМО с ограниченной очередью")
        print("1. Ввести исходные данные (λ, μ, m)")
        print("2. Выбрать расчет показателя")
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
            print("2. Вероятности состояний (P0, P1... P_m+1) -> ОТКРЫТЬ МЕНЮ ФОРМУЛ")
            print("3. Вероятность отказа (P_otk)")
            print("4. Пропускная способность (q и A)")
            print("5. Среднее число заявок в очереди (r) -> ОТКРЫТЬ МЕНЮ ФОРМУЛ")
            print("6. Среднее число заявок в СМО (k)")
            print("7. Среднее время ожидания в очереди (t_wait)")
            print("8. Среднее время пребывания в СМО (t_smo)")
            print("0. Назад в главное меню")
            print("------------------------------------")

            param_choice = input("Выберите номер показателя: ")

            if param_choice == '0':
                continue
            elif param_choice in [str(i) for i in range(1, 9)]:
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

