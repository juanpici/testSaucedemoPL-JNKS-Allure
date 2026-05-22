import pytest
from playwright.sync_api import Page, expect

# 1. Pruebas de Login Parametrizadas (Flujos correctos e incorrectos)
@pytest.mark.parametrize("username,password,should_succeed", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user", "wrong_password", False)
])
def test_login_flow(page: Page, username, password, should_succeed):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill(username)
    page.locator("[data-test='password']").fill(password)
    page.locator("[data-test='login-button']").click()
    
    if should_succeed:
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    else:
        expect(page.locator("[data-test='error']")).to_be_visible()

# 2. Flujo Integrado: Agregar al carrito y verificar persistencia
def test_cart_management(page: Page):
    # Login funcional rápido
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # Agregar dos productos
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    
    # Validar contador del carrito
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")
    
    # Entrar al carrito y verificar que estén los productos
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".cart_item")).to_have_count(2)

# 3. Flujo E2E Completo: Compra Exitosa
def test_end_to_end_purchase(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # Agregar producto e ir al checkout
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()

    # Formulario de envío
    page.locator("[data-test='firstName']").fill("Juan Pablo")
    page.locator("[data-test='lastName']").fill("Cintioli")
    page.locator("[data-test='postalCode']").fill("03001")
    page.locator("[data-test='continue']").click()

    # Finalizar
    page.locator("[data-test='finish']").click()
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

# 4. Prueba de UI: Filtros de ordenamiento
def test_product_sorting(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # Ordenar por precio (Low to High)
    page.locator("[data-test='product-sort-container']").select_option("lohi")
    
    # Capturar los precios de los productos expuestos
    prices = page.locator(".inventory_item_price").all_inner_texts()
    prices_floats = [float(p.replace("$", "")) for p in prices]
    
    # Validar que la lista esté ordenada ascendentemente
    assert prices_floats == sorted(prices_floats)
