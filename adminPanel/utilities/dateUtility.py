import calendar
import datetime
# from datetime import datetime

DAYS_DICT = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}


def calculate_next_date(next_date, frequency, days):
    """
    To calculate the correct next delivery date in case the next date does not match
    with the values of days provided as delivery days options
    :return: the correct next delivery date
    """
    delivery_days = days
    next_date = datetime.datetime.strptime(next_date, "%Y-%m-%d")

    # weekday = the day of the next_date; day_num = the number for day assigned in python;
    week_day = calendar.day_name[next_date.weekday()]
    day_num = next_date.weekday()

    # print "Entered Dates: ", next_date, week_day, next_date.weekday(), frequency, delivery_days
    # if frequency == "Twice Weekly":
    #     delivery_days = ["Wednesday", "Friday"]
    # else:
    #     delivery_days = ["Monday", "Thursday", "Friday"]

    if week_day in delivery_days:
        print "Correct date for day"
    else:
        print "Incorrect date for day"
        day1 = DAYS_DICT[delivery_days[0]]
        day2 = 0
        day3 = 0
        if frequency == "Twice Weekly":
            day2 = DAYS_DICT[delivery_days[1]]
        if frequency == "Thrice Weekly":
            day3 = DAYS_DICT[delivery_days[2]]

        # check for days difference- Cases can be both are positive or both negative or one positive-one negative
        if frequency == "Weekly":
            if day1 - day_num > 0:
                # When next_date is Friday and day1 is for Sunday.
                next_date = next_date + datetime.timedelta(days=day1 - day_num)
            elif day1 - day_num < 0:
                # When next_date is Sunday but day1 is for Friday.
                next_date = next_date + datetime.timedelta(days=(day1 - day_num) + 7)

        if frequency == "Twice Weekly":
            # When delivery_days are Saturday and Sunday and day for next_date is Thursday.
            if day1 - day_num > 0 and day2 - day_num > 0:
                if (day1 - day_num) > (day2 - day_num):
                    # day2 is the closest day, change next date to date of day2
                    next_date = next_date + datetime.timedelta(days=day2 - day_num)
                else:
                    # day1 is the closest day, change next date to date of day1
                    next_date = next_date + datetime.timedelta(days=day1 - day_num)

            # When delivery_days are Monday and Wednesday and day for next_date is Thursday.
            elif day1 - day_num < 0 and day2 - day_num < 0:
                if abs(day1 - day_num) > abs(day2 - day_num):
                    # day1 is the closest day, change next date to date of day1
                    next_date = next_date + datetime.timedelta(days=(day1 - day_num)+7)
                else:
                    # day2 is the closest day, change next date to date of day2
                    next_date = next_date + datetime.timedelta(days=(day2 - day_num)+7)

            # When delivery_days are Monday and Saturday and day for next_date is Thursday.
            else:
                if day1 - day_num > 0:
                    # day1 is closest, change next date to date of day1
                    next_date = next_date + datetime.timedelta(days=day1 - day_num)
                else:
                    # day2 is closest, change next date to date of day2
                    next_date = next_date + datetime.timedelta(days=day2 - day_num)

        elif frequency == "Thrice Weekly":
            if day1 - day_num > 0 and day2 - day_num > 0 and day3 - day_num > 0:
                if (day1 - day_num) < ((day2 - day_num) and (day3 - day_num)):
                    # day1 is the closest day, change next date to date of day1
                    next_date = next_date + datetime.timedelta(days=day1 - day_num)
                elif (day2 - day_num) < ((day1 - day_num) and (day3 - day_num)):
                    # day2 is the closest day, change next date to date of day2
                    next_date = next_date + datetime.timedelta(days=day2 - day_num)
                elif (day3 - day_num) < ((day1 - day_num) and (day2 - day_num)):
                    # day3 is the closest day, change next date to date of day3
                    next_date = next_date + datetime.timedelta(days=day3 - day_num)

            elif day1 - day_num < 0 and day2 - day_num < 0 and day3 - day_num < 0:
                if abs(day1 - day_num) > (abs(day2 - day_num) and abs(day3 - day_num)):
                    # day1 is the closest day, change next date to date of day1
                    next_date = next_date + datetime.timedelta(days=(day1 - day_num) + 7)
                elif abs(day2 - day_num) > (abs(day1 - day_num) and abs(day3 - day_num)):
                    # day2 is the closest day, change next date to date of day2
                    next_date = next_date + datetime.timedelta(days=(day2 - day_num) + 7)
                elif abs(day3 - day_num) > (abs(day1 - day_num) and abs(day2 - day_num)):
                    # day3 is the closest day, change next date to date of day3
                    next_date = next_date + datetime.timedelta(days=(day3 - day_num) + 7)

            else:
                if day1 - day_num > 0:
                    if day2 - day_num > 0:
                        if (day1 - day_num) < (day2 - day_num):
                            # day1 is closest, change next date to date of day1
                            next_date = next_date + datetime.timedelta(days=day1 - day_num)
                        else:
                            # day2 is closest, change next date to date of day2
                            next_date = next_date + datetime.timedelta(days=day2 - day_num)
                    elif day3 - day_num > 0:
                        if (day1 - day_num) < (day3 - day_num):
                            # day1 is closest, change next date to date of day1
                            next_date = next_date + datetime.timedelta(days=day1 - day_num)
                        else:
                            # day3 is closest, change next date to date of day3
                            next_date = next_date + datetime.timedelta(days=day3 - day_num)
                    else:
                        # day1 is closest, change next date to date of day1
                        next_date = next_date + datetime.timedelta(days=day1 - day_num)

                elif day2 - day_num > 0:
                    if day1 - day_num > 0:
                        if (day1 - day_num) < (day2 - day_num):
                            # day1 is closest, change next date to date of day1
                            next_date = next_date + datetime.timedelta(days=day1 - day_num)
                        else:
                            # day2 is closest, change next date to date of day2
                            next_date = next_date + datetime.timedelta(days=day2 - day_num)
                    elif day3 - day_num > 0:
                        if (day2 - day_num) < (day3 - day_num):
                            # day2 is closest, change next date to date of day2
                            next_date = next_date + datetime.timedelta(days=day2 - day_num)
                        else:
                            # day3 is closest, change next date to date of day3
                            next_date = next_date + datetime.timedelta(days=day3 - day_num)
                    else:
                        # day2 is closest, change next date to date of day2
                        next_date = next_date + datetime.timedelta(days=day2 - day_num)

                elif day3 - day_num > 0:
                    if day1 - day_num > 0:
                        if (day1 - day_num) < (day3 - day_num):
                            # day1 is closest, change next date to date of day1
                            next_date = next_date + datetime.timedelta(days=day1 - day_num)
                        else:
                            # day3 is closest, change next date to date of day3
                            next_date = next_date + datetime.timedelta(days=day3 - day_num)
                    elif day2 - day_num > 0:
                        if (day2 - day_num) < (day3 - day_num):
                            # day2 is closest, change next date to date of day2
                            next_date = next_date + datetime.timedelta(days=day2 - day_num)
                        else:
                            # day3 is closest, change next date to date of day3
                            next_date = next_date + datetime.timedelta(days=day3 - day_num)
                    else:
                        # day3 is closest, change next date to date of day3
                        next_date = next_date + datetime.timedelta(days=day3 - day_num)

    print "Next date {}".format(next_date.strftime("%Y-%m-%d"))
    return next_date.strftime("%Y-%m-%d")


