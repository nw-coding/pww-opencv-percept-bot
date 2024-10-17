from bot import BotState, Bot
from discord_messenger import DiscordMessenger

# Initialize Discord messenger with the token and channel ID
dc_messenger = DiscordMessenger(token='', channel_id='')
dc_messenger.start()

class Bot(Bot):
    """
    A bot class for automating trading actions based on price detection within
    a specified range. Inherits from the Bot class and overrides the run method
    to implement trading logic based on detected prices on the screen.
    """

    found = True
    prevprice = 0

    TARGET_MIN_PRICE = 40000
    TARGET_MAX_PRICE = 140000

    def send_message(self, message):
        """Send a message to Discord."""
        dc_messenger.send(message)

    def send_screencap(self):
        """Send a screenshot to Discord."""
        dc_messenger.send_screencap(self.screenshot, (43, 150), (556, 919))

    def update_price(self, price):
        """Update the price history and notify if there's a price change."""
        if price == 0:
            return
        if self.prevprice != 0 and self.prevprice != price:
            self.send_message(f"The market price has changed from {self.prevprice} to {price}.")
        self.prevprice = price
    
    def check_price(self, price):
        """Check if the price is within the target range and notify accordingly."""
        if self.TARGET_MIN_PRICE < price < self.TARGET_MAX_PRICE:
            if not self.found or self.prevprice != price:
                self.send_screencap()
                self.send_message(f"Price {price} is within the target range.")
                self.found = True
        else:
            if self.found:
                self.send_message(f"Price {price} is outside the target range. Continuing search...")
                self.found = False

    def run(self):
        """
        Main loop of the PWWBot, executing trading logic based on the detected
        price. The bot transitions through various states and interacts with
        the UI to search for products and update prices.
        """

        # Define positions for buttons and price content area
        POSITION_CLOSE_BUTTON = (526, 185)
        POSITION_VIEW_BUTTON = (301, 792)
        AREA_PRICE_CONTENT = [(297, 630), (406, 653)]
        POSITION_SELECT_1_BUTTON = (181, 389)

        while not self.stopped:
            self.wait(1.5)  # Pause briefly between actions unless in TRADING state

            if self.state == BotState.INITIALIZING:
                # Notify Discord of the bot's initialization and starting price range
                self.send_message(f"Starting PWWBot with target price settings: Min Price = {self.TARGET_MIN_PRICE}, Max Price = {self.TARGET_MAX_PRICE}")
                self.send_screencap()
                
                # Perform initial click to start product selection
                self.click(POSITION_SELECT_1_BUTTON)

                # Transition to SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                # Perform a product search by interacting with the interface
                self.click(POSITION_VIEW_BUTTON)
                self.wait(1.5)  # Wait briefly for price update

                # Extract the price from the defined screen area
                price = self.extract_integer_from_area(AREA_PRICE_CONTENT)
                
                # Check price range and update if necessary
                self.check_price(price)
                self.update_price(price)
                
                self.click(POSITION_CLOSE_BUTTON)

        # Stop the Discord messenger when the bot is stopped
        dc_messenger.stop()
