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
        TARGET_MIN_PRICE = 5000  # Minimum target price for trading
        TARGET_MAX_PRICE = 12000  # Maximum target price for trading

        # Define positions for buttons and price content area
        POSITION_FILTER_BUTTON = (51, 316)
        POSITION_FILTER_CONFIRM_BUTTON = (284, 583)
        AREA_PRICE_CONTENT = [(139, 393), (273, 421)]
        POSITION_BUY_BUTTON = (281, 813)
        POSITION_BUY_CONFIRM_BUTTON = (285, 663)
        POSITION_BUY_CONFIRM_2_BUTTON = (396, 612)
        POSITION_SELECT_1_BUTTON = (161, 389)

        while not self.stopped:
            # Wait for a short period if not in the TRADING state
            if self.state is not BotState.TRADING:
                self.wait(1)

            if self.state == BotState.INITIALIZING:
                
                print(f"Starting PWWBot with target price settings: Min Price = {TARGET_MIN_PRICE}, Max Price = {TARGET_MAX_PRICE}")
                
                # Transition to the SEARCHING state
                self.lock.acquire()
                self.state = BotState.SEARCHING
                print("Transitioning to SEARCHING state...")
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                # Click the filter and confirm buttons to search for products
                print("Searching for products...")
                self.click(POSITION_FILTER_BUTTON)
                self.click(POSITION_FILTER_CONFIRM_BUTTON)
                
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

            elif self.state == BotState.TRADING:
                # Perform trading actions
                print(f'Detected product meets the target price. Starting trading...')
                self.click(POSITION_SELECT_1_BUTTON)
                self.click(POSITION_BUY_BUTTON)
                self.click(POSITION_BUY_CONFIRM_BUTTON)
                self.click(POSITION_BUY_CONFIRM_2_BUTTON)
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