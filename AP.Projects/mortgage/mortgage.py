def find_payment(loan, r, m):
    return loan * ((r * (1 + r) ** m) / ((1 + r) ** m - 1))

class Mortgage(object):
    def __init__(self, loan, ann_rate, months):
        self._loan = loan
        self._rate = ann_rate / 12
        self._months = months
        self._paid = [0.0]
        self._outstanding = [loan]
        self._payment = find_payment(loan, self._rate, months)
        self._legend = None

    def make_payment(self):
        self._paid.append(self._payment)
        reduction = self._payment - self._outstanding[-1] * self._rate
        self._outstanding.append(self._outstanding[-1] - reduction)
    
    def get_total_paid(self):
        return sum(self._paid)

    def __str__(self):
        return f'{self._legend}'
    
class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self._legend = f'Fixed, {r*100:.1f}%'

class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts): 
        Mortgage.__init__(self, loan, r, months)
        self._pts = pts
        self._paid = [loan * (pts / 100)]
        self._legend = f'Fixed, {r * 100: .1f} %, {pts} points'

class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaser_rate, teaser_months):
        Mortgage.__init__(self, loan, teaser_rate, months)
        self._teaser_months = teaser_months
        self._teaser_rate = teaser_rate 
        self._nextRate = r / 12
        self._legend = (f' {100 * teaser_rate:.1f}% for ' + f'{self._teaser_months} months, then {100 * r:.1f}%')

    def make_payment (self):
        if len(self._paid) == self._teaser_months + 1: 
            self._rate= self._nextRate
            self._payment = find_payment(self._outstanding[-1], self._rate, self._months - self._teaser_months)
        Mortgage.make_payment(self)

def compare_mortgages (amt, years, fixed_rate, pts, pts_rate, var_rate1, var_rate2, var_months):
    tot_months = years * 12 
    fixed1 = Fixed(amt, fixed_rate, tot_months)
    fixed2 = FixedWithPts(amt, pts_rate, tot_months, pts) 
    two_rate = TwoRate(amt, var_rate2, tot_months, var_rate1, var_months) 
    morts = [fixed1, fixed2, two_rate]
    for m in range(tot_months):
        for mort in morts:
            mort.make_payment()
    for m in morts: 
        print(m)
        print(f' Total payments = ${m.get_total_paid():,.0f}')

compare_mortgages(amt=200000, years=30, fixed_rate=0.035, pts = 2, pts_rate=0.03, var_rate1=0.03, var_rate2=0.05, var_months=60)