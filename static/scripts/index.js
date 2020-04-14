// set input box widths
const inputs = document.getElementsByTagName('input[type="text"]');

for (let input of inputs) {
    dynamicWidth(input);
}


function dynamicWidth(target) {
    const element = target || event.target;
    element.style.width = 3 + (element.value.length * 1.2) + 'ch';
    console.log(element, element.style.width)
}


function handleListOnInput() {
    handleOnInput(setListUpdate, setListDelete);
}


function handleItemOnInput() {
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

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Update";
    }
}


function setListDelete(frm) {
    const newAction = frm.action.replace('update', 'delete');

    if (frm.action != newAction) {
        frm.action = newAction;

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Delete";
    }
}


function setItemUpdate(frm) {
    const newAction = frm.action.replace('remove', 'update');

    if (frm.action != newAction) {
        frm.action = newAction;

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Update";
    }
}


function setItemRemove(frm) {
    const newAction = frm.action.replace('update', 'remove');

    if (frm.action != newAction) {
        frm.action = newAction;

        // update button text
        const submit = frm.querySelector('input[type=submit]');
        submit.value = "Remove";
    }
}