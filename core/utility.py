def _convert(iter_obj):
    return [_[0] for _ in iter_obj]


def get_total_coast(database):
    all_product_id = database.select_all_product_id()
    all_price = [database.select_single_product_price(itm)
                 for itm in all_product_id]
    all_quantity = [database.select_order_quantity(itm)
                    for itm in all_product_id]
    return total_coast(all_quantity, all_price)


def get_total_quantity(database):
    all_product_id = database.select_all_product_id()
    all_quantity = [database.select_order_quantity(itm)
                    for itm in all_product_id]
    return total_quantity(all_quantity)


def total_quantity(list_quantity):
    order_total_quantity = 0
    for itm in list_quantity:
        order_total_quantity += itm
    return order_total_quantity


def total_coast(list_quantity, list_price):
    order_total_coast = 0
    for ind, itm in enumerate(list_price):
        order_total_coast += list_quantity[ind]*list_price[ind]
    return order_total_coast


if __name__ == "__main__":
    print(_convert([(5,), (8,)]))

