function handleOnInput() {
    const frm = event.target.parentNode;
    // if the description or checkbox value is not equal to data-original-value then
    for (let e of frm.getElementsByTagName('input')) {
        if (e.type === 'submit')
            continue;

        const orig = e.getAttribute('data-original-value');

        const checkboxChanged = e.type === 'checkbox' && e.checked !== (orig === 'checked');
        const textChanged = e.type === 'text' && orig !== e.value;

        if (checkboxChanged || textChanged) {
            setFormUpdate(frm);
            return;
        }
    }

    setFormRemove(frm);
}

function setFormUpdate(frm) {
    const newAction = frm.action.replace('remove', 'update');

    if (frm.action != newAction) {
        frm.action = newAction;

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Update";
    }
}

function setFormRemove(frm) {
    const newAction = frm.action.replace('update', 'remove');

    if (frm.action != newAction) {
        frm.action = newAction;

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Remove";
    }
}