def calculate_hold_dates(next_date, frequency, day):
    DAILY_BUFFER = 3
    FORTNIGHT_BUFFER = 4
    MONTHLY_BUFFER = 7
    WEEKLY_BUFFER = 3
    TWICE_WEEKLY_BUFFER = 3
    THRICE_WEEKLY_BUFFER = 3

    current_date = datetime.datetime.now().date()
    hold_dates_list = list()

    if frequency == "Daily":
        for i in range(10):
            hold_dates_list.append(next_date + datetime.timedelta(days=i+DAILY_BUFFER))
        print hold_dates_list
        return hold_dates_list

    elif frequency == "Fortnight":
        date_diff = abs((next_date-current_date).days)
        hold_date = next_date
        if date_diff <= FORTNIGHT_BUFFER:
            for i in range(10):
                hold_date = hold_date + datetime.timedelta(days=15)
                hold_dates_list.append(hold_date)
        else:
            for i in range(9):
                hold_dates_list.append(hold_date)
                hold_date = hold_date + datetime.timedelta(days=15)
            hold_dates_list.append(hold_date)

        print hold_dates_list
        return hold_dates_list

    elif frequency == "Monthly":
        date_diff = abs((next_date - current_date).days)
        hold_date = next_date
        print hold_date, hold_date.month

        if date_diff <= MONTHLY_BUFFER:
            for i in range(10):
                if hold_date.month == 12:
                    hold_date = hold_date.replace(year=hold_date.year+1, month=1)
                    hold_dates_list.append(hold_date)
                else:
                    hold_date = hold_date.replace(month=hold_date.month+1)
                    hold_dates_list.append(hold_date)
        else:
            for i in range(9):
                if hold_date.month == 12:
                    hold_date = hold_date.replace(year=hold_date.year+1, month=1)
                    hold_dates_list.append(hold_date)
                else:
                    hold_dates_list.append(hold_date)
                    hold_date = hold_date.replace(month=hold_date.month + 1)

            hold_dates_list.append(hold_date)

        print hold_dates_list
        return hold_dates_list

    elif frequency == "Weekly":
        date_diff = abs((next_date - current_date).days)
        hold_date = next_date
        week_day = calendar.day_name[hold_date.weekday()]

        if date_diff <= WEEKLY_BUFFER:
            for i in range(10):
                hold_date = hold_date + datetime.timedelta(days=7)
                hold_dates_list.append(hold_date)
        else:
            for i in range(9):
                hold_dates_list.append(hold_date)
                hold_date = hold_date + datetime.timedelta(days=7)
            hold_dates_list.append(hold_date)

        print hold_dates_list
        return hold_dates_list

    elif frequency == "Twice Weekly":
        # print next_date, day
        all_hold_dates_list = twice_weekly_hold_dates(next_date, day)
        index = 0
        for hold_date in all_hold_dates_list:
            if (hold_date - current_date).days > TWICE_WEEKLY_BUFFER:
                index = all_hold_dates_list.index(hold_date)
                break
        hold_dates_list = all_hold_dates_list[index:index+10]

        print hold_dates_list
        return hold_dates_list

    elif frequency == "Thrice Weekly":
        # print next_date, day
        all_hold_dates_list = thrice_weekly_hold_dates(next_date, day)
        index = 0
        for hold_date in all_hold_dates_list:
            if (hold_date - current_date).days > THRICE_WEEKLY_BUFFER:
                index = all_hold_dates_list.index(hold_date)
                break
        hold_dates_list = all_hold_dates_list[index:index + 10]

        print hold_dates_list
        return hold_dates_list


