from typing import List, Tuple
from enum import Enum
from bisect import insort


class Side(Enum):
    BUY = "buy"
    SELL = "sell"


class Order:
    def __init__(self, side: Side, price: float, quantity: int):
        self.side = side
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Order(side={self.side}, price={self.price}, quantity={self.quantity})"


class OrderBook:
    def __init__(self):
        # Define lists for buy and sell orders
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order: Order):
        if order.side == Side.BUY:
            # Use insort to append to buy orders
            insort(self.buy_orders, order, key=lambda x: -x.price) # Keep buy orders in descending manner
        else:
            insort(self.sell_orders, order, key=lambda x: x.price) # Keep sell orders in ascending manner

    def match_orders(self) -> List[Tuple[Order, Order, int]]:
        # Define a list for matches
        matches = []
        # While there are buy orders and sell orders in the order book
        while self.buy_orders and self.sell_orders:
            # Define the best buy and sell orders as the first item in each list as they are already sorted
            best_buy_order = self.buy_orders[0]
            best_sell_order = self.sell_orders[0]

            # Break if there is no match
            if best_buy_order.price < best_sell_order.price:
                break

            # Match quantity by taking the least quantity between the best buy order and best sell order
            match_quantity = min(best_buy_order.quantity, best_sell_order.quantity)
            matches.append((best_buy_order, best_sell_order, match_quantity))

            # Update the best buy order and best sell order quantities
            best_buy_order.quantity -= match_quantity
            best_sell_order.quantity -= match_quantity

            # Remove filled buy and sell orders
            if best_buy_order.quantity == 0:
                self.buy_orders.pop(0)
            if best_sell_order.quantity == 0:
                self.sell_orders.pop(0)

        return matches

    def show(self):
        print("Buy Orders:")
        for order in self.buy_orders:
            print(f"Price: {order.price}, Quantity: {order.quantity}")

        print("\nSell Orders:")
        for order in self.sell_orders:
            print(f"Price: {order.price}, Quantity: {order.quantity}")


if __name__ == "__main__":
    order_book = OrderBook()

    # Example orders
    orders = [
        Order(Side.BUY, 1000, 2),
        Order(Side.BUY, 2000, 2),
        Order(Side.SELL, 2000, 1),
        Order(Side.SELL, 2100, 4),
    ]

    for order in orders:
        order_book.add_order(order)

    order_book.show()

    matches = order_book.match_orders()

    print("\nMatches:")
    for buy_order, sell_order, quantity in matches:
        print(f"Buy order matched with sell order, quantity: {quantity}")

    print("\nUpdated Order Book:")
    order_book.show()
