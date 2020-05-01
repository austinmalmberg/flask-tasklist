# Tasklists

A single-page application for managing things to do in your daily life. Create one or multiple tasklists and allows the user to check items off as they're completed!

## Endpoints

#### /

Displays the user's tasklists. If no user is logged in, redirects to **/login**

### Authentication

#### /login

Provides a form for the user to login to their account.

#### /register

Provides a form so the user can create an account.

### Tasklist

#### /create

Creates a new tasklist for the user and returns a tasklist template.  This template is added before the last element (the Create New div) in the tasklist--container.

#### /<list_id>/update

Returns a template for the new header on status 200 (OK). **NOTE:** This is not utilized in the current version.  Right now, the client-side script updates sets the data-original-value attribute on <input>s to their current values on status 200 (OK).

#### /<list_id>/delete

Removes the tasklist and all items in that list. On status 200 (OK), removes the tasklist--card representing the tasklist from the DOM.

#### /<list_id>/additem

Adds an item to the tasklist. On status 200 (OK), returns an <form> element representing the item. 

#### /<list_id>/<item_id>/update

Updates an item and returns a <form> element representing the updated item. **NOTE:** This is not utilized in the current version. Right now, the client-side script sets the data-original-value attribute on <input>s to their current values on status 200 (OK).

#### /<list_id>/<item_id>/remove

Deletes an item. On status 200 (OK), removes the list--item <li> from the task--list <ul>.
