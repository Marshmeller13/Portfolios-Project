# Iteration 3 Report

For week three, we focused on making profiles shareable, adding the ability to post, display, and delete resumes, and on adding account creation 


## Tasks Responsible For 

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


## Tasks Completed

### Cameron 

 1. Share button appears on profile page
 2. When clicked button takes you to sites share page
 3. shares link to profile (because the page is still just an html it links to another site as a proof of concept. Would need to change to sites url for final iteration)
 4. Buttons are companies logo so user can easily know how they are trying to share their profile 
 5. Created README.md file

### Blake

 1. Users can now make a unique account
 2. Link to new account form on login page is functional 
 3. flash() alerts now show up in the login page and are styled correctly

### Noah 


## Tasks Planned but not Finished

### Cameron 

 - When sharing via email the users name does not appear in standardized message 

### Blake

 - Adding session id's to keep a user logged in. (Will add once we are done with basic website layouts)

### Noah 

 - Display uploaded resumes

## Troubles Encountered 

### Cameron 

 - Issues with code not loading correctly, the file needed to be force-reloaded.

### Blake

 - flash() funtionality needed to be executed in HTML code, as the actual flash() function in python basically only adds the messages to a library.

### Noah 

 - No major troubles encountered

## Adjustments to overall design 

### Cameron 

 - Removed share button from overlay navbar and instead decided to have the share button available on the page itself. I did this for a cleaner design to the page and it is now more user friendly as it is more obvious how to share and requires less clicks to do so. 

### Blake

 - Added signup.html which is basically a copy of login.html. 

### Noah 

 - No major adjustments made 

## Helpful Process

 - https://blog.tecladocode.com/flashing-messages-with-flask/ was very helpful in describing how to get flash() to work 

 - Utilizing discord to consult with Professor Liffiton 

 - Referenced the code to my original Flaskr project for the edit/delete buttons


## Iteration 4 Plan

### Cameron

 > ### Runnable Code 

 1. Make code able to be displayed on profile page
 2. Make code runnable on profile page
 3. Minor adjustments to site design - cleaning up site overall

### Blake

 > ### Unit Tests

 1. Create unit tests for code
 2. Make sure code is able to pass unit tests and is written effectively 

### Noah 

 > ### Display resumes

 1. Display uploaded resumes
 2. Display resumes based on user - User creation wasn't done last week so couldn't connect to specific users
 3. Upgrade resume creation template, design