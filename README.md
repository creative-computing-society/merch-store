# Merch Store

Portal for distributing Creative Computing Society merch to society members.

## Tech Stack

**Client**: NodeJS, ReactJS, Vite, Axios, TailwindCSS

**Server**: Python, Django-Rest-Framework

**Database**: PostgreSQL

## Run Live Production

Visit [https://merch.ccstiet.com/](https://merch.ccstiet.com/) for using the website on live production environment

## Run Locally

### Clone this project

```sh
git clone https://github.com/creative-computing-society/merch-store.git
```

### To start the frontend server

Go to project directory

```sh
cd frontend
```

Install the project dependencies

```sh
npm i
```

Run the start script

```sh
npm run dev
```

### To start the backend server

Go to the project directory

```sh
cd backend/config
```

We recommend you to use a virtual environment

```sh
python -m venv env
```

Activate virtual environment

For Windows PowerShell:

```sh
env/Scripts/activate.ps1
```

For Linux and MacOS:

```sh
source env/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Create a \`.env\` file in the project's root directory (base directory), and add \`DEBUG\`, \`ALLOWED_HOSTS\`, \`SECURITY_KEY\`, \`EMAIL_HOST_USER\`, and \`EMAIL_HOST_PASSWORD\`.

This project uses CCS Single Sign On (SSO) for user authentication. You would be required to add \`JWT_SECRET_KEY\` to the \`.env\` aswell which would be equal to the application's client secret created on CCS Auth portal.

You would also be required to add \`PAYU_MERCHANT_KEY\` and \`PAYU_MERCHANT_SALT\` for the utilisation of PayU Payment Gateway.

At last, you would be required to add the database credentials in the \`.env\` file aswell, which includes the fields \`DATABASE_URL\`, \`POSTGRES_NAME\`,\`POSTGRES_USER\`, \`POSTGRES_PASSWORD\`, \`POSTGRES_HOST\`, and \`POSTGRES_PORT\`.

Run Migrations

```sh
python manage.py makemigrations
```

```sh
python manage.py migrate
```

Start the server

```sh
python manage.py runserver
```

## Endpoints

### Legends

-   (⭕) - Authentication (correct token in localStorage) is required
-   (🔵) - Staff/Admin permissions required

### Auth

-   POST /auth/login/ - Login user with token from CCS SSO
-   (⭕) GET /auth/logout/ - Logout user
-   (⭕) GET /auth/user/ - Get user details

### Products

-   (⭕) GET /product/all/ - Fetches all product data
-   (⭕) GET /product/\<int:product_id\>/ - Fetches single product data by id
-   (⭕) POST /cart/add/ - Adds product to cart
-   (⭕) GET /cart/view/ - View cart items
-   (⭕) POST /cart/delete/ - Deletes product from cart
-   (⭕) POST /cart/update/ - Update cart product parameters like quantity

### Orders

-   (⭕) GET /order/all/ - Fetches all previous orders
-   (⭕) GET /order/\<int:order_id\>/ - Fetches single order details by id
-   (⭕) POST /order/place/ - Place order for the current cart items
-   (⭕) POST /order/apply-discount/ - Apply discount code on the order
-   (⭕) POST /payment/\<int:order_id\>/ - Fetch payment details for the order id
-   POST /payment/success/ - Handled by PayU Gateway
-   POST /payment/failure/ - Handled by PayU Gateway
-   (⭕) POST /payment/verify/ - Verifies payment status after successful/failed payment

### Dashboard

-   (🔵) GET /dashboard/ - Renders Dashboard page template
-   (🔵) POST /stop-orders/ - Stops accepting all orders and clears cart items
-   (🔵) POST /start-orders/ - Starts accepting all orders
-   (🔵) GET /discount-codes/ - Renders Discount Code page template
-   (🔵) POST /discount-codes/create/ - Creates a discount code
-   (🔵) POST /discount-codes/edit/\<int:code_id\>/ - Edits a discount code with code id
-   (🔵) POST /discount-codes/delete/\<int:code_id\>/ - Deletes a discount code with code id
-   (🔵) GET /products/ - Renders Products page template
-   (🔵) POST /products/create/ - Creates a product
-   (🔵) POST /products/edit/\<int:product_id\>/ - Edits a product with code id
-   (🔵) POST /products/delete/\<int:product_id\>/ - Deletes a product with code id
-   (🔵) GET /scan_qr/ - Renders Scan QR code page template
-   (🔵) POST /scan_qr/scan/ - Verify details and marked as delivered after successful scan
-   (🔵) POST /export_csv/\<int:id\>/ - Exports a CSV file for given order item id

## Maintainers

-   [Akshat Bakshi - @akshat448](https://github.com/akshat448/)
-   [Sakshham Bhagat - @SakshhamTheCoder](https://github.com/sakshhamthecoder/)
