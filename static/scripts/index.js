function handleListOnInput() {
    handleOnInput(setListUpdate, setListDelete);
}


function handleItemOnInput() {
    if (event.target.type === 'checkbox') {
        const frm = event.target.parentNode;

        const textInput = frm.querySelector('input[type=text]');
        textInput.classList.toggle('checked');
    }

    handleOnInput(setItemUpdate, setItemRemove);
}


function handleOnInput(onChange, onUnchanged) {
    const frm = event.target.parentNode;

    // if the description or checkbox value is not equal to data-original-value then
    for (let e of frm.getElementsByTagName('input')) {
        if (e.type === 'submit')
            continue;

        const orig = e.getAttribute('data-original-value');

        const checkboxChanged = e.type === 'checkbox' && e.checked !== (orig === 'checked');
        const textChanged = e.type === 'text' && orig !== e.value;

        if (checkboxChanged || textChanged) {
            onChange(frm);
            return;
        }
    }

    onUnchanged(frm);
}


function setListUpdate(frm) {
    const newAction = frm.action.replace('delete', 'update');

    if (frm.action != newAction) {
        frm.action = newAction;

        const submit = frm.querySelector('input[type=submit]');
        submit.className = 'btn-update';
        submit.title = "Update list name"
    }
}


function setListDelete(frm) {
    const newAction = frm.action.replace('update', 'delete');

    if (frm.action != newAction) {
        frm.action = newAction;

        const submit = frm.querySelector('input[type=submit]');
        submit.className = 'btn-delete';
        submit.title = "Delete list"
    }
}


function setItemUpdate(frm) {
    const newAction = frm.action.replace('remove', 'update');

    if (frm.action != newAction) {
        frm.action = newAction;

        const submit = frm.querySelector('input[type=submit]');
        submit.className = 'btn-update';
        submit.title = "Update item"
    }
}


function setItemRemove(frm) {
    const newAction = frm.action.replace('update', 'remove');

    if (frm.action != newAction) {
        frm.action = newAction;

        const submit = frm.querySelector('input[type=submit]');
        submit.className = 'btn-delete';
        submit.title = "Remove item"
    }
}