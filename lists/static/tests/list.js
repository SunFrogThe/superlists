function initialize() {
    $('input[name="text"]').on('keypress',
        () => $('.is-invalid').hide());
}
