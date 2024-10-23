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

    item_names = [
        ["披風", "手部", "鞋子", "頭部", "衣服", "腿部"],
        ["一夫當關", "業火", "破陣子", "捻花一笑", "桃之夭夭", "巨靈", "夸父", "滿江紅"],
        ["力拔千鈞", "紅蓮", "桃花扇", "三昧真火", "梨花煙雨", "蚩尤", "塞下", "殺破狼"],
        ["對酒當歌", "赤煉", "美人香", "玉壺冰心", "煙光殘照", "陽關", "離歌", "崩壞"],
    ]
    prevprices = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    price_index = 0
    category_index = 0
    delete_after = 1800
    TIEM_TARGET_PRICE = [
        [40000, 40000, 40000, 40000, 40000, 40000],  # 裝備
        [6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000],  # 一級天書
        [30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000],  # 二級天書
        [50000, 120000, 70000, 40000, 40000, 120000, 40000, 40000],  # 三級天書
    ]
    SCREENCAP_ENABLE = [True, True, True, True]
    FILTER_BUTTON_ENABLE = True
    FIRST_REPORT = True

    def send_message(self, message):
        """Send a message to Discord."""
        dc_messenger.send(message, delete_after=self.delete_after)

    def send_screencap(self):
        """Send a screenshot to Discord."""
        if self.SCREENCAP_ENABLE:
            dc_messenger.send_screencap(
                self.screenshot, (43, 334), (556, 411), delete_after=self.delete_after)

    def update_price(self, price):
        """Update the price history and notify if there's a price change."""
        if price == 0:
            return
        self.prevprices[self.category_index][self.price_index] = price

    def check_price(self, price):
        """Check if the price is within the target range and notify accordingly."""
        if 501 < price < self.TIEM_TARGET_PRICE[self.category_index][self.price_index]:
            if self.prevprices[self.category_index][self.price_index] != price:
                self.send_message(f"目前 {self.item_names[self.category_index][self.price_index]} 裝備的價格為 {price}，已在設定的目標範圍內。")
                if self.SCREENCAP_ENABLE[self.category_index]:
                    self.send_screencap()

    def next_button(self):
        """Move to the next item by updating the price index."""
        self.price_index = self.price_index + 1
        if self.price_index == len(self.POSITION_ITEMS_BUTTON[self.category_index]):
            self.price_index = 0
            self.category_index = self.category_index + 1
            if self.category_index == len(self.POSITION_ITEMS_BUTTON):
                self.category_index = 0
                if self.FIRST_REPORT:
                    self.FIRST_REPORT = False
                    self.send_price_summary()
            

    def send_price_summary(self):
        """Send a summary of all item prices to Discord every hour."""
        price_summary = ", ".join(
            [f"{self.item_names[0][i]}: {self.prevprices[0][i]}" for i in range(len(self.item_names[0]))]
        )
        self.send_message(f"當前裝備擺攤價格更新: {price_summary} ")
        price_summary = ", ".join(
            [f"{self.item_names[1][i]}: {self.prevprices[1][i]}" for i in range(len(self.item_names[1]))]
        )
        self.send_message(f"當前一級天書擺攤價格更新: {price_summary} ")
        price_summary = ", ".join(
            [f"{self.item_names[2][i]}: {self.prevprices[2][i]}" for i in range(len(self.item_names[2]))]
        )
        self.send_message(f"當前二級天書市場擺攤價格更新: {price_summary} ")
        price_summary = ", ".join(
            [f"{self.item_names[3][i]}: {self.prevprices[3][i]}" for i in range(len(self.item_names[3]))]
        )
        self.send_message(f"當前三級天書市場擺攤價格更新: {price_summary} ")

    def run(self):
        """
        Main loop of the PWWBot, executing trading logic based on the detected
        price. The bot transitions through various states and interacts with
        the UI to search for products and update prices.
        """

        # Define positions for buttons and price content area
        self.POSITION_ITEMS_BUTTON = [
            [
                (192, 444), (192, 520), (192, 600),
                (454, 371), (454, 444), (454, 520)
            ],
            [
                (192, 371), (192, 444), (192, 520), (192, 600),
                (454, 371), (454, 444), (454, 520), (454, 600)
            ],
            [
                (192, 371), (192, 444), (192, 520), (192, 600),
                (454, 371), (454, 444), (454, 520), (454, 600)
            ],
            [
                (192, 371), (192, 444), (192, 520), (192, 600),
                (454, 371), (454, 444), (454, 520), (454, 600)
            ]
        ]
        self.POSITION_CATEGORY = [(74, 208), (528, 208), (528, 208), (528, 208)]
        self.POSITION_FILTER_BUTTON = (80, 306)
        self.POSITION_FILTER_CONFIRM_BUTTON = (284, 562)
        self.POSITION_BACK_BUTTON = [(224, 257), (224, 257), (343, 256), (461, 256)]
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
                self.send_message(f"正在啟動 PWW Bot...")

                # Transition to SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                # Simulate interactions: back button, select item, apply filters
                if self.price_index == 0:
                    self.click(self.POSITION_CATEGORY[self.category_index])
                self.wait(1)
                self.click(self.POSITION_BACK_BUTTON[self.category_index])
                self.wait(1)
                self.click(self.POSITION_ITEMS_BUTTON[self.category_index][self.price_index])
                self.wait(1)
                if self.category_index == 0 and self.FILTER_BUTTON_ENABLE:
                    self.click(self.POSITION_FILTER_BUTTON)
                    self.wait(1)
                    self.click(self.POSITION_FILTER_CONFIRM_BUTTON)
                    self.wait(1)

                # Wait for price update
                self.wait(1)

                # Extract the price from the screen
                price = self.extract_integer_from_area(self.AREA_PRICE_CONTENT)

                # Check price range and update if necessary
                self.check_price(price)
                self.update_price(price)

                # Move to the next item
                self.next_button()

        # Stop Discord messenger when the bot stops
        dc_messenger.stop()
