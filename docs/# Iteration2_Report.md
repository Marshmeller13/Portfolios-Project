# Iteration 2 Report

For week two, we focused on finishing any uncompleted tasks from the previous iteration, designing a login and homepage for the site, and adding the ability to upload projects to a portfolio 


## Tasks Responsible For 

### Cameron
 
 > ### Create a Homepage
 Will be creating a homepage for the site
 
 1. Buttons available for features to be implemented via
 2. Clean Design for Site
 3. Overall finished Design for Homepage of site

### Noah
 
 > ### Upload Projects to Portfolio
 - As a creator, I want to be able to upload my projects to a portfolio so that future employers can see them so that I won't have to email or physically get one instead.
 - Confirmation: User/Creator can upload their projects to a portfolio.

 1. User can access their portfolio
 2. User can upload file to the portfolio
 3. User files appear when accessing the portfolio

### Blake
 
 > ### Finish User Login and Resume Template
 - Finish User Login and Resume Template design from Iteration 1

 1. Information will be stored in a database after being entered
 2. Login information will be accepted or rejected
 3. Creat resume template for displaying resumes


## Tasks Completed

### Cameron 

 1. Created clean design for login page (Not Functionality)
 2. Created profile page with a navbar of buttons that can be used in future iterations
 3. Created post page with a navbar of buttons that can be used in future iterations
 4. Designed a logo for the company with Adobe Illustrator 

### Noah

 1. Created database schema for uploaded resumes
 2. Added functions/routes to allow for the uploading of a pdf resume to the site
 3. Created a basic input form for creating a resume on the site. 
 4. Created a basic html page for uploading a resume

- A portion of the code for uploading a pdf to a sql database was taken from a Pynative tutorial. From what I could find, the basic process for uploading a file using HTML and flask is fairly simply, but the act of storing it in the database as opposed to just saving the file caused some problems.

### Blake

 1. Created database schema for a User index
 2. re-wrote app path for logging in
 3. modified HTML form for login.


## Tasks Planned but Not Finished

### Cameron 

 - Profile page design is not complete. I decided that it made more sense to wait until other aspects of the project are finished in order to properly implement an effective design for the profile page (e.g. I am not sure how much space will be required for the users generated protfolio as they cannot be generated yet)
 - Posts page design is not complete. Similar to Profile page I decided to wait until other aspects of the project were finished before designing a full site

### Noah

 - All assigned tasks finished

### Blake

 - Did not display resumes because I did not want to interfere with noah's work

## Helpful Process

### Cameron

 - I found that using the site "HTML Color Codes" was very useful in determining the values of colors used in the logo so that they could also be used for the background of the site

### Blake

 - DBFiddle was especially helpful in figuring out my syntax problems. Flaskr 1.1 documentation was also something I referred to frequently 

# Iteration 3 Plan

### Cameron
 
 > ### Share Profiles

 1. Share button appears on profiles
 2. When clicked button gives options on how and who to send to
 3. When sent the button links to the profile
 4. Add a customized design to link in order to look more professional

### Noah
 
 > ### Resumes and Posts

 1. Displaying the resumes assigned to specific users
 2. Editing or deleting posts 
 3. Displaying uploaded resumes
 4. Routes for converting back to an image file

### Blake
 
 > ### Account Creation

 1. Users will be able to create unique accounts
 2. Link to new account form on login page 
 3. Create session id within cookies to keep user logged in
 4. fix flash() functionality
