# Members
Irfan, BY, layla, elvis

# Module 2:
🐳 Dockerfile
The Dockerfile is responsible for creating the CareBridge Hospital container environment.

A simplified version of the Dockerfile is:

FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

CMD ["python", "app.py"]
Dockerfile Instructions
Instruction	Purpose
FROM	Selects the Python base image
WORKDIR	Sets the working directory
COPY	Copies project files into the image
RUN	Installs project dependencies
EXPOSE	Documents the application port
CMD	Starts the Flask application
🚀 Running with Docker Compose
Docker Compose is the recommended way to run CareBridge Hospital.

1. Open the project directory
PowerShell:

cd "C:\Users\[name]\Downloads\CareBridge-Hospital"
If the repository was cloned into another directory, use that directory instead.

2. Build and start the application
docker compose up --build
The application will be available at:

http://localhost:5000
3. Run in the background
To start the application in detached mode:

docker compose up --build -d
4. Check the container
docker compose ps
You should see the CareBridge container running and port 5000 mapped.

Example:

carebridge-hospital-container
0.0.0.0:5000->5000/tcp
5. View application logs
docker compose logs
To continuously follow the logs:

docker compose logs -f
6. Stop the application
docker compose down
🐳 Running with Docker Directly
Docker Compose is recommended, but the application can also be started manually.

Build the Docker image
docker build -t carebridge-hospital .
Run the container
docker run -p 5000:5000 carebridge-hospital
Then open:

http://localhost:5000
💾 SQLite Database Persistence
The project uses a Docker volume mapping for the SQLite database.

The docker-compose.yml contains a database mapping similar to:

volumes:
  - ./carebridge.db:/app/carebridge.db
This maps the SQLite database on the host machine to the database location inside the Docker container.

Why this is important
Without persistent storage, data stored only inside a container could be lost when the container is removed.

The volume mapping allows the project to continue using the host's:

carebridge.db
when the Docker container is restarted.
# Module 
🌐 Using ngrok
ngrok is used as a local internet gateway to make the locally running CareBridge Hospital application accessible through a public HTTPS URL.

The CareBridge application runs on port 5000.

The basic architecture is:

Internet
   │
   ▼
 ngrok Public HTTPS URL
   │
   ▼
Port 5000
   │
   ▼
Docker Container
   │
   ▼
Flask Application
   │
   ▼
SQLite Database
🌐 ngrok Setup
1. Start CareBridge Hospital
Open PowerShell:

cd "C:\Users\[name]\Downloads\CareBridge-Hospital"
Start Docker Compose:

docker compose up -d
Check that the container is running:

docker compose ps
Then test the local application:

http://localhost:5000
Make sure CareBridge Hospital works locally before starting ngrok.

2. Locate the ngrok Executable
Because ngrok is installed through the Microsoft Store, the executable may not be directly available through the normal PowerShell PATH.

Run:

$pkg = Get-AppxPackage ngrok.ngrok
Then locate ngrok.exe:

$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
This stores the location of the ngrok executable in:

$ngrokExe
3. Start th
