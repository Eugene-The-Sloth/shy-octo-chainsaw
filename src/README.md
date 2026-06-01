# Mergington High School Activities

A web application that allows students to view and sign up for extracurricular activities at Mergington High School, with teacher-managed registration.

## Features

- View all available extracurricular activities with detailed information:
	- Activity descriptions and schedules
	- Current enrollment and capacity indicators
	- Real-time availability status
- Filter activities by:
	- Category (Sports, Arts, Academic, Community, Technology)
	- Day of the week
	- Time slots (Before School, After School, Weekend)
- Search activities by name or description
- Teacher authentication for managing registrations
- Student registration system with capacity limits
- Participant management (signup/removal) by authenticated teachers

## Current Activities

Activities include various clubs and teams such as:
- Chess Club (Mon/Fri afternoons)
- Programming Class (Tue/Thu mornings)
- Morning Fitness (Mon/Wed/Fri early mornings)
- Sports Teams (Soccer, Basketball)
- Manga Club (Tuesday evenings)
- And many more!

## Technical Implementation

- Backend: FastAPI with in-memory data store
- Frontend: Vanilla JavaScript with responsive design
- Authentication: Teacher login system for managing registrations
- Real-time updates: Dynamic activity status and capacity tracking

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).

> **Note**: The application currently uses an in-memory database implementation. Data resets when the server restarts.
