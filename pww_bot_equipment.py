from bot import BotState, Bot
from discord_messenger import DiscordMessenger
import time

# Initialize Discord messenger with the token and channel ID
dc_messenger = DiscordMessenger(token='', channel_id='')
dc_messenger.start()

class Bot(Bot):
    """
    A bot class for automating trading actions based on price detection within
    a specified range. Inherits from the Bot class and overrides the run method
    to implement trading logic based on detected prices on the screen.
    """

    item_names = ["披風", "手部", "鞋子", "頭部", "衣服", "腿部"]
    prevprices = [0, 0, 0, 0, 0, 0]
    price_index = 0
    delete_after = 3600

    TARGET_MIN_PRICE = 1000
    TARGET_MAX_PRICE = 5000
    SCREENCAP_ENABLE = False
    FILTER_BUTTON_ENABLE = True

    def send_message(self, message):
        """Send a message to Discord."""
        dc_messenger.send(message, delete_after=self.delete_after)

    def send_screencap(self):
        """Send a screenshot to Discord."""
        if self.SCREENCAP_ENABLE:
            dc_messenger.send_screencap(self.screenshot, (43, 334), (556, 411), delete_after=self.delete_after)

    def update_price(self, price):
        """Update the price history and notify if there's a price change."""
        if price == 0:
            return
        self.prevprices[self.price_index] = price

    def check_price(self, price):
        """Check if the price is within the target range and notify accordingly."""
        if self.TARGET_MIN_PRICE < price < self.TARGET_MAX_PRICE:
            if self.prevprices[self.price_index] != price:
                self.send_message(f"目前 {self.item_names[self.price_index]} 裝備的價格為 {price}，已在設定的目標範圍內。")
                self.send_screencap()

    def next_button(self):
        """Move to the next item by updating the price index."""
        self.price_index = (self.price_index + 1) % len(self.POSITION_ITEMS_BUTTON)

    def send_price_summary(self):
        """Send a summary of all item prices to Discord every hour."""
        price_summary = ", ".join(
            [f"{self.item_names[i]}: {self.prevprices[i]}" for i in range(len(self.item_names))]
        )
        self.send_message(f"當前市場擺攤價格更新: {price_summary} ")

    def run(self):
        """
        Main loop of the PWWBot, executing trading logic based on the detected
        price. The bot transitions through various states and interacts with
        the UI to search for products and update prices.
        """

        # Define positions for buttons and price content area
        self.POSITION_ITEMS_BUTTON = [
            (192, 444), (192, 520), (192, 600),
            (454, 371), (454, 444), (454, 520)
        ]
        self.POSITION_FILTER_BUTTON = (80, 306)
        self.POSITION_FILTER_CONFIRM_BUTTON = (284, 562)
        self.POSITION_BACK_BUTTON = (224, 257)
        self.AREA_PRICE_CONTENT = [(164, 378), (268, 403)]
        self.last_summary_time = time.time()

        while not self.stopped:
            self.wait(1)

            # Check if an hour has passed to send the price summary
            current_time = time.time()
            if current_time - self.last_summary_time >= 10800:  # 10800 seconds = 3 hour
                self.send_price_summary()
                self.last_summary_time = current_time  # Reset the last summary time

            if self.state == BotState.INITIALIZING:
                # Notify Discord of bot initialization and target price settings
                self.send_message(f"正在啟動 PWW Bot ，目標價格設定為 最低價格: {self.TARGET_MIN_PRICE}，最高價格: {self.TARGET_MAX_PRICE}。")

                # Transition to SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                # Simulate interactions: back button, select item, apply filters
                self.click(self.POSITION_BACK_BUTTON)
                self.wait(1)
                self.click(self.POSITION_ITEMS_BUTTON[self.price_index])
                self.wait(1)
                if self.FILTER_BUTTON_ENABLE:
                    self.click(self.POSITION_FILTER_BUTTON)
                    self.wait(1)
                    self.click(self.POSITION_FILTER_CONFIRM_BUTTON)
                    self.wait(1)
                
                # Wait for price update
                self.wait(0.5)

                # Extract the price from the screen
                price = self.extract_integer_from_area(self.AREA_PRICE_CONTENT)

                # Check price range and update if necessary
                self.check_price(price)
                self.update_price(price)

                # Move to the next item
                self.next_button()

        # Stop Discord messenger when the bot stops
        dc_messenger.stop()