function handleOnInput() {
    const target = event.target;
    const form = target.parentNode;

    const isCheckbox = (node) => node.type === 'checkbox';
    const isText = (node) => node.type === 'text';
    const matches = (v1, v2) => v1 === v2;

    const setShowDelete = (show) => {
        const btn = form.querySelector('input[value="Delete"]');
        btn.hidden = !show;
    }
    const setShowUpdate = (show) => {
        const btn = form.querySelector('input[value="Update"]');
        btn.hidden = !show;
    }

    for (let node of form.getElementsByTagName('input')) {

        // get the original content
        const origValue = node.getAttribute('data-original-value');

        // skip elements who don't have the 'data-original-value' attribute
        if (origValue === null) continue;

        const contentChanged = isCheckbox(node) && !matches(node.checked, origValue === 'checked') ||
                isText(node) && !matches(node.value, origValue);

        if (contentChanged) {
            // set visible form button to update
            setShowDelete(false);
            setShowUpdate(true);

            return true;
        }
    }

    // set visible form button to delete
    setShowDelete(true);
    setShowUpdate(false);

    return false;
}

// form submission timeout ids
// an object to track form submission timeouts
const submissions = {};
const autoSubmitTimeout = 1500;
const flashMessages = {
    'queued': "Queued",
    'saving': "Saving...",
    'saved': "Saved",
    'error': (msg) => msg
};

function autoSubmit() {

    const form = event.target.parentNode;

    if (form.id in submissions) {
        clearTimeout(submissions[form.id]);
        delete submissions[form.id];
    }

    // compare each input with its original value (ignore type='submit')
    if (contentChanged(form)) {
        submissions[form.id] = newTimeout(form);
    }


    function newTimeout(form) {
        return setTimeout(() => {
            form.submit();
            delete submissions[form.id];
        }, 3000);
    }


    function contentChanged(form) {
        const isCheckbox = (node) => node.type === 'checkbox';
        const isText = (node) => node.type === 'text';
        const matches = (v1, v2) => v1 === v2;

        for (let node of form.getElementsByTagName('input')) {

            // get the original content
            const origValue = node.getAttribute('data-original-value');

            // skip elements who don't have the 'data-original-value' attribute
            if (!origValue) continue;

            const contentChanged = isCheckbox(node) && !matches(node.checked, origValue === 'checked') ||
                    isText(node) && !matches(node.value, origValue);

            if (contentChanged) {
                return true;
            }
        }

        return false;
    }
}

function autoSubmitNoRefresh() {

    const form = event.target.parentNode;

    // stop submission if the form is queued to submit
    if (form.id in submissions) {
        clearTimeout(submissions[form.id]);
        delete submissions[form.id];
    }

    // add a new timeout if the content was changed
    if (inputChanged(form)) {
        submissions[form.id] = newTimeout(form);
    }


    function newTimeout(form) {
        return setTimeout(() => {
            fetchHTML(form);
            delete submissions[form.id];
        }, autoSubmitTimeout);


        async function fetchHTML(form) {
            const response = await fetch(form.action, { method: 'POST' });
            if (response.status === 200) {
                const data = await response.text();
                console.log(data);
            } else {
                console.log(response);
            }
        }
    }
}


function inputChanged(form) {
    const isCheckbox = (node) => node.type === 'checkbox';
    const isText = (node) => node.type === 'text';
    const matches = (v1, v2) => v1 === v2;

    for (let node of form.getElementsByTagName('input')) {

        // get the original content
        const origValue = node.getAttribute('data-original-value');

        // skip elements who don't have the 'data-original-value' attribute
        if (origValue === null) continue;

        const contentChanged = isCheckbox(node) && !matches(node.checked, origValue === 'checked') ||
                isText(node) && !matches(node.value, origValue);

        if (contentChanged) return true;
    }

    return false;
}


function replaceElement(oldElement, newElement) {


}


function insertElementBefore(element, newElement) {

}