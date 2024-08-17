# CT_Mini_Project_Library_Management_System

Library Management System Mini Project for Coding Temple Software Engineering Course
====

Table of Contents:
----

### 1. Installing and Running the Application
	a.Required programs and libraries
	b.Installation
	c.Running the application
### 2. How to set-up the E-commerce API
	a. Setting up the database connection
	b. Using the Postman Collection
### 3. Customer Endpoints
	a. Add a new customer
	b. Update a customer
	c. Retrieve all customers
	d. Retrieve a customer by id
	e. Delete a customer
### 4. Customer Account Endpoints
	a. Add a new customer account
	b. Update a customer account
	c. Retrieve all customer accounts
	d. Retrieve a customer account by id
	e. Delete a customer account
### 5. Product Endpoints
	a. Add a new product
	b. Update a product
	c. Retrieve all products
	d. Retrieve a product by id
	e. Delete a product
	f. Check Product Stock Levels
### 6. Order Endpoints
	a. Add a new order
	b. Update a order
	c. Retrieve all orders
	d. Retrieve an order by id
	e. Track order by id
	f. Retrieve a customer's order history
	g. Delete an order
  

### 1. Installing and Running the Application:
####  a. Required programs and libraries
This API was written with MySQL 8.0 and higher as the basis. An SQLAlchemy compatible database server is required for the function of this API, but may require some modification to work properly with the chosen database server.
Please ensure to have on installed before attempting to run the API app.

Libraries required:
* Flask 3.0.3
* Flask-Marshmallow 1.2.1
* Flask-SQLAlchemy 3.1.1
* Marshmallow-SQLAlchemy 1.0.0

