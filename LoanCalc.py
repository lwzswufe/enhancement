# author='lwz'
# coding:utf-8
# 贷款计算器


class Cash_Flow(object):
    def __init__(self, ed_month, rate, amount, interval, sign_, st_month=0):
        self.ed_month = ed_month
        self.rate = rate
        self.amount = amount
        self.interval = interval
        self.surplus = amount
        self.sign = sign_
        self.st_month = st_month

    def get_repayment(self):
        repay_list = list()
        for i in range(self.st_month, self.ed_month):
            repay = self.surplus * self.rate / 12
            if (i + 1) % self.interval == 0:
                repay += self.amount * self.interval / self.ed_month
            repay_list.append(self.sign * repay)
        return repay_list


def sum_cash_flow(cash_flow_list):
    f = open("D:\\cash_flow.csv", "w")
    max_month = 0
    for cf in cash_flow_list:
        max_month = max(max_month, len(cf))

    sum_count = 0
    year_count = 0
    for m in range(max_month):
        this_term_cash = 0
        print("{}, ".format(m + 1), end="", file=f)
        for cf in cash_flow_list:
            if m < len(cf):
                c = cf[m]
            else:
                c = 0
            print("{:.4f}w, ".format(c), end="", file=f)
            this_term_cash += c
        print("{:.4f}w, ".format(this_term_cash), end="", file=f)
        sum_count += this_term_cash
        year_count += this_term_cash
        print("{:.4f}w, {:.4f}w".format(year_count, sum_count), file=f)
        if (m + 1) % 12 == 0:
            year_count = 0
    f.close()


def main():
    year = 20
    price = 107
    cash_1 = Cash_Flow(year*12, 0.049, price * 0.7, 1, -1).get_repayment()       # 贷款
    cash_2 = Cash_Flow(36,  0.066, 21, 6, -1).get_repayment()                # 消费贷
    cash_3 = Cash_Flow(18,  0.000, 8, 12, -1, 8).get_repayment()             # 学费
    cash_4 = Cash_Flow(year*12, 0.000, 8*20, 12, +1, 8).get_repayment()             # 年终
    cash_5 = Cash_Flow(year*12, 0.000, 3.775*20, 12, +1, 1).get_repayment()         # 公积金
    cf_list = [cash_1, cash_2, cash_3, cash_4, cash_5]
    sum_cash_flow(cf_list)


if __name__ == "__main__":
    main()