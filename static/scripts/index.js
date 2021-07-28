
const isCheckbox = (input) => input.type === 'checkbox';
const isText = (input) => input.type === 'text';

const ORIGINAL_VALUE_ATTRIBUTE = 'data-original-value';
const DEFAULT_SUBMIT_TIMEOUT = 1200;

// form submission timeout ids
// an object to track form submission timeouts
const submitManager = {};

function autoSubmit(tts=DEFAULT_SUBMIT_TIMEOUT) {
    const matches = (val1, val2) => val1 === val2;

    const target = event.target;
    const form = target.closest('form');

    // stop timeout if the form is queued to submit
    if (form.id in submitManager) {
        clearTimeout(submitManager[form.id]);
        delete submitManager[form.id];
    }

    // add a new timeout if the content was changed
    if (inputChanged(form)) {
        flashInfo(form, 'Update queued')

        const onSuccess = () => {
            // set data-default-value to match current value
            syncInputValues(form);
            flashSuccess(target, 'Up to date');
        };
        const onError = (err) => {
            // reset value
            const formInput = form.querySelector('input[type=text]');
            formInput.value = formInput.getAttribute(ORIGINAL_VALUE_ATTRIBUTE);
            flashError(target, err);
        };

        const submitTimeout = setTimeout(() => {
            postFormData(form, onSuccess, onError);
            delete submitManager[form.id];
        }, tts);

        submitManager[form.id] = submitTimeout;
    } else {
        flashSuccess(target, 'Up to date');
    }


    function inputChanged(form) {

        for (const input of form.getElementsByTagName('input')) {

            // get the original content
            const origValue = input.getAttribute(ORIGINAL_VALUE_ATTRIBUTE);

            // skip elements who don't have the ORIGINAL_VALUE_ATTRIBUTE attribute
            if (origValue === null) continue;

            const contentChanged = isCheckbox(input) && !matches(input.checked, origValue === 'checked') ||
                    isText(input) && !matches(input.value, origValue);

            if (contentChanged) return true;
        }

        return false;
    }


    async function postFormData(form, callback, err) {

        const response = await fetch(form.action, {
            method: 'post',
            body: new FormData(form)
        });

        const data = await response.text();

        if (response.status === 200) {
            callback(data);
        } else {
            err(data);
        }
    }


    function syncInputValues(form) {

        // update button title
        const button = form.querySelector('button');
        const textInput = form.querySelector('input[type=text]');

        const originalValue = textInput.getAttribute(ORIGINAL_VALUE_ATTRIBUTE);
        const newTitle = button.getAttribute('title').replace(originalValue, textInput.value)
        button.setAttribute('title', newTitle);

        for (let input of form.getElementsByTagName('input')) {
            if (isCheckbox(input))
                input.setAttribute(ORIGINAL_VALUE_ATTRIBUTE, input.checked ? 'checked': 'unchecked');
            else if (isText(input))
                input.setAttribute(ORIGINAL_VALUE_ATTRIBUTE, input.value);
        }
    }
}


function updateInputClassList(target=event.target) {

    const isChecked = target.checked;

    const form = target.closest('form');

    for (let input of form.querySelectorAll('input[type=text]')) {
        if (isChecked && !input.classList.contains('checked')) {
            input.classList.add('checked');
        } else if (!isChecked && input.classList.contains('checked')) {
            input.classList.remove('checked');
        }
    }
}


async function handleCreateList() {

    // fetch the new list template
    const response = await fetch(event.target.getAttribute('formaction'), { method: event.target.getAttribute('formmethod') });
    const data = await response.text();

    if (response.status === 200) {
        // append the element to the document before the Create New List div
        const div = document.getElementById('last-card');
        for (let node of stringToHtmlElements(data)) {
            div.parentNode.insertBefore(node, div);
        }
    }
}


async function handleDelete(className) {

    const target = event.target;

    const response = await fetch(event.target.getAttribute('formaction'), { method: event.target.getAttribute('formmethod') });

    if (response.status === 200) {
        const nodeToDelete = target.closest(className);
        nodeToDelete.parentNode.removeChild(nodeToDelete);
    } else {
        const err = await response.text();
        target.closest('.flash').innerText = err;
    }
}


async function handleAddItem() {
    // stop form from leaving the page
    event.preventDefault();

    const form = event.target;

    // fetch the new item
    const response = await fetch(form.action, {
        method: form.getAttribute('method'),
        body: new FormData(event.target)
    });
    const data = await response.text();

    if (response.status === 200) {
        // create a new list element
        const newLi = document.createElement('li');
        newLi.classList.add('list__item');

        // append the html data received from the fetch
        for (let node of stringToHtmlElements(data)) {
            newLi.appendChild(node);
        }

        // add it before add item list element
        const ul = form.closest('ul');
        ul.insertBefore(newLi, ul.querySelector('.last.list__item'));

        flashSuccess(form, 'Up to date');
    }

    clearForm(form);
    
    
    function clearForm(form) {
        form.reset();

        for (let input of form.querySelectorAll('input[type=text]')) {
            input.classList.remove('checked');
        }
    }
}


function stringToHtmlElements(htmlString) {
    // convert string data into an html element we can use
    const template = document.createElement('template');
    template.innerHTML = htmlString.trim();
    return template.content.childNodes;
}


function flashSuccess(target, text) {
    closestFlashElement(target, flash => {

        flash.classList.remove('info');
        flash.classList.remove('error');

        if (!flash.classList.contains('success')) {
            flash.classList.add('success');
        }

        flash.innerText = text;
    });
}


function flashInfo(target, text) {
    closestFlashElement(target, flash => {

        flash.classList.remove('success');
        flash.classList.remove('error');

        if (!flash.classList.contains('info')) {
            flash.classList.add('info');
        }

        flash.innerText = text;
    });
}


function flashError(target, text) {
    closestFlashElement(target, flash => {

        flash.classList.remove('success');
        flash.classList.remove('info');

        if (!flash.classList.contains('error')) {
            flash.classList.add('error');
        }

        flash.innerText = text;
    });
}


function closestFlashElement(target, callback) {
    const card = target.closest('.tasklist__card');
    if (card) {
        const flash = card.querySelector('.flash');
        if (flash)
            return callback(flash);
    }
}
