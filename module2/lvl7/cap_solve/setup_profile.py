from browser import PROFILE_DIR, create_driver, installed_extensions

WEB_STORE_URL = "https://chromewebstore.google.com/"


def main() -> None:
    with create_driver() as driver:
        driver.get(WEB_STORE_URL)
        print(f"Профіль: {PROFILE_DIR}")
        input("Встанови розширення в браузері, потім натисни Enter тут... ")

        extensions = installed_extensions(driver)
        print("Розширення в профілі:")
        for extension in extensions:
            print(f"  - {extension['name']} ({extension['id']})")
        if not extensions:
            print("  поки жодного")


if __name__ == "__main__":
    main()
