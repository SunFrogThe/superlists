window.SuperLists = {};
window.SuperLists.initialize = () => {
    $('input[name="text"]').on('keypress',
        () => $('.is-invalid').hide());
}
