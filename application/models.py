from .database import db
from flask_login import UserMixin


class Developer(db.Model,UserMixin):
    __tablename__='developer'
    developer_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    APIkey=db.Column(db.String,unique=True, nullable=True)
    def get_id(self):
        return str(self.developer_id)

class User(db.Model,UserMixin):
    __abstract__=True
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String(10),nullable=False)

class Customer(User):
    __tablename__='customer'
    customer_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    address=db.Column(db.String,nullable=False)
    def get_id(self):
        return str(self.customer_id)

class StoreManager(User):
    __tablename__='store_manager'
    store_manager_id=db.Column(db.Integer,primary_key=True)
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    def get_id(self):
        return str(self.store_manager_id)

class DeliveryExecutive(User):
    __tablename__='delivery_executive'
    delivery_executive_id=db.Column(db.Integer,primary_key=True)
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    def get_id(self):
        return str(self.delivery_executive_id)



#next three classes can only be read or written by the admin(app developer or db manager)
class StoreManagerids(db.Model):
    __tablename__='store_manager_ids'
    store_manager_id=db.Column(db.Integer,primary_key=True) 
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)

class DeliveryExecutiveids(db.Model):
    __tablename__='delivery_executive_ids'
    delivery_executive_id=db.Column(db.Integer,primary_key=True)
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)

class Branch(db.Model):
    __tablename__='branch'
    branch_id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String,nullable=False)



class Category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String,nullable=False, unique=True)
    description=db.Column(db.String)
    
class Products(db.Model):
    __tablename__='products'
    product_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    price=db.Column(db.Float,nullable=False) #price of minimum quantity
    quantity=db.Column(db.Integer,nullable=False) #quantity available in store
    unit=db.Column(db.String,nullable=False) #kg, liters, packet etc
    pricePerUnit=db.Column(db.Float,nullable=False) #price of 1 kg, litre etc.
    category_id=db.Column(db.Integer, db.ForeignKey("category.category_id")) #one product can be in one category only
    manufacture_date=db.Column(db.String)
    expiry_date=db.Column(db.String)
    image_url=db.Column(db.String,nullable=False)
    avg_rating=db.Column(db.Float) 
    isDeleted=db.Column(db.String,default='False') 

class Reviews(db.Model):
    __tablename__='reviews'
    review_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"),nullable=False)
    stars=db.Column(db.Integer)
    review_text=db.Column(db.String)
    date=db.Column(db.String,nullable=False)
    isPurchased=db.Column(db.String,nullable=False)

    @property
    def customer_name(self):
        customer = Customer.query.filter_by(customer_id=self.customer_id).first()
        if customer:
            return customer.name
        return None

#once the order is placed, the items in cart are moved to this table, and cart is emptied, and product quantity is reduced in products table
class Cart(db.Model):
    __tablename__='cart'
    sno=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"))
    quantity=db.Column(db.Integer) #quantity of product in cart

class OrderDetails(db.Model):
    __tablename__='order_details'
    order_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    delivery_executive_id=db.Column(db.Integer, db.ForeignKey("delivery_executive.delivery_executive_id"),nullable=False)
    modeOfPayment=db.Column(db.String,nullable=False)
    delivery_status=db.Column(db.String)
    order_date=db.Column(db.String,nullable=False)
    total_price=db.Column(db.Float,nullable=False)

class OrdersItems(db.Model):
    __tablename__='orders_items'
    sno=db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"),nullable=False)
    price=db.Column(db.String,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)

class onlinePayments(db.Model):
    __tablename__='online_payments'
    payment_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"))
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    payment_status=db.Column(db.String,nullable=False)
    payment_date=db.Column(db.String,nullable=False)
    payment_amount=db.Column(db.Float,nullable=False)
    payment_intent_id=db.Column(db.String,nullable=False,unique=True)

db.create_all()



# Initializing 1 store branch, 1 store manager and 3 delivery executives

if (
    db.session.query(Branch).count() == 0 and
    db.session.query(StoreManagerids).count() == 0 and
    db.session.query(DeliveryExecutiveids).count() == 0
):
    # Create and add the branch
    branch = Branch(branch_id=1,location='New Delhi', phone_no='1800180045')
    db.session.add(branch)

    # Create and add the store manager
    store_manager = StoreManagerids(branch_id=1,store_manager_id=1)
    db.session.add(store_manager)

    # Create and add the delivery executives
    for _ in range(1,4):
        delivery_executive = DeliveryExecutiveids(delivery_executive_id=_,branch_id=1)
        db.session.add(delivery_executive)

    # Adding category 0
    category = Category(category_id=0,name='Others',description='Products not in any category')
    db.session.add(category)
    
    db.session.commit()
    print("Database initialized successfully.")
else:
    print("Database already contains data. Skipping initialization.")
