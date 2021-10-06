import os
import datetime
import csv
import pandas
import datetime
import dateutil
import argparse


def no_rest_because_call_outcome(df, ind):
    df["Call Outcome"][ind]
    # may want to capture typos/missing capitalisation here
    # if df["Call Outcome"][ind] in ["Engaged", "Callback", "Decision maker unavailable"]:
    #     return True
    # else:
    #     False
    return True if df["Call Outcome"][ind] in ["Engaged",
                                               "Callback",
                                               "Decision maker unavailable"
                                               ] else False


def is_lead_in_window(df, ind):
    call_outcome = {"Hung up": 6, "Not Interested": 3}
    index_call_outcome = df["Call Outcome"][ind]
    print(index_call_outcome)

    if index_call_outcome in call_outcome.keys():

        last_call_date = datetime.datetime.strptime(
            df["Call Datetime"][ind], "%d/%m/%Y %H:%M:%S")
        print(last_call_date)
        delta = dateutil.relativedelta.relativedelta(
            months=call_outcome[index_call_outcome])

        callback_date = last_call_date + delta
        # doesn't account for callbacks that would be witin the period of the month
        return True if callback_date < datetime.datetime.now() else False
    else:
        return False


def check_string_contains_csv(string):
    print(string[-4:])
    if string[-4:] == ".csv":
        return True


def create_leads_df(directory):
    no_rest_conditionals = [is_lead_in_window, no_rest_because_call_outcome]
    no_rest_ids = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if not check_string_contains_csv(file):
                print("I'm not a csv!")
                continue
            print("I'm a csv!")
            filepath = subdir + os.sep + file
            print(str(file))
            df = pandas.read_csv(filepath)
            for ind in df.index:
                for conditional in no_rest_conditionals:
                    print(conditional)
                    if conditional(df, ind) and df["Lead ID"][ind] not in no_rest_ids:
                        no_rest_ids.append(df["Lead ID"][ind])
                        print("Gotcha!")
                        break
                    print("conditional_was_false !")
    output_df = pandas.DataFrame({"Lead IDs": no_rest_ids})
    return output_df


def main(client, directory):
    df = create_leads_df(directory)
    df.to_csv(f"{client}-{str(datetime.datetime.now())}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # defaults to todays date if no argument is passed in for billing_window_start_date
    # parser.add_argument(
    #     "--date-to-return-to-client",
    #     type=datetime.date.fromisoformat,
    #     default=str(datetime.date.today()),
    # )
    parser.add_argument(
        "--directory",
        type=str,
        default=None,
    )
    parser.add_argument("--client", default=None)
    parser.add_argument("--dry-run", default=False, action="store_true")
    args = parser.parse_args()
    main(
        args.client,
        args.directory,
    )
