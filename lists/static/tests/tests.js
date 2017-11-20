QUnit.test('smoke test', assert => {
    const $error = $('.is-invalid');
    assert.equal($error.is(':visible'), true);
    $error.hide();
    assert.equal($error.is(':visible'), false);
});

QUnit.test('smoke test', assert => {
    const $error = $('.is-invalid');
    assert.equal($error.is(':visible'), true);
    $error.hide();
    assert.equal($error.is(':visible'), false);
});

QUnit.test('errors should be hidden on keypress',
    assert => {
        initialize();
        $('input[name="text"]').trigger('keypress');
        assert.equal($('.is-invalid').is(':visible'), false);
    });

QUnit.test("errors aren't hidden if there is no keypress",
    assert => {
        initialize();
        assert.equal($('.is-invalid').is(':visible'), true);
    }
);