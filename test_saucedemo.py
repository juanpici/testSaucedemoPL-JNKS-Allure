import pytest
from playwright.sync_api import Page, expect

# Helper para no repetir el login como un bot
def loguearse(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

@pytest.mark.parametrize("user,password,espera_exito", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user", "wrong_password", False)
])
def test_login_flow(page: Page, user, password, espera_exito):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill(user)
    page.locator("[data-test='password']").fill(password)
    page.locator("[data-test='login-button']").click()
    
    if espera_exito:
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    else:
        expect(page.locator("[data-test='error']")).to_be_visible()

def test_cart_management(page: Page):
    loguearse(page)
    
    # Meto un par de productos al carrito
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")
    
    # Chequeo que sigan estando adentro de la lista
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".cart_item")).to_have_count(2)

def test_remove_from_cart(page: Page):
    loguearse(page)
    
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator(".shopping_cart_link").click()
    
    # Lo saco directamente desde la vista del carrito y valido que se limpie el badge
    page.locator("[data-test='remove-sauce-labs-backpack']").click()
    expect(page.locator(".cart_item")).to_have_count(0)
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()

def test_end_to_end_purchase(page: Page):
    loguearse(page)

    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()

    # Formulario con datos de envío
    page.locator("[data-test='firstName']").fill("Juan Pablo")
    page.locator("[data-test='lastName']").fill("Cintioli")
    page.locator("[data-test='postalCode']").fill("03001")
    page.locator("[data-test='continue']").click()

    # Cierro la compra de una
    page.locator("[data-test='finish']").click()
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

def test_checkout_validation_errors(page: Page):
    loguearse(page)
    
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()
    
    # Le mando continuar sin llenar nada para romper el flujo a propósito
    page.locator("[data-test='continue']").click()
    expect(page.locator("[data-test='error']")).to_contain_text("Error: First Name is required")

def test_product_sorting(page: Page):
    loguearse(page)

    # Ordeno por precio de menor a mayor
    page.locator("[data-test='product-sort-container']").select_option("lohi")
    
    precios = page.locator(".inventory_item_price").all_inner_texts()
    precios_limpios = [float(p.replace("$", "")) for p in precios]
    
    assert precios_limpios == sorted(precios_limpios)

def test_logout_flow(page: Page):
    loguearse(page)
    
    # Abro el menú del costado y lo saco de la sesión
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    
    # Tiene que rebotar al home del login sin dejar rastro
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("[data-test='login-button']")).to_be_visible()
