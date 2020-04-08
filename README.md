# Todo Lists

A web application manages items in a todo list

## Endpoints

### /

***HTTP Methods***

**GET** | Displays a login form or, if a user is logged in, a list of user-defined items.

### /register

***HTTP Methods***

**GET** | Provides a form so the user can create an account.

**POST** | Sends form data to server.

### /login

***HTTP Methods***

**GET** | Provides a form for the user to login to their account.

**POST** | Sends form data to server.


### /additem

***HTTP Methods***

**POST** | Adds an item to the todo list from JSON data provided in the body

    {
        description: <string>
    }

> **201** | Created. Returns an item snippet with the new data. This includes an <input> element to update the item
> description and a "button" <input> element to delete the item

> **400** | Bad Request. The body does not contain the description


### /<item_id>/update

***HTTP Methods***

**POST** | Updates an item. Only one of the following arguments are required

    {
        description: <string>
    }

> **200** | OK. Returns an item snippet with the new data. This includes an <input> element to update the item
> description and a "button" <input> element to delete the item.
>
> **403** | Forbidden. Attempting to update an item that does not belong to the current user.
>
> **404** | Not Found. The item item does not exist 


### /<item_id>/remove

***HTTP Methods***

**POST** | Deletes an item.

> **200** | OK
>
> **403** | Forbidden. Attempting to delete an item that does not belong to the current user.
>
> **404** | Not Found. The item does not exist 