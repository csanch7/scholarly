Scholarly -- https://scholarly-53yu.onrender.com
Overview

Scholarly is a web application that helps students manage their scholarship applications. Users can add, edit, track, and categorize scholarships based on status (e.g., In Progress, Completed, Received), as well as store and manage supporting document links for each application.

The goal of Scholarly is to simplify the scholarship process, reduce stress, and give students an organized dashboard to track deadlines, progress, and application materials.

I built this application because I personally struggled with managing multiple scholarships. I often found myself losing track of deadlines or forgetting which ones I had applied to. Scholarly addresses that problem with personalized tracking tools designed specifically for this case.

Distinctiveness and Complexity
Distinctiveness

Scholarly is not an e-commerce site and not a social network. It is fundamentally different from CS50W Project 2 (Commerce) and Project 4 (Network), and not based on the old Pizza project.

It is not e-commerce: there is no buying, selling, or product listing. Scholarships are not commodities, they are tasks the user privately manages.

It is not a social network: there are no posts, likes, followers, or interaction between users. All data is private to the authenticated user.

Its purpose is unique: it is a personal productivity tool for students managing scholarship applications, with features tailored to deadlines, statuses, and required documents.

Complexity

Scholarly includes multiple layers of functionality that go beyond basic CRUD operations:

- Real-time deadline logic: Scholarships are flagged as expired or active based on the current date, calculated dynamically with both Django and JavaScript.

- Multi-status workflow: Scholarships can be marked as None, In Progress, Completed, or Received, with updates saved via AJAX without reloading.

- Editing & deleting: Users can fully update scholarship details (name, URL, amount, deadline, requirements) or delete scholarships directly from the UI.

- Document management: Each scholarship supports multiple supporting document links. Users can add or remove links dynamically.

- Date-aware filtering: Scholarships can be filtered to hide outdated ones, with sorting by deadline.

- Interactive React components: The index dashboard uses React for searching, filtering, and displaying a summary of near-due-date scholarships.

- User-specific data: Each scholarship is tied to an authenticated user, no cross-user visibility.

- Mobile responsive design: Built with Bootstrap 5, layouts adapt to smaller screens.

File Descriptions
models.py

Defines the Scholarship model. Each scholarship is linked to a user and contains:

Name, URL, deadline, amount, requirements

Category (None, In Progress, Completed, Received)

A list of document links

views.py

Handles all application logic:

index : dashboard showing all active scholarships

compose : add a scholarship

edit : edit scholarship details (AJAX-powered)

scholarship : detail view for a scholarship, with category selection

remove : delete a scholarship

completedview : shows completed scholarships

recievedScholarship : mark scholarships as received/not received

adddocumentlink : add/remove supporting document links

urls.py

Maps URLs to scholarship/user views.

templates/

layout.html – base layout & navbar

index.html – React-powered dashboard with search, filters, and summary of deadlines

add.html – form to create new scholarships

edit.html – update existing scholarship details

scholarship.html – detail view: update category, manage links, delete scholarship

completed.html – list of completed scholarships

register.html – user registration page

login.html – login page

static/scholarship/

styles.css – custom styling

React/JS logic for dashboard interactivity

requirements.txt

Lists required packages to run the project.

How to Run
python manage.py runserver


Then open the local server in your browser (default: http://127.0.0.1:8000/).
