
# Merch Store
Portal for distributing Creative Computing Society merch to society members.

## Tech Stack
**Client**: ReactJs

**Server**: Python, Django-Rest-Framework

**Database**: PostgreSQL

## Run Locally
### Clone this project
```sh
git clone https://github.com/creative-computing-society/ec-store-new.git
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

Create a \`.env\` file in the project's root directory (base directory), and add \`SECURITY_KEY\`, \`EMAIL_HOST_USER\`, and \`EMAIL_HOST_PASSWORD\`.

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
# Endpoints
- 