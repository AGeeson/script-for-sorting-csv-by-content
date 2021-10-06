import output_no_rests
# from freezegun import freeze_time


def test_call_outcome_conditional():
    df = {'Call Outcome': ["Callback", "Hung up"]}
    assert output_no_rests.no_rest_because_call_outcome(
        df, 0) == True, "true output from calloutcome test"
    assert output_no_rests.no_rest_because_call_outcome(
        df, 1) == False, "false output from calloutcome test"

# library import was having issues
# @freeze_time("2021-01-20")


def test_is_lead_in_window():
    df = {'Call Outcome': ['Hung up', 'Not Interested'],
          'Call Datetime': ["01/01/2021 13:37:00", "01/10/2021 13:37:00"]}
    assert output_no_rests.is_lead_in_window(df, 0) == True
    assert output_no_rests.is_lead_in_window(df, 1) == False
