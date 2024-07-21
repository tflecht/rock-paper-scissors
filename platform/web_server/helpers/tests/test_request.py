from pytest import raises

from helpers import request


##############################
# "boolean string" conversions
##############################
def test_converting_string_representationss_for_false():
    for rep in ('FALSE', 'fALsE', 'false'):
        assert request.boolean_string(rep) == False


def test_converting_string_representationss_for_true():
    for rep in ('TRUE', 'TrUe', 'true'):
        assert request.boolean_string(rep) == True


def test_converting_invalid_string_representation_fails():
    with raises(ValueError):
        request.boolean_string('not_convertible')


########################################
# Retrieving mandatory typed value lists
########################################
def test_retrieving_mandatory_valid_typed_list_succeeds(mocker):
    value_list = ('1', '2', '3')
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=value_list)
    assert request.get_mandatory_typed_list(mock_listable, key='key', value_type=int) == [1, 2, 3]


def test_retrieving_mandatory_nonexistant_typed_list_fails(mocker):
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=None)
    with raises(request.exceptions.ValidationError):
        request.get_mandatory_typed_list(mock_listable, key='key', value_type=int)


def test_retrieving_mandatory_incompatible_typed_list_fails(mocker):
    value_list = ('red', 'green', 'blue')
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=value_list)
    with raises(request.exceptions.ValidationError):
        request.get_mandatory_typed_list(mock_listable, key='key', value_type=int)


###################################
# Retrieving mandatory typed values 
###################################
def test_retrieving_mandatory_valid_typed_item_succeeds():
    from_dict = { 'key': '2' }
    assert request.get_mandatory_typed_value(from_dict, key='key', value_type=int) == 2


def test_retrieving_mandatory_nonexistant_typed_value_fails():
    with raises(request.exceptions.ValidationError):
        request.get_mandatory_typed_value({}, key='key', value_type=int)


def test_retrieving_mandatory_incompatible_types_value_fails():
    from_dict = { 'key': 'not_a_number' }
    with raises(request.exceptions.ValidationError):
        request.get_mandatory_typed_value(from_dict, key='key', value_type=int)


#######################################
# Retrieving optional typed value lists
#######################################
def test_retrieving_optional_valid_typed_list_succeeds(mocker):
    value_list = ('1', '2', '3')
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=value_list)
    assert request.get_optional_typed_list(mock_listable, key='key', value_type=int) == [1, 2, 3]


def test_retrieving_optional_nonexistant_typed_list_fails(mocker):
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=None)
    assert request.get_optional_typed_list(mock_listable, key='key', value_type=int) is None


def test_retrieving_optional_incompatible_typed_list_fails(mocker):
    value_list = ('red', 'green', 'blue')
    mock_listable = mocker.MagicMock()
    mock_listable.getlist = mocker.MagicMock(return_value=value_list)
    with raises(request.exceptions.ValidationError):
        request.get_optional_typed_list(mock_listable, key='key', value_type=int)


##################################
# Retrieving optional typed values
##################################
def test_retrieving_optional_valid_typed_item_succeeds():
    from_dict = { 'key': '2' }
    assert request.get_optional_typed_value(from_dict, key='key', value_type=int) == 2


def test_retrieving_optional_nonexistant_typed_value_succeeds():
    request.get_optional_typed_value({}, key='key', value_type=int) is None


def test_retrieving_optional_incompatible_types_value_fails():
    from_dict = { 'key': 'not_a_number' }
    with raises(request.exceptions.ValidationError):
        request.get_optional_typed_value(from_dict, key='key', value_type=int)