#### b. Installation: Clone or download the repository to a directory.
#### c. Running the Application
##### Running the Application on Windows:
python .\Library_Management_System.py (if Python is setup in your system's PATH)
[installation Directory]\python.exe .\Library_Management_System.py (no system PATH set)
##### Running the Application on POSIX Operating Systems(Linux/Unix/BSD/MacOS):
python ./Contact_Management_System.py (if proper environment variables setup)
python3 ./Contact_Management_System.py (some systems may require python3 command instead of python command)

[install path]/python ./Contact_Management_System.py (no environment variable set)
[install path]/python3 ./Contact_Management_System.py (alternative for some systems with no environment variable set)

### 2.  How to setup the E-commerce API

#### a. Setting up the database connection
Please use the included 'Create database.db' or run the command on your server:
`CREATE DATABASE e_commerce_db;`

There are two main ways to set up the database for a connection:
*  create a file named db_user.py and add the following code replacing the password and user name with the appropriate values for your setup:
```Python
db_password  =  "user password"
db_user  =  'username'
```
* remove the line:
```Python
```  from  db_login  import  db_password, db_user
```
from Main.py and then replace the `{db_user}` and `{db_password} fields in the line:
```Python
app.config['SQLALCHEMY_DATABASE_URI'] =  f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/e_commerce_db'
```
with the appropriate values for your setup
#### b. Using the Postman Collection
A collection of pre setup endpoints with related templates for using the API is provided in JSON format to be imported into the Postman application and will be referenced to in following documentation for ease of use and testing of the API.
### 3. Customer Endpoints
#### a. Add a new customer
The endpoint is '<your_domain>/customers'
Filling in the empty quotes in postman, using the Add New Customer method,  or completing and passing the provided JSON with in a POST request will add a new customer with the input information passed in the JSON data:
```JSON
{
	"name" : "customer name",
	"email" : "customer email",
	"phone" : "customer phone"
}
```
Success message:
```JSON
{
	"message": "Customer added successfully"
}
```
#### b. Update a customer
The endpoint is '<your_domain>/customers/<customer_id>'
Filling in the empty quotes in postman, using the Update Customer method and making sure to fill out all fields to ensure data isn't lost,  or completing and passing the provided JSON in a PUT request will update the customer with the customer id passed through the URI with the input information passed in the JSON data:
```JSON
{
	"name" : "customer name",
	"email" : "customer email",
	"phone" : "customer phone"
}
```
Success Message:
```JSON
{
	"message": "Customer details updated successfully"
}
```
!!Please make sure that data that doesn't change is input exactly as it was previously!!
#### c. Retrieve all customers
The endpoint is '<your_domain>/customers'
Sending a GET request to this endpoint will return the customer data for all customers in the database in JSON format. 
Example of return data:
```JSON
[
	{
	"name" : "customer_1",
	"email" : "customer1@email.com",
	"phone" : "1234567890"
	},
	{
	"name" : "customer_2",
	"email" : "customer2@email.com",
	"phone" : "0987654321"
	}
]
```
#### d. Retrieve a customer by id
The endpoint is '<your_domain>/customers/<customer_id>'
Sending a GET request to this endpoint will return the customer data for all customers in the database in JSON format. 
Example of return data:
```JSON
{
	"name" : "customer",
	"id" : 2,
	"email" : "customer2@email.com",
	"phone" : "0987654321"
}
```
#### e. Delete a customer
The endpoint is '<your_domain>/customers/<customer_id>'
sending a DELETE request to this end point will delete the customer with the customer_id passed from the URI from the Customer table in the database:
Success Message:
```JSON
{
	"message": "Customer deleted successfully"
}
```
### 4. Customer Account Endpoints
#### a. Add a new customer account
The endpoint is '<your_domain>/customeraccounts'
Filling in the empty quotes in postman, using the Add New Customer Account method,  or completing and passing the provided JSON with in a POST request will add a new customer with the input information passed in the JSON data with data following the following rules:
* Passwords must contain atleast 8 character, 1 uppercase letter, 1 lowercase letter, 1 numerical digit, and 1 special character
* Username must be unique
```JSON
{
	"username" : "unique username",
	"password" : "valid_password",
	"customer_id" : customer_id
}
```
Success Message:
```JSON
{
	"message": "Customer Account added successfully"
}
```
#### b. Update a customer account
The endpoint is '<your_domain>/customeraccounts/<customer_account_id>'
Filling in the empty quotes in postman, using the Update Customer method and making sure to fill out all fields to ensure data isn't lost,  or completing and passing the provided JSON in a PUT request will update the customer with the customer id passed through the URI with the input information passed in the JSON data:
```JSON
{
	"username" : "unique username",
	"password" : "valid_password",
	"customer_id" : customer_id
}
```
Success Message:
```JSON
{
	"message": "Customer Account updated successfully"
}
```
#### c. Retrieve all customer accounts
The endpoint is '<your_domain>/customeraccounts'
Sending a GET request to this endpoint will return the customer account data including the data of the linked customer for all customer accounts in the database in JSON format. 
Example of return data:
```JSON
[
	{
		"customer" : {
			"email" : "john.doe@example.com",
			"id" : 1,
			"name" : "John Doe",
			"phone" : "1234567890"
		},
		"customer_id" : 1,
		"id" : 1,
		"password" : "6YHN$rfv",
		"username" : "jdoe1971"
	},
	{
		"customer" : {
			"email" : "jane.doe@example.com",
			"id" : 2,
			"name" : "Jaane Doe",
			"phone" : "0987654321"
		},
		"customer_id" : 2,
		"id" : 2,
		"password" : "8UHB^yhn",
		"username" : "jdoe1975"
	}
]
```
#### d. Retrieve a customer account by id
The endpoint is '<your_domain>/customeraccounts/<customer_account_id>'
Sending a GET request to this endpoint will return the customer account data for the customer account with the customer_account_id passed through the URI in the database in, JSON format. 
Example of return data:
```JSON
{
	"customer" : {
		"email" : "jane.doe@example.com",
		"id" : 2,
		"name" : "Jaane Doe",
		"phone" : "0987654321"
	},
	"customer_id" : 2,
	"id" : 2,
	"password" : "8UHB^yhn",
	"username" : "jdoe1975"
}
```
#### e. Delete a customer account
The endpoint is 'your_domain/customeraccounts/<customer_id>'
sending a DELETE request to this end point will delete the customer with the customer_id passed from the URI from the Customer table in the database:
Success Message:
```JSON
{
	"message": "Customer Account deleted successfully"
}
```
### 5. Product Endpoints
#### a. Add a new product
The endpoint is '<your_domain>/products'
Filling in the empty quotes in postman, using the Add New Customer Account method,  or completing and passing the provided JSON with in a POST request will add a new customer with the input information passed in the JSON data with data following the following rules:
* Passwords must contain atleast 8 character, 1 uppercase letter, 1 lowercase letter, 1 numerical digit, and 1 special character
* Username must be unique
```JSON
{
	"product_name" : "name_of_product",
	"price" : product_price,
	"stock_quantity" : quantity_of_product_in_stock
}
```
Success Message:
```JSON
{
	"message": "Product added successfully"
}
```
#### b. Update a product
The endpoint is '<your_domain>/products/<product_id>'
Filling in the empty quotes in postman, using the Update Product method and making sure to fill out all fields to ensure data isn't lost,  or completing and passing the provided JSON in a PUT request will update the product with the product id passed through the URI with the input information passed in the JSON data:
```JSON
{
	"product_name" : "name_of_product",
	"price" : product_price,
	"stock_quantity" : quantity_of_product_in_stock
}
```
Success Message:
```JSON
{
	"message": "Product updated successfully"
}
```
#### c. Retrieve all products
The endpoint is '<your_domain>/products'
Sending a GET request to this endpoint will return the product data for the product with the product id passed through the URI  in JSON format. 
Example of return data:
```JSON
[
	{
		"id" : 1
		"product_name" : "Sneakers",
		"price" : 49.99,
		"stock_quantity" : 6
	},
	{
		"id" : 2
		"product_name" : "Leather Jacket",
		"price" : 499.99,
		"stock_quantity" : 3
	}
]
```
#### d. Retrieve a product by id
The endpoint is '<your_domain>/products/<product_id>'
Sending a GET request to this endpoint will return the product data for all products in the database in JSON format. 
Example of return data:
```JSON
[
	{
		"id" : 1
		"product_name" : "Sneakers",
		"price" : 49.99,
		"stock_quantity" : 6
	},
	{
		"id" : 2
		"product_name" : "Leather Jacket",
		"price" : 499.99,
		"stock_quantity" : 3
	}
]
```
#### e. Delete a product
The endpoint is 'your_domain/products/<product_id>'
sending a DELETE request to this end point will delete the product with the product_id passed from the URI from the Product table in the database:
Success Message:
```JSON
{
	"message": "Product deleted successfully"
}
```
#### f. Check Product Stock Levels
The endpoint is '<your_domain>/products/checkstock'
Sending a GET request to this endpoint will return the product stock data for all the products in the database in JSON format. 
Example of return data:
```JSON
[
	{
		"Product Name" : "Jellybeans",
		"Product id" : 1,
		"Quantity in stock" : 16
	},
	{
		"Product Name" : "Chocolate Bar",
		"Product id" : 3,
		"Quantity in stock" : 27
	},
	{
		"Product Name" : "Cherry Cordials",
		"Product id" : 4,
		"Quantity in stock" : 10
	}
]
```
### 6. Order Endpoints
#### a. Add a new order
The endpoint is '<your_domain>/orders?Product=<product_id>'
Filling in the empty quotes and adding a parameter named 'Product' with the value of the product_id for each product in the order in postman, using the Add New Order method,  or completing and passing the provided JSON with a Product=<product_id> parameter for each product in the order in a POST request will add a new customer with the input information passed in the JSON data with data following the following rules:
* Passwords must contain atleast 8 character, 1 uppercase letter, 1 lowercase letter, 1 numerical digit, and 1 special character
* Username must be unique
```JSON
{
	"customer_id" : customer_id,
	"date" : "date_of_order",
	"expected_delivery" : "date_of_expected_delivery"
}
```
Success Message:
```JSON
{
	"message": "Order added successfully"
}
```
#### b. Update a order
The endpoint is '<your_domain>/orders/<order_id>'
Filling in the empty quotes in postman, using the Update Order method and making sure to fill out all fields to ensure data isn't lost,  or completing and passing the provided JSON in a PUT request will update the order with the order id passed through the URI with the input information passed in the JSON data:
```JSON
{
	"customer_id" : customer_id,
	"date" : "date_of_order",
	"expected_delivery" : "date_of_expected_delivery"
}
```
Success Message:
```JSON
{
	"message": "Product updated successfully"
}
```
#### c. Retrieve all orders
The endpoint is '<your_domain>/orders'
Sending a GET request to this endpoint will return the order data including the data of the linked products for all orders in the database in JSON format. 
Example of return data:
```JSON
[
	{
		"customer_id": 1,
		"date": "2024-08-01",
		"expected_delivery": "2024-08-06",
		"id": 1,
		"products": [
			{
				"id": 1,
				"price": 289.99,
				"product_name": "Video Card"
			},
			{
				"id": 3,
				"price": 394.99,
				"product_name": "CPU"
			}
		]
	},
	{
		"customer_id": 3,
		"date": "2024-08-01",
		"expected_delivery": "2024-08-08",
		"id": 2,
		"products": [
			{
				"id": 6,
				"price": 1289.99,
				"product_name": "High-end Video Card"
			},
			{
				"id": 8,
				"price": 994.99,
				"product_name": "High core count CPU"
			}
		]
	}
]
```
#### d. Retrieve an order by id
The endpoint is '<your_domain>/orders/<order_id>'
Sending a GET request to this endpoint will return the order data including the data of the linked products for the order with the order id passed through the URI in JSON format. 
Example of return data:
```JSON
[
	{
		"customer_id": 1,
		"date": "2024-08-01",
		"expected_delivery": "2024-08-06",
		"id": 1,
		"products": [
			{
				"id": 1,
				"price": 289.99,
				"product_name": "Video Card"
			},
			{
				"id": 3,
				"price": 394.99,
				"product_name": "CPU"
			}
		]
	}
]
```
#### e. Track order by id
The endpoint is '<your_domain>/orders/track_by_id?=<order_id>'
Sending a GET request to this endpoint with the parameter order_id will return the tracking data for the order with the order id passed through the order_id parameter in JSON format. 
Example of return data:
```JSON
{
	"Date Ordered": "Thu, 01 Aug 2024 00:00:00 GMT",
	"Expected Delivery Date": "Tue, 06 Aug 2024 00:00:00 GMT"
}
```
#### f. Retrieve a customer's order history
The endpoint is '<your_domain>/orders/orderhistory?customer_id=<customer_id>'
Sending a GET request to this endpoint with the parameter customer_id will return the order data for the orders placed byt the customer whose id is passed through the customer_id parameter in JSON format. 
Example of return data:
```JSON
[
	{
		"customer_id": 3,
		"date": "2024-07-01",
		"expected_delivery": "2024-07-05",
		"id": 2,
		"products": [
			{
				"id": 15,
				"price": 89.99,
				"product_name": "1TB SSD Drive"
			},
			{
				"id": 27,
				"price": 34.99,
				"product_name": "Webcam"
			}
		]
	},
	{
		"customer_id": 3,
		"date": "2024-07-15",
		"expected_delivery": "2024-07-24",
		"id": 10,
		"products": [
			{
				"id": 12,
				"price": 19.99,
				"product_name": "Compressed Air canister"
			},
			{
				"id": 30,
				"price": 94.99,
				"product_name": "4TB HDD"
			}
		]
	}
]
```
#### g. Delete an order
The endpoint is 'your_domain/orders/<order_id>'
Sending a DELETE request to this end point will delete the customer with the order_id passed from the URI from the Order table in the database:
Success Message:
```JSON
{
	"message": "Order deleted successfully"
}
```