# TicketShow App

## Overview

The TicketShow App is a user-friendly movie ticket booking platform that provides seamless access to the latest movie releases and showtimes. With an intuitive interface, users can easily browse through a wide selection of movies and reserve their tickets hassle-free.

## Getting Started

To run the TicketShow App on your local machine, follow these steps:

### Prerequisites

- Python (3.6 or higher)
- Node.js and npm (Node Package Manager)

### Backend Setup

1. Navigate to the backend directory:

```bash
cd TicketShow2/TicketShow2_B
```

2. Install Python dependencies:

```
pip install -r requirements.txt
```

3. Update config.py for Redis and Celery:
Make sure you have Redis installed on your machine. If not, you can download it from the official Redis website (https://redis.io/download) and follow the installation instructions for your operating system.

In the config.py file, update the Redis and celery configuration settings according to your setup.

4. Start the Redis server:
```
sudo service redis-server start
```
5. Start Celery Worker for background task processing:
```
celery -A app.celery worker --l INFO
```

6. Start Celery Beat for periodic task scheduling:
```
celery -A app.celery beat --l INFO
```

7. Start the Flask development server:

```
flask run
```

### Frontend Setup

1. Open a new terminal or command prompt.

2. Navigate to the frontend directory:

```
cd TicketShow2/TicketShow2_F

```

3. Install Node.js dependencies:

```
npm install
```

4. Start the Vue.js development server:

```
npm run dev
```

Accessing the App
The backend server will be running on http://localhost:5000, and the frontend development server will be running on http://localhost:8080. Access the TicketShow App through your web browser using the provided URLs.

## Contact Information

For any issues or inquiries, please contact the project author at:

- Author: Azhar Bihari
- Email: azhrbhr@gmail.com

Thank you for using the TicketShow App! Enjoy hassle-free movie ticket booking.
