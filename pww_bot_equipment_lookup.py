from bot import BotState, Bot

class Bot(Bot):
    """
    A bot class for automating trading actions based on price detection
    within a specified range.

    Inherits from the Bot class and overrides the run method to implement 
    trading logic based on detected prices on the screen.
    """

    def run(self):
        """
        The main loop of the PWWBot, executing its trading logic based on the
        detected price of a product. The bot transitions through various states,
        including INITIALIZING, SEARCHING, TRADING, and BACKTRACKING.

        The bot performs the following actions:
        - Searches for a product within a specified price range.
        - Executes a trade when the price falls within the defined limits.
        - Backtracks to the searching state after completing a trade.
        """
        TARGET_ITEM_CONTENT = [["+56.86", 2], ["+20%", 2]]  # Target item content for trading

        # Define positions for buttons and price content area
        POSITION_ITEMS_BUTTON = [(68, 387), (68, 468), (68, 544), (68, 622), (326, 387), (326, 468), (326, 544), (326, 622)]
        POSITION_CLOSE_BUTTON = (459, 811)
        POSITION_NEXT_PAGE_BUTTON = (357, 723)
        AREA_ITEM_CONTENT = [(29, 634), (319, 927)]

        i = 0
        while not self.stopped:
            # Wait for a short period if not in the TRADING state
            if self.state is not BotState.TRADING:
                self.wait(1)

            if self.state == BotState.INITIALIZING:
                
                print(f"Starting PWWBot with target item content settings: content = {TARGET_ITEM_CONTENT}")
                
                # Transition to the SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                print("Transitioning to SEARCHING state...")
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                # Click the filter and confirm buttons to search for products
                print("Searching for products...")
                if i == len(POSITION_ITEMS_BUTTON):
                    i = 0
                    self.click(POSITION_NEXT_PAGE_BUTTON)

                self.click(POSITION_ITEMS_BUTTON[i])
                i += 1
                
                self.wait(0.5)  # Wait briefly for the price to update

                content = self.extract_text_from_area(AREA_ITEM_CONTENT)
                for item in TARGET_ITEM_CONTENT:
                    if content.count(item[0]) > item[1]:
                        print(f"Item {content} is within the target range. Transitioning to TRADING state...")
                        self.lock.acquire()
                        self.state = BotState.TRADING
                        self.lock.release()
                        continue

                self.click(POSITION_CLOSE_BUTTON)
                print(f"Item {content} is outside the target range. Continuing search...")                

            elif self.state == BotState.TRADING:
                # Perform trading actions
                print(f'Detected product meets the target content. Starting trading...')
                self.wait(5)
                print(f'Transaction completed successfully.')

                self.lock.acquire()
                self.state = BotState.BACKTRACKING  # Transition to BACKTRACKING state
                print("Transitioning to BACKTRACKING state...")
                self.lock.release()

            elif self.state == BotState.BACKTRACKING:
                # Click to select the product again and prepare for searching
                print("Backtracking to prepare for the next search...")
                self.click(POSITION_CLOSE_BUTTON)

                self.lock.acquire()
                self.state = BotState.SEARCHING  # Transition back to SEARCHING state
                print("Transitioning back to SEARCHING state...")
                self.lock.release()

# 擺攤天書
class PWWBot2(Bot):
    """
    A bot class for automating trading actions based on price detection
    within a specified range.

    Inherits from the Bot class and overrides the run method to implement 
    trading logic based on detected prices on the screen.
    """

    def run(self):
        """
        The main loop of the PWWBot, executing its trading logic based on the
        detected price of a product. The bot transitions through various states,
        including INITIALIZING, SEARCHING, TRADING, and BACKTRACKING.

        The bot performs the following actions:
        - Searches for a product within a specified price range.
        - Executes a trade when the price falls within the defined limits.
        - Backtracks to the searching state after completing a trade.
        """
        TARGET_MIN_PRICE = 25000  # Minimum target price for trading
        TARGET_MAX_PRICE = 65000  # Maximum target price for trading

        POSITION_CLOSE_BUTTON = (501, 190) # (-1798, 22)
        POSITION_VIEW_BUTTON = (281, 792) # (-1798, 202)
        POSITION_BUY_BUTTON = (281, 850) # (-1798, 202)
        AREA_PRICE_CONTENT = [(274, 653), (396, 684)]
        POSITION_SELECT_1_BUTTON = (161, 389) # (-1798, 202)
        while not self.stopped:
            # Wait for a short period if not in the TRADING state
            if self.state is not BotState.TRADING:
                self.wait(1)

            if self.state == BotState.INITIALIZING:

                self.click(POSITION_SELECT_1_BUTTON)

                # Transition to the SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                print("Transitioning to SEARCHING state...")
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                
                # Click the filter and confirm buttons to search for products
                print("Searching for products...")
                self.click(POSITION_VIEW_BUTTON)
                
                self.wait(0.5)  # Wait briefly for the price to update

                # Get the detected price from the specified area
                price = self.extract_integer_from_area(AREA_PRICE_CONTENT)

                # Check if the detected price is within the target range
                if TARGET_MIN_PRICE < price < TARGET_MAX_PRICE:
                    print(f"Price {price} is within the target range. Transitioning to TRADING state...")
                    self.lock.acquire()
                    self.state = BotState.TRADING  # Transition to TRADING state
                    self.lock.release()
                else:
                    print(f"Price {price} is outside the target range. Continuing search...")
                    self.click(POSITION_CLOSE_BUTTON)

            elif self.state == BotState.TRADING:

                # Perform trading actions
                print(f'Detected product meets the target price. Starting trading...')
                self.click(POSITION_BUY_BUTTON)
                print(f'Transaction completed successfully.')

                self.lock.acquire()
                self.state = BotState.BACKTRACKING  # Transition to BACKTRACKING state
                print("Transitioning to BACKTRACKING state...")
                self.lock.release()

            elif self.state == BotState.BACKTRACKING:

                # Click to select the product again and prepare for searching
                print("Backtracking to prepare for the next search...")
                self.click(POSITION_SELECT_1_BUTTON)

                self.lock.acquire()
                self.state = BotState.SEARCHING  # Transition back to SEARCHING state
                print("Transitioning back to SEARCHING state...")
                self.lock.release()