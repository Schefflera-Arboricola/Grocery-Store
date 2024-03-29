# Description

## Database : 

![db](/static/img/db.jpg)

Run the code in `database.dbd` [here](https://dbdiagram.io/) to get the updated diagram

<br>

## Data flow :

1. <b>Initialisation</b> : Database is initialized with one branch in `Branch` table and one Store Manager in `StoreManagerIds` and three Delivery Executives in `DeliveryExecutiveIds`. These IDs are required while signing up as store manager and delivery executive. These are provided by the store to them. Category 0 is created for products that are in none of the categories. Store manger cannot delete or edit this category. When a category is deleted, all the products in that category are moved to category 0. The `alembic_version` table was created while modifying the db structure.

2. <b>Placing Orders</b> :

- `Cart` table has all the items currently in the carts of all the customers.
- `OrdersItems` has all the items ordered by all the customers.
- Once the order is placed a new entry is created in the `OrderDetails` table, and the items
in the `Cart` table(for that customer) are transferred to the `OrdersItems` table and the quantities in the `Products` table are also decreased accordingly.
- If payment fails, the order is automatically placed with Cash-on-delivery as the `modeOfPayment`.