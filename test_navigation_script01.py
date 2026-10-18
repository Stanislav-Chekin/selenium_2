import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestBrowserNavigation:
    FORM_URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    GOOGLE_URL = "https://www.google.com/"

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        yield
        # TODO реализован: quit() полностью закрывает драйвер и все вкладки.
        self.driver.quit()

    def test_browser_navigation(self):
        """Триангуляция: проверка REFRESH, BACK, FORWARD"""
        # 1. Открываем страницу формы
        self.driver.get(self.FORM_URL)

        # 👇 ИСПРАВЛЕНО: ждем "Practice Form"
        self.wait.until(ec.title_contains("Practice Form"))
        assert "Practice Form" in self.driver.title

        # 2. REFRESH (Обновление страницы)
        self.driver.refresh()
        assert "Practice Form" in self.driver.title

        # 3. Переходим на Google
        self.driver.get(self.GOOGLE_URL)
        # Ждем загрузки Гугла, так как он может грузиться дольше
        self.wait.until(ec.title_contains("Google"))
        assert "Google" in self.driver.title

        # 4. BACK (Назад на страницу формы)
        self.driver.back()
        self.wait.until(ec.title_contains("Practice Form"))
        assert "Practice Form" in self.driver.title

        # 5. FORWARD (Вперед на Google)
        self.driver.forward()
        self.wait.until(ec.title_contains("Google"))
        assert "Google" in self.driver.title

    def test_open_new_tab(self):
        """Демонстрация разницы между close() и quit()"""
        self.driver.get(self.FORM_URL)
        self.wait.until(ec.title_contains("Practice Form"))

        # Открываем новую вкладку через JavaScript
        self.driver.execute_script("window.open('https://www.google.com/', '_blank');")

        # Переключаемся на новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.wait.until(ec.title_contains("Google"))
        assert "Google" in self.driver.title

        # Закрываем ТОЛЬКО текущую вкладку (Google)
        self.driver.close()

        # Переключаемся обратно на первую вкладку (Форма)
        self.driver.switch_to.window(self.driver.window_handles[0])

        # 👇 ИСПРАВЛЕНО: проверяем "Practice Form"
        assert "Practice Form" in self.driver.title
