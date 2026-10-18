import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.window import WindowTypes


class TestWindowManagement:
    FORM_URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    GOOGLE_URL = "https://www.google.com/"

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        yield
        # quit() закрывает все вкладки и завершает процесс драйвера (безопасно)
        self.driver.quit()

    def test_switch_and_close_tabs(self):
        """Триангуляция: работа с Window Handles, переключение и закрытие вкладок"""

        # 1. Открываем исходную страницу и сохраняем дескриптор
        self.driver.get(self.FORM_URL)
        self.wait.until(ec.title_contains("Practice Form"))
        original_window = self.driver.current_window_handle
        assert original_window is not None

        # 2. Открываем НОВУЮ ВКЛАДКУ
        self.driver.switch_to.new_window(WindowTypes.TAB)

        # Ждем, пока количество вкладок станет равно 2
        self.wait.until(ec.number_of_windows_to_be(2))

        # 3. Загружаем сайт на новой вкладке
        self.driver.get(self.GOOGLE_URL)
        self.wait.until(ec.title_contains("Google"))
        assert "Google" in self.driver.title

        # 4. ПЕРЕКЛЮЧЕНИЕ обратно на главную страницу формы
        self.driver.switch_to.window(original_window)
        self.wait.until(ec.title_contains("Practice Form"))

        # Докажем, что мы вернулись
        assert "Practice Form" in self.driver.title

        # 5. Закрытие конкретной вкладки (TODO: close vs quit)
        # Получаем список всех открытых вкладок
        all_windows = self.driver.window_handles

        # Переключаемся на вторую вкладку (Google) и закрываем её
        for window in all_windows:
            if window != original_window:
                self.driver.switch_to.window(window)
                self.driver.close()  # close() закрывает ТЕКУЩУЮ вкладку

        # Ждем, пока останется 1 вкладка
        self.wait.until(ec.number_of_windows_to_be(1))

        # Возвращаем фокус драйвера на оставшуюся вкладку
        self.driver.switch_to.window(original_window)

        # Если бы мы случайно вызвали quit(), драйвер бы умер, и следующая строка выдала бы ошибку.
        # То, что мы можем проверить заголовок — доказывает, что сессия жива после close().
        assert "Practice Form" in self.driver.title

