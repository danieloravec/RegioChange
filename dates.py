import datetime


class Dates:

    @staticmethod
    def remove_day_month_zeros(readable_date):
        if readable_date[3] == '0':
            readable_date = readable_date[0:3] + readable_date[4:len(readable_date)]
        if readable_date[0] == '0':
            readable_date = readable_date[1:len(readable_date)]
        return readable_date

    def add_one_day(self, date, readable):
        day = int(date[6:8])
        month = int(date[4:6])
        year = int(date[0:4])
        date = datetime.datetime(year, month, day, 0, 0, 0)
        date += datetime.timedelta(days=1)
        date = str(date)
        if readable:
            date = date[8:10] + '.' + date[5:7] + '.' + date[0:4]
            date = self.remove_day_month_zeros(date)
        else:
            date = date[0:4] + date[5:7] + date[8:10]
        return date
