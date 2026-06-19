# одноканальная СМО с НЕОГРАНИЧЕННОЙ очередью
class SMOUnlimited:
    def __init__(self):
        self.lam = None
        self.mu = None
        self.data_entered = False

    def input_data(self):
        print("\n--- Ввод исходных данных ---")
        try:
            self.lam = float(input("Введите λ (интенсивность входящего потока): "))
            self.mu = float(input("Введите μ (интенсивность выходящего потока): "))

            if self.mu <= 0 or self.lam <= 0:
                print("Ошибка: Интенсивности λ и μ должны быть больше 0.")
                return

            # Главное условие для СМО с бесконечной очередью: ρ < 1
            if self.lam >= self.mu:
                print("\n[!] ОШИБКА: λ >= μ (ρ >= 1).")
                print("В СМО с неограниченной очередью при ρ >= 1 очередь будет расти бесконечно.")
                print("Стационарный режим невозможен. Введите λ < μ.")
                return

            self.data_entered = True
            print("[✓] Данные успешно сохранены.")
        except ValueError:
            print("Ошибка: Введите числовое значение.")

    def calculate_p0_pk(self, rho):
        """Расчет P0 и Pk для неограниченной очереди"""
        print(f"\n--- РАСЧЕТ ВЕРОЯТНОСТЕЙ СОСТОЯНИЙ (P0 и Pk) ---")
        p0 = 1 - rho
        print(f"Вероятность простоя СМО (P0) = 1 - ρ = {p0:.6f}")

        try:
            k_limit = int(input("Введите количество состояний k для расчета Pk (например, 5): "))
            if k_limit <= 0:
                print("Число k должно быть больше 0.")
                return

            print(f"--- Расчет Pk = ρ^k * P0 (для k от 1 до {k_limit}) ---")
            for k in range(1, k_limit + 1):
                pk = (rho ** k) * p0
                print(f"P_{k} = {pk:.6f}")
        except ValueError:
            print("Ошибка: Введите целое число.")

    def calculate_param(self, choice):
        if not self.data_entered:
            print("\n[!] Сначала введите данные (Пункт 1)!")
            return

        # Базовый параметр
        rho = self.lam / self.mu

        if choice == '1':
            print(f"\n1. Приведенная интенсивность (ρ = λ/μ): {rho:.4f}")

        elif choice == '2':
            self.calculate_p0_pk(rho)

        elif choice == '3':
            # В бесконечной очереди отказов нет
            print(f"\n3. Вероятность отказа (P_otk): 0.000000 (Очередь бесконечна, отказов нет)")

        elif choice == '4':
            # q = 1, A = lambda
            q = 1.0
            A = self.lam
            print(f"\n4. Относительная пропускная способность (q): {q:.6f}")
            print(f"   Абсолютная пропускная способность (A = λ): {A:.4f}")

        elif choice == '5':
            # r = rho^2 / (1 - rho)
            r = (rho ** 2) / (1 - rho)
            print(f"\n5. Среднее число заявок в очереди (r = ρ² / (1 - ρ)): {r:.4f}")

        elif choice == '6':
            # k = rho / (1 - rho)
            k_bar = rho / (1 - rho)
            print(f"\n6. Среднее число заявок в СМО (k = ρ / (1 - ρ)): {k_bar:.4f}")

        elif choice == '7':
            # t_wait = rho^2 / (lambda * (1 - rho))
            t_wait = (rho ** 2) / (self.lam * (1 - rho))
            print(f"\n7. Среднее время ожидания в очереди (t_wait = ρ² / [λ(1 - ρ)]): {t_wait:.4f}")

        elif choice == '8':
            # t_smo = 1 / (mu * (1 - rho))
            t_smo = 1 / (self.mu * (1 - rho))
            print(f"\n8. Среднее время пребывания в СМО (t_smo = 1 / [μ(1 - ρ)]): {t_smo:.4f}")


def main():
    calc = SMOUnlimited()

    while True:
        print("\n========== ГЛАВНОЕ МЕНЮ ==========")
        print("Одноканальная СМО с НЕОГРАНИЧЕННОЙ очередью")
        print("1. Ввести исходные данные (λ, μ)")
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
            print("2. Вероятности состояний (P0, Pk)")
            print("3. Вероятность отказа (P_otk)")
            print("4. Пропускная способность (q и A)")
            print("5. Среднее число заявок в очереди (r)")
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