def twice_weekly_hold_dates(next_date, delivery_days):
    """It is assumed that next date is correct and the day on next date is in delivery_days list"""

    hold_dates = []
    # next_date = datetime.datetime.now().date() + datetime.timedelta(days=3)
    week_day = calendar.day_name[next_date.weekday()]
    print next_date, week_day, next_date.weekday()

    # delivery_days = ["Thursday", "Friday"]
    day1, day2 = DAYS_DICT[delivery_days[0]], DAYS_DICT[delivery_days[1]]
    print "days are: ", day1, day2

    # calculate next 7 days for the next_date.
    hold_date = next_date
    for i in range(7):
        hold_date = hold_date + datetime.timedelta(days=7)
        hold_dates.append(hold_date)

    # Find other day number
    if delivery_days.index(week_day) == 0:
        other_day = day2
    else:
        other_day = day1
    print "other day is: ", other_day

    # calculate the next date
    days_ahead = int(other_day) - int(next_date.weekday())
    print "days ahead: ", days_ahead
    hold_date = next_date
    if days_ahead > 0:
        hold_date = hold_date + datetime.timedelta(days=days_ahead)
        hold_dates.append(hold_date)
    else:
        hold_date = hold_date + datetime.timedelta(days=days_ahead+7)
        hold_dates.append(hold_date)
    # append next dates
    for i in range(6):
        hold_date = hold_date + datetime.timedelta(days=6)
        hold_dates.append(hold_date)
    # sort the list
    hold_dates.sort()
    return hold_dates


def thrice_weekly_hold_dates(next_date, delivery_days):
    """It is assumed that next date is correct and the day on next date is in delivery_days list"""
    DAYS_DICT = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

    hold_dates = []
    # next_date = datetime.datetime.now().date() + datetime.timedelta(days=0)
    week_day = calendar.day_name[next_date.weekday()]
    print next_date, week_day, next_date.weekday()

    # delivery_days = ["Monday", "Friday", "Tuesday"]
    day1, day2, day3 = DAYS_DICT[delivery_days[0]], DAYS_DICT[delivery_days[1]], DAYS_DICT[delivery_days[2]]
    print "days are: ", day1, day2, day3

    hold_date = next_date
    for i in range(3):
        hold_date = hold_date + datetime.timedelta(days=7)
        hold_dates.append(hold_date)

    # Find other day number
    if delivery_days.index(week_day) == 0:
        other_days = [day2, day3]
    elif delivery_days.index(week_day) == 1:
        other_days = [day1, day3]
    else:
        other_days = [day1, day2]
    print "other day is: ", other_days

    for other_day in other_days:
        # calculate the next date
        days_ahead = int(other_day) - int(next_date.weekday())
        print "days ahead: ", days_ahead
        hold_date = next_date
        if days_ahead > 0:
            hold_date = hold_date + datetime.timedelta(days=days_ahead)
            hold_dates.append(hold_date)
        else:
            days_ahead += 7
            hold_date = hold_date + datetime.timedelta(days=days_ahead)
            hold_dates.append(hold_date)
        # append next dates
        for i in range(3):
            hold_date = hold_date + datetime.timedelta(days=7)
            hold_dates.append(hold_date)
    # sort the list
    hold_dates.sort()
    return hold_dates
