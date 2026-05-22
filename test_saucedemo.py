from playwright.sync_api import Page, expect

def test_e2e_shopping_flow(page: Page):
    # Primero vamos a la web del software in test
    page.goto("https://www.saucedemo.com/")
    
    # Mecanismo de Login
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # Una compra basica
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")
    page.click("#checkout")
    
    # Nos pide datos
    page.fill("#first-name", "Juan")
    page.fill("#last-name", "QA")
    page.fill("#postal-code", "03001")
    page.click("#continue")
    
    # 5. check y fin
    page.click("#finish")
    expect(page.locator(".complete-header")).to_contain_text("Thank you for your order")
