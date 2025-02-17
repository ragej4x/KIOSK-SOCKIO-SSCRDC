import pygame
import sys
from pygame.locals import *
from PIL import Image, ImageTk
import time , csv, json

pygame.init()
clock = pygame.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 600
BACKGROUND_COLOR = (241, 246, 249)
HEADER_COLOR = (255, 255, 255)
TEXT_COLOR = (10, 10, 10)
BUTTON_COLOR = (10, 10, 10)
BUTTON_HOVER_COLOR = (170, 170, 170)
KEYBOARD_COLOR = (200, 200, 200) 
KEY_TEXT_COLOR = (255, 255, 255) 
POPUP_COLOR = (255, 255, 255)

BUTTON_BACK_COLOR = (220, 53, 69)
BUTTON_PROCEED_COLOR = (40, 167, 69)
BUTTON_TEXT_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
banner = pygame.image.load("assets/banner.png")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("SOCKIO - San Sebastian College Recoletos De Cavite")

font = pygame.font.Font("poppins-light.ttf", 12)
header_font = pygame.font.SysFont("Arial", 22)
search_font = pygame.font.SysFont("Arial", 14)

class SockioApp: 
    def __init__(self):
        # categories for product filtering
        self.categories = ["All Meals", "Rice Meals", "Biscuits", "Drinks", "Icecream"]

        self.search_active = False
        self.search_text = ""
        self.products = [
            {"name": "Shanghai Rice Meal", "price": 50, "image": "assets/shanghai.png"},
            {"name": "Spaghetti", "price": 30, "image": "assets/spaghetti.png"},
            {"name": "Sinigang Rice Meal", "price": 55, "image": "assets/sinigang.png"},
            {"name": "Chicken Rice Meal", "price": 65, "image": "assets/chicken.png"},
            {"name": "C2 Drink", "price": 25, "image": "assets/c2.png"},
            {"name": "Gatorade Drink", "price":30, "image": "assets/gatorade.png"},
            {"name": "Water Bottle", "price": 15, "image": "assets/water.png"},
            {"name": "Frootees Biscuit", "price":10, "image": "assets/frootees.png"},
            {"name": "Butternut Biscuit", "price":10, "image": "assets/butternut.png"},
            {"name": "Berryknots Biscuits", "price":10, "image": "assets/berryknots.png"},
            {"name": "Corneto Icecream", "price":20, "image": "assets/corneto.png"},
            {"name": "Magnum Icecream", "price":50, "image": "assets/magnum.png"},
            {"name": "Selecta Icecream", "price":15, "image": "assets/selecta.png"},
            {"name": "Alice Icecream", "price":10, "image": "assets/alice.png"}
        ]
        self.filtered_products = self.products.copy()
        self.cart_items = []
        self.selected_product = None
        self.selected_quantity = 1
        self.virtual_keyboard = self.create_virtual_keyboard()
        self.keyboard_triggered = False  # Initialize the keyboard trigger state
        self.mouse_pressed = False
        self.view_checkout_bool = False
        # Scroll variables
        self.scroll_offset = 0  # Start position of the scroll
        self.scroll_bar_height = 0  # Height of the scroll bar handle
        self.mouse_drag_start_y = None  # Track the initial mouse Y position when dragging
        self.scroll_bar_rect = pygame.Rect(WINDOW_WIDTH - 15, 80, 15, WINDOW_HEIGHT - 80)  # Position and size of scroll barself.scroll_bar_rect = pygame.Rect(WINDOW_WIDTH - 15, 80, 15, WINDOW_HEIGHT - 80)  # Position and size of scroll bar
        self.add_to_cart_bool = False
    
        self.view_cart_bool = False
        self.cashin_bool = False

    def load_image(self, image_path, size=(100, 100)):
        try:
            img = Image.open(image_path)
            img = img.resize(size)  # Resize the image
            mode = img.mode
            size = img.size
            data = img.tobytes()
            return pygame.image.fromstring(data, size, mode)  # Convert to Pygame surface
        except Exception as e:
            #print(f"Error loading image {image_path}: {e}")
            return pygame.Surface(size)  # Return a placeholder surface if loading fails

    def draw_scroll_bar(self):
        total_height = len(self.filtered_products) * 220  # Total content height
        visible_area = WINDOW_HEIGHT - 80  # Visible window area for products

        # Calculate the size of the scroll handle
        if total_height > visible_area:
            self.scroll_bar_height = max(visible_area * visible_area / total_height, 40)
            handle_y = 80 + (self.scroll_offset * visible_area / total_height)
        else:
            self.scroll_bar_height = visible_area  # Full height if no scrolling
            handle_y = 80

        # Draw the scroll bar background
        pygame.draw.rect(screen, (200, 200, 200), self.scroll_bar_rect)

        # Draw the scroll handle (the draggable part of the scroll bar)
        scroll_handle_rect = pygame.Rect(
            self.scroll_bar_rect.x, handle_y, self.scroll_bar_rect.width, self.scroll_bar_height
        )
        pygame.draw.rect(screen, (100, 100, 100), scroll_handle_rect)


    def handle_scroll(self):
        """Handle scroll bar interaction with mouse events."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Check if the scrollbar handle is clicked and dragged
        if mouse_pressed and self.scroll_bar_rect.collidepoint(mouse_pos):
            if self.mouse_drag_start_y is None:
                self.mouse_drag_start_y = mouse_pos[1]  # Store initial Y position
            
            # Calculate drag distance
            delta_y = mouse_pos[1] - self.mouse_drag_start_y
            self.mouse_drag_start_y = mouse_pos[1]  # Update start position

            # Calculate proportional scroll offset
            total_height = len(self.filtered_products) * 220  # Total height of product list
            visible_area = WINDOW_HEIGHT - 80  # Height of visible area
            if total_height > visible_area:
                scroll_proportion = visible_area / total_height
                self.scroll_offset += delta_y / scroll_proportion

                # Clamp the scroll offset to valid range
                self.scroll_offset = max(0, min(self.scroll_offset, total_height - visible_area))
        else:
            self.mouse_drag_start_y = None  # Reset drag start position if mouse is released

    def create_virtual_keyboard(self):
        keys = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
            "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "Spc", "Del", "Dn"
        ]
        key_width, key_height = 60, 40  # Dimensions of each key
        horizontal_spacing, vertical_spacing = 5, 5  # Adjust spacing between keys
        keys_positions = []

        # Calculate keyboard starting position
        keyboard_x = (WINDOW_WIDTH - ((key_width + horizontal_spacing) * 10)) // 2
        keyboard_y = WINDOW_HEIGHT - 190

        # Iterate over the keys to position them
        for i, key in enumerate(keys):
            x = (i % 10) * (key_width + horizontal_spacing) + keyboard_x
            y = (i // 10) * (key_height + vertical_spacing) + keyboard_y
            keys_positions.append((key, (x, y)))

        return keys_positions


    def draw_virtual_keyboard(self):
        if self.keyboard_triggered:
            # Define the keyboard background
            pygame.draw.rect(screen, KEYBOARD_COLOR, (0, WINDOW_HEIGHT - 200, WINDOW_WIDTH, 200))

            # Draw individual keys
            for key, pos in self.virtual_keyboard:
                key_rect = pygame.Rect(pos, (50, 40))  # Adjust key size
                # Change color when hovering over the key
                color = BUTTON_HOVER_COLOR if key_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
                pygame.draw.rect(screen, color, key_rect, border_radius=5)

                # Render the key label
                key_text = font.render(key, True, KEY_TEXT_COLOR)
                screen.blit(key_text, (key_rect.x + 15, key_rect.y + 10))

                # Handle key presses (trigger only on the first click)
                if key_rect.collidepoint(pygame.mouse.get_pos()) :
                    if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                        if not self.mouse_pressed:  # Trigger only once
                            self.mouse_pressed = True
                            if key == "Dn":
                                self.view_cart_bool = False
                                self.add_to_cart_bool = False
                                self.search_active = False
                                self.keyboard_triggered = False
                                

                            elif key == "Del":
                                self.search_text = self.search_text[:-1]
                                
                            elif key == "Spc":
                                self.search_text += " "
                            else:
                                self.search_text += key
                    else:
                        self.mouse_pressed = False


    def white_pannel(self):
        pygame.draw.rect(screen, (230, 230, 230), (120, 50, 889, 80))


    def filter_by_search_text(self):
    # Check if the search text is empty
        if not self.search_text.strip():
            self.filtered_products = self.products  # Show all products if no search text
        else:
            # Perform a case-insensitive search
            search_query = self.search_text.lower()
            self.filtered_products = [
                product for product in self.products if search_query in product["name"].lower()
            ]


    def filter_by_category(self):
        if self.selected_category == "All Meals":
            self.filtered_products = self.products  # Show all products
        elif self.selected_category == "Rice Meals":
            self.filtered_products = [
                product for product in self.products if "Rice Meal" in product["name"]
            ]
        elif self.selected_category == "Drinks":
            self.filtered_products = [
                product for product in self.products if "Drink" in product["name"] or "Water" in product["name"]
            ]
        elif self.selected_category == "Biscuits":
            self.filtered_products = [
                product for product in self.products if "Biscuit" in product["name"]
            ]

        elif self.selected_category == "Icecream":
            self.filtered_products = [
                product for product in self.products if "Icecream" in product["name"]
            ]




    def create_header(self):

        self.header = self.load_image("assets/banner.png", (WINDOW_WIDTH, 80))

        screen.blit(self.header, (0, 0))


    def create_side_panel(self):
            side_panel_width = 120
            pygame.draw.rect(screen, HEADER_COLOR, (0, 80, side_panel_width, WINDOW_HEIGHT - 80))

            #category_title = font.render("Categories", True, (255, 255, 255))
            #screen.blit(category_title, (10, 100))

            button_y = 120
            for category in self.categories:
                category_button_rect = pygame.Rect(30, button_y, side_panel_width - 60, 60)
                pygame.draw.rect(screen, BUTTON_COLOR, category_button_rect,1, border_radius=5)
                category_button_text = font.render(category, True, TEXT_COLOR)
                screen.blit(category_button_text, (category_button_rect.x -1, category_button_rect.y + 5))

                image = self.load_image(f"assets/{category.lower()}.png", (60, 60 ))
                screen.blit(image, (category_button_rect.x , button_y ))
                if category_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.selected_category = category
                    self.filter_by_category()

                button_y += 80

    def create_search_bar(self):
        search_rect = pygame.Rect(WINDOW_WIDTH - 322, 90, 280, 30)
        pygame.draw.rect(screen, (255, 255, 255), search_rect, border_radius=100)
        search_text_surface = search_font.render(self.search_text, True, TEXT_COLOR)
        screen.blit(search_text_surface, (search_rect.x + 10, search_rect.y + 5))

        search_button_rect = pygame.Rect(WINDOW_WIDTH - 120, 90, 80, 30)
        pygame.draw.rect(screen, (255, 255, 255), search_button_rect,1,border_radius=100)
        search_button_text = font.render("Search", True, TEXT_COLOR)
        screen.blit(search_button_text, (search_button_rect.x + 15, search_button_rect.y + 5))

        # Open the keyboard when the search bar is clicked
        if search_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.search_active = True
            self.keyboard_triggered = True

        # Trigger search when clicking the search button
        if search_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.filter_by_search_text()



    def render_products(self):
        start_x = 200  # Start drawing products after the side panel
        start_y = 140 - self.scroll_offset  # Adjust Y position by the scroll offset
        card_width, card_height = 140, 200
        max_cards_per_row = (WINDOW_WIDTH - start_x - 20 - 20) // (card_width + 20)  # Reserve space for the scroll bar

        for i, product in enumerate(self.filtered_products):
            if i % max_cards_per_row == 0 and i > 0:
                start_x = 200
                start_y += card_height + 20

            product_card_rect = pygame.Rect(start_x, start_y, card_width, card_height)
            pygame.draw.rect(screen, (255, 255, 255), product_card_rect, border_radius=5)

            # Load and render the product image at the top of the card (resize to 120x120)
            product_image = self.load_image(product["image"], (120, 120))  # Resize image
            screen.blit(product_image, (start_x + (card_width - 120) // 2, start_y + 10))  # Center the image

            # Render the product name below the image
            product_name_text = font.render(product["name"], True, TEXT_COLOR)
            screen.blit(product_name_text, (start_x + (card_width - product_name_text.get_width()) // 2, start_y + 130))  # Positioned below the image

            # Render the price below the product name
            product_price_text = font.render(f"Php {product['price']}", True, TEXT_COLOR)
            screen.blit(product_price_text, (start_x + (card_width - product_price_text.get_width()) // 2, start_y + 150))  # Positioned below the name

            # Add to Cart button at the bottom
            add_button_rect = pygame.Rect(start_x + 10, start_y + 170, 120, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, add_button_rect,1, border_radius=5)
            add_button_text = font.render("Add to Cart", True, TEXT_COLOR)
            screen.blit(add_button_text, (add_button_rect.x + 25, add_button_rect.y + 5))

            if not self.keyboard_triggered and add_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.add_to_cart_bool == False:
                self.selected_product = product
                self.selected_quantity = 1
                self.add_to_cart_bool = True

            start_x += card_width + 20




    def draw_product_popup(self):
        popup_width, popup_height = 400, 400
        popup_rect = pygame.Rect(
            (WINDOW_WIDTH - popup_width) // 2,  # Center horizontally
            (WINDOW_HEIGHT - popup_height) // 2,  # Center vertically
            popup_width,
            popup_height,
        )
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=10)

        # Load and draw the product image, enlarged (resize to 200x200)
        product_image = self.load_image(self.selected_product["image"], (200, 200))  # Resize image
        screen.blit(product_image, (popup_rect.x + (popup_width - 200) // 2, popup_rect.y + 20))

        # Draw product name and quantity
        product_name_text = font.render(self.selected_product["name"], True, TEXT_COLOR)
        screen.blit(product_name_text, (popup_rect.x + (popup_width - product_name_text.get_width()) // 2, popup_rect.y + 230))

        quantity_text = font.render(f"Quantity: {self.selected_quantity}", True, TEXT_COLOR)
        screen.blit(quantity_text, (popup_rect.x + (popup_width - quantity_text.get_width()) // 2, popup_rect.y + 260))

        # Buttons for adjusting the quantity and completing the action
        button_width, button_height = 40, 40  # Define button sizes
        button_spacing = 20  # Space between the buttons

        plus_button_rect = pygame.Rect(popup_rect.x + (popup_width - button_width * 3 - button_spacing * 2) // 2, popup_rect.y + popup_height - 80, button_width, button_height)
        minus_button_rect = pygame.Rect(plus_button_rect.x + button_width + button_spacing, popup_rect.y + popup_height - 80, button_width, button_height)
        done_button_rect = pygame.Rect(minus_button_rect.x + button_width + button_spacing, popup_rect.y + popup_height - 80, button_width * 2 + button_spacing, button_height)

        # Draw the buttons
        pygame.draw.rect(screen, BUTTON_COLOR, plus_button_rect,1, border_radius=5)
        pygame.draw.rect(screen, BUTTON_COLOR, minus_button_rect,1, border_radius=5)
        pygame.draw.rect(screen, BUTTON_COLOR, done_button_rect,1, border_radius=5)

        # Render the +, -, and Done text on the buttons
        plus_button_text = font.render("+", True, TEXT_COLOR)
        minus_button_text = font.render("-", True, TEXT_COLOR)
        done_button_text = font.render("Done", True, TEXT_COLOR)
        screen.blit(plus_button_text, (plus_button_rect.x + (button_width - plus_button_text.get_width()) // 2, plus_button_rect.y + (button_height - plus_button_text.get_height()) // 2))
        screen.blit(minus_button_text, (minus_button_rect.x + (button_width - minus_button_text.get_width()) // 2, minus_button_rect.y + (button_height - minus_button_text.get_height()) // 2))
        screen.blit(done_button_text, (done_button_rect.x + (done_button_rect.width - done_button_text.get_width()) // 2, done_button_rect.y + (button_height - done_button_text.get_height()) // 2))

        # Handle button clicks (single press)
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
            if not self.mouse_pressed:  # Trigger only once
                self.mouse_pressed = True

                # Handle Plus button click
                if plus_button_rect.collidepoint(mouse_pos):
                    self.selected_quantity += 1

                # Handle Minus button click
                if minus_button_rect.collidepoint(mouse_pos):
                    self.selected_quantity = max(1, self.selected_quantity - 1)

                # Handle Done button click
                if done_button_rect.collidepoint(mouse_pos):
                    # Add item to cart and close popup
                    self.cart_items.append({
                        "name": self.selected_product["name"],
                        "quantity": self.selected_quantity,
                        "price": self.selected_product["price"] * self.selected_quantity,
                    })
                    self.selected_product = None  # Close the popup
                    self.add_to_cart_bool = False

        # Reset mouse_pressed when the mouse button is released
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_pressed = False

    """
    def view_cart(self):
        cart = pygame.draw.rect(screen, (200,200,255), (30,30,30,30))
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
            if not self.mouse_pressed:  # Trigger only once
                self.mouse_pressed = True

            # Handle Plus button click
            if cart.collidepoint(mouse_pos):
                self.view_cart_bool = True

        if not pygame.mouse.get_pressed()[0]:
            self.mouse_pressed = False
            
        if self.view_cart_bool == True:
            tab = pygame.draw.rect(screen, (255,255,255), (30,30, 500,400))

        """
    

    def render_cart_summary(self):
        
        cart_rect = pygame.Rect(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40)
        pygame.draw.rect(screen, (220, 220, 220), cart_rect)

        total_items = len(self.cart_items)
        total_price = sum(item["price"] * item["quantity"] for item in self.cart_items)

        total_items_text = font.render(f"Total Items: {total_items}", True, TEXT_COLOR)
        total_price_text = font.render(f"Total Price: {total_price}", True, TEXT_COLOR)

        screen.blit(total_items_text, (10, WINDOW_HEIGHT - 40))
        screen.blit(total_price_text, (10 , WINDOW_HEIGHT - 20))

        # Add "View Cart" button
        view_cart_button = pygame.Rect(WINDOW_WIDTH -   330, WINDOW_HEIGHT - 35, 100, 30)
        pygame.draw.rect(screen, BUTTON_COLOR, view_cart_button,1, border_radius=5)
        view_cart_text = font.render("View Cart", True, TEXT_COLOR)
        screen.blit(view_cart_text, (view_cart_button.x + 15, view_cart_button.y + 5))

        checkout_button = pygame.Rect(WINDOW_WIDTH - 200 , WINDOW_HEIGHT - 35, 160, 30)
        pygame.draw.rect(screen, BUTTON_COLOR, checkout_button,1, border_radius=5)
        checkout_text = font.render("Proceed to Checkout", True, TEXT_COLOR)
        screen.blit(checkout_text, (checkout_button.x + 15, checkout_button.y + 5))


        if view_cart_button.collidepoint(pygame.mouse.get_pos()) and self.keyboard_triggered == False:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                if not self.mouse_pressed:  # Trigger only once
                    self.mouse_pressed = True
                    self.view_cart_bool = True

                else:
                    self.mouse_pressed = False


        if checkout_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.keyboard_triggered == False and self.view_cart_bool == False:
            self.view_checkout_bool = True

    def draw_view_cart_popup(self):
        if not self.view_cart_bool:
            return

        popup_width, popup_height = 500, 400
        popup_rect = pygame.Rect(
            (WINDOW_WIDTH - popup_width) // 2,
            (WINDOW_HEIGHT - popup_height) // 2,
            popup_width,
            popup_height,
        )
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=10)

        # Header
        header_text = font.render("Your Cart", True, TEXT_COLOR)
        screen.blit(header_text, (popup_rect.x + 230, popup_rect.y + 10))

        # Render items
        item_start_y = popup_rect.y + 50
        for i, item in enumerate(self.cart_items):
            item_rect = pygame.Rect(popup_rect.x + 20, item_start_y + i * 60, popup_width - 40, 50)
            pygame.draw.rect(screen, (230, 230, 230), item_rect, border_radius=5)

            # Product Name and Price
            item_name = font.render(f"{item['name']} ({item['price']})", True, TEXT_COLOR)
            screen.blit(item_name, (item_rect.x + 20, item_rect.y + 10))

            # Quantity and Buttons
            quantity_text = font.render(f"Qty: {item['quantity']}", True, TEXT_COLOR)
            screen.blit(quantity_text, (item_rect.x + 160, item_rect.y + 10))

            # Add Quantity Button
            add_button = pygame.Rect(item_rect.x + 220, item_rect.y + 10, 30, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, add_button,1, border_radius=5)
            add_text = font.render("+", True, TEXT_COLOR)
            screen.blit(add_text, (add_button.x + 8, add_button.y + 3))

            if add_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                item["quantity"] += 1

            # Subtract Quantity Button
            subtract_button = pygame.Rect(item_rect.x + 260, item_rect.y + 10, 30, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, subtract_button,1, border_radius=5)
            subtract_text = font.render("-", True, TEXT_COLOR)
            screen.blit(subtract_text, (subtract_button.x + 8, subtract_button.y + 3))

            if subtract_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    self.cart_items.pop(i)  # Remove item if quantity is 0

            # Remove Button
            remove_button = pygame.Rect(item_rect.x + 390, item_rect.y + 10, 60, 30)
            pygame.draw.rect(screen, (200, 50, 50), remove_button, border_radius=5)
            remove_text = font.render("Remove", True, (255, 255, 255))
            screen.blit(remove_text, (remove_button.x + 5, remove_button.y + 5))

            if remove_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.cart_items.pop(i)

        # Done Button
        done_button = pygame.Rect(popup_rect.x + (popup_width - 100) // 2, popup_rect.y + popup_height - 50, 100, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, done_button,1, border_radius=5)
        done_text = font.render("Done", True, TEXT_COLOR)
        screen.blit(done_text, (done_button.x + 20, done_button.y + 10))

        if done_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.view_cart_bool = False
            



    def cashin(self):
        pygame.draw.rect(screen, (BACKGROUND_COLOR), (0,0, WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(screen, (10,10,10), (500,50),(500,400))

        
        with open('receipt.json') as file :
            data = json.load(file)

            pay_text = header_font.render(f" Total Items \n\n To pay \n\n Cash \n\n Change ", True, (10,10,10))
            pay_count = header_font.render(f" {data['items']} \n\n {data['total_price']} \n\n  \n\n test ", True, (10,10,10))
            screen.blit(pay_text, (300, 50))
            screen.blit(pay_count, (600, 50))



        
        back_button = pygame.Rect(100,  520, 200, 50)
        proceed_button = pygame.Rect(700,  520, 200, 50)

        pygame.draw.rect(screen, BUTTON_BACK_COLOR, back_button, border_radius=10)
        pygame.draw.rect(screen, BUTTON_PROCEED_COLOR, proceed_button, border_radius=10)

        back_text = font.render("Cancel", True, BUTTON_TEXT_COLOR)
        proceed_text = font.render("Pay", True, BUTTON_TEXT_COLOR)

        screen.blit(back_text, (back_button.x + 80, back_button.y + 15))
        screen.blit(proceed_text, (proceed_button.x + 90, proceed_button.y + 15))
        

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.cashin_bool = False
            """
            if proceed_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.generate_receipt()
                self.cashin_bool = True
                """


    def draw(self):
        screen.fill(BACKGROUND_COLOR)


         
        
        
        self.render_products()
        # Draw the scroll bar
        self.draw_scroll_bar()


        self.white_pannel()
        
        self.create_side_panel()
        self.create_search_bar()
        self.create_header()
        self.render_cart_summary()  # Display cart summary
        pygame.draw.rect(screen, (10,10,10), (0, 560, 119,40),1)



        if self.search_active and self.cashin_bool == False:
            self.draw_virtual_keyboard()

        if self.selected_product and self.view_cart_bool == False and self.keyboard_triggered == False and self.cashin_bool == False:
            self.draw_product_popup()


        if self.view_checkout_bool:
            self.draw_checkout_page()


        self.draw_view_cart_popup()

        if self.cashin_bool == True:
            self.cashin()
        #self.view_cart()
        pygame.display.update()


    def draw_header(self):

        self.header = self.load_image("assets/banner.png", (WINDOW_WIDTH, 80))

        screen.blit(self.header, (0, 0))



    def generate_receipt(self):

        # Generate JSON
        receipt_data = {
            "items": self.cart_items,
            "cash":None,
            "Change":None,
            "total_price": sum(item["price"] * item["quantity"] for item in self.cart_items)
        }
        with open("receipt.json", "w") as jsonfile:
            json.dump(receipt_data, jsonfile, indent=4)




    def draw_checkout_page(self):
        screen.fill(BACKGROUND_COLOR)
        self.draw_header()

        # List of Orders Header
        header_text = font.render("List of Orders", True, TEXT_COLOR)
        screen.blit(header_text, (WINDOW_WIDTH // 2 - header_text.get_width() // 2, 100))

        # Draw order list
        start_y = 150
        total_price = 0

        for item in self.cart_items:
            name_text = font.render(f"{item['name']}", True, TEXT_COLOR)
            quantity_text = font.render(f"{item['quantity']}x", True, TEXT_COLOR)
            price_text = font.render(f"P {item['price'] * item['quantity']}", True, TEXT_COLOR)

            screen.blit(name_text, (100, start_y))
            screen.blit(quantity_text, (400, start_y))
            screen.blit(price_text, (700, start_y))

            start_y += 40
            total_price += item['price'] * item['quantity']

        # Total Price
        pygame.draw.line(screen, LINE_COLOR, (100, start_y), (900, start_y), 1)
        total_price_text = font.render(f"Total Price: P {total_price}", True, TEXT_COLOR)
        screen.blit(total_price_text, (700, start_y + 10))

        # Footer Buttons
        back_button = pygame.Rect(100,  520, 200, 50)
        proceed_button = pygame.Rect(700,  520, 200, 50)

        pygame.draw.rect(screen, BUTTON_BACK_COLOR, back_button, border_radius=10)
        pygame.draw.rect(screen, BUTTON_PROCEED_COLOR, proceed_button, border_radius=10)

        back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
        proceed_text = font.render("Proceed Checkout", True, BUTTON_TEXT_COLOR)

        screen.blit(back_text, (back_button.x + 80, back_button.y + 15))
        screen.blit(proceed_text, (proceed_button.x + 50, proceed_button.y + 15))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.view_checkout_bool = False

        if proceed_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.generate_receipt()
            self.cashin_bool = True


                
# Run the game loop as before
app = SockioApp()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    app.handle_scroll()  # Handle scroll bar interaction
    app.draw()
    pygame.display.update()
    clock.tick(60)
    print(clock)
