function appendEmptyItems() {
    const lists = document.getElementsByClassName('todo-list');

    for (let list of lists) {
        appendEmptyItem(list);
    }
}

appendEmptyItems();


/**
*   Makes an AJAX request to the backend. If successful, creates an new empty item element.
*
*   @param {element} itemInput - an item input element
*/
async function handleAddItem(itemInput) {

    li = itemInput.parentElement;

    const created = await addNewItem(itemInput);

    // add an empty
    if (created) {
        appendEmptyItem(li.parentElement);
    }
}


/**
*   Makes an AJAX request to the new item creation endpoint. If successful, the given element and its siblings are
*   replaced with the HTML response.
*
*   @param {element} textInputElement - the text input element for an item
*   @returns {boolean} True if the fetch was successful (status code 200) and false otherwise
*/
async function addNewItem(textInputElement) {

    if (textInputElement.value === '') {
        console.log('Item cannot be empty');
        return false;
    }

    const data = {
        'description': textInputElement.value,
    };

    const response = await fetch('/additem', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

    if (response.status != 200) {
        console.log(response);
        return false;
    }

    // get the HTML response
    const responseText = await response.text();

    // replace this content with the new item element
    const li = textInputElement.parentElement;
    li.innerHTML = responseText;

    return true;
}


/**
*   Makes an AJAX request to get a new item template and appends an empty item to the given <ul> element
*
*   @param {element} ul - a <ul> element
*/
async function appendEmptyItem(ul) {

    const response = await fetch('/emptyitem');
    const responseText = await response.text();

    // create a new
    const liNode = document.createElement('li');
    liNode.innerHTML = responseText;

    ul.appendChild(liNode);
}


/**
*   Changes the given <input> button to an Update button
*
*   @param {element} inputButton - an <input> button element corresponding to an item
*   @param {integer} itemId - the item id
*/
function handleUpdateButton(inputButton, itemId) {

    if (inputButton.value != 'Update') {
        inputButton.setAttribute('class', 'btn-update');
        inputButton.setAttribute('onclick', `handleUpdateItem(this.previousElementSibling, ${itemId})`);
        inputButton.value = 'Update';
    }
}


/**
*   Makes an AJAX request to update the item where item id == item.id then replaces the item with HTML received from the
*   response.
*
*   @param {element} itemInput - the text <input> element of an item
*   @param {integer} itemId - the item id
*/
async function handleUpdateItem(itemInput, itemId) {

    const response = await fetch(`/${itemId}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                description: itemInput.value
            }),
        });

    if (response.status != 200) {
        console.log(response);
        return false;
    }

    // get the HTML response
    const responseText = await response.text();

    // replace the element
    const li = itemInput.parentElement;
    li.innerHTML = responseText;
}


/**
*   Makes an AJAX request to the remove item endpoint. If successful, the given item input element and its siblings are
*   deleted from the <ul>
*
*   @param {element} itemInput - an item input element
*   @param {integer} itemId - the item id
*   @return - True if the fetch was successful (status code 200) and false otherwise
*/
async function handleRemoveItem(itemInput, itemId) {

    const response = await fetch(`/${itemId}/remove`, { method: 'POST' });

    if (response.status == 200) {
        // remove the element from the list
        const li = itemInput.parentElement;
        li.parentNode.removeChild(li);
    }
}