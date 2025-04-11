from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
def scrape_cars():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://auto.ria.com/uk/search/")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    car_blocks = soup.find_all("div", class_="content-bar")
    
    if not car_blocks:
        print("No car blocks found")
        return []

    cars = []

    for block in car_blocks:
        try:
            # Назва, марка, модель, рік
            title_tag = block.select_one(".ticket-title a.address")
            full_title = title_tag.text.strip() if title_tag else "Unknown"
            parts = full_title.split()
            make = parts[0] if len(parts) > 0 else "Unknown"
            model = " ".join(parts[1:-1]) if len(parts) > 2 else "Unknown"
            year = int(parts[-1]) if parts[-1].isdigit() else 0

            # Ціна
            price_tag = block.select_one(".price-ticket .green")
            price = 0.0
            if price_tag:
                price_text = price_tag.text.strip().replace(' ', '').replace('$', '').replace('₴', '')
                try:
                    price = float(price_text)
                except ValueError:
                    price = 0.0

            # Локація
            location_tag = block.select_one(".view-location.js-location")
            location = location_tag.text.strip() if location_tag else "Unknown"

            # Зображення
            image_tag = block.select_one(".ticket-photo img")
            image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else "No image"

            # Характеристики
            characteristics = block.select("ul.characteristic li.item-char")
            engine_info = characteristics[0].text.strip() if len(characteristics) > 0 else "Unknown"

            # Пробіг
            mileage = "Unknown"
            mileage_tag = block.select_one(".item-char.js-race")
            if mileage_tag:
                mileage = mileage_tag.text.strip().replace(' ', '').replace('км', '')

            # Розбиття engine_info на об’єм і тип пального
            engine_volume, engine_type = "0.0", "Unknown"
            if ',' in engine_info:
                parts = engine_info.replace("л.", "").split(',')
                if len(parts) == 2:
                    engine_volume = float(parts[0].strip())
                    engine_type = parts[1].strip()

            # Трансмісія
            transmission = "Unknown"
            transmission_tag = block.select_one(".item-char") 
            if transmission_tag:
                transmission = transmission_tag.text.strip()
            
            car = {
                "make": make,
                "model": model,
                "year": year,
                "price": price,
                "mileage": mileage,
                "engine_type": engine_type,
                "engine_volume": engine_volume,
                "transmission": transmission,
                "location": location,
                "image_url": image_url
            }
            cars.append(car)

        except Exception as e:
            print(f"Error parsing car: {e}")
            continue

    driver.quit()
    return cars
