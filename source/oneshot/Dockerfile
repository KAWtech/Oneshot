# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Change to the source directory where your src folder is located
WORKDIR /app/oneshot/src

# Expose the port the app runs on
EXPOSE 3001

# Define the command to run your app
CMD ["npm", "start"]
