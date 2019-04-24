from django import forms

class formName(forms.Form):
    OPTIONS1 = (
            (1, "Someone who stays away from risk"),
            (2, "Very risk avoiding"),
            (3, "Cautious"),
            (4, "Willing to take calculated risk"),
            (5, "Very risk taking"),
            (6, "Extremely risk taking"),
            )
    OPTIONS2 = (
            (1, "1% chance of winning Rs 200,000"),
            (2, "5% chance of winning Rs 100,000"),
            (3, "25% chance of winning Rs 20,000"),
            (4, "50% chance of winning Rs 10,000"),
            (5, "75% chance of winning Rs 5,000"),
            (6, "90% chance of winning Rs 1,000"),
            )
    OPTIONS3 = (
            (1, "Thrill"),
            (2, "Opportunity"),
            (3, "Nothing"),
            (4, "Uncertainty"),
            (5, "Avoid"),
            (6, "Loss"),
            )

    OPTIONS4 = (
            (1, "I would like to gamble all my money and hope for best case scenario"),
            (2, "Rs 4500 gain best case; Rs 2500 loss worst case"),
            (3, "Rs 2600 gain best case; Rs 800 loss worst case"),
            (4, "Rs 800 gain best case; Rs 200 loss worst case"),
            (5, "Rs 200 gain best case; Rs 0 loss worst case"),
            (6, "I would not like to do anything"),
            )
    OPTIONS5 = (
            (1, "10% chance to gain Rs 10,000 and 90% chance to gain nothing"),
            (2, "25% chance to gain Rs 5,000 and 75% chance to gain nothing"),
            (3, "50% chance to gain Rs 2,000 and 50% chance to gain nothing"),
            (4, "90% chance to gain Rs 1,000 and 10% chance to gain nothing"),
            (5, "A sure gain of Rs 500"),
            (6, "I would do nothing and stick with the money I have"),
            )
    OPTIONS6 = (
            (1, "Sell the bonds, put all your money in real assets and borrow more money to buy even more real assets"),
            (2, "Sell the bonds and put all your money in real assets"),
            (3, "Keep half the money in both bonds and half in other real assets"),
            (4, "Hold the bonds"),
            (5, "I would like to liquidate my position and keep cash"),
            (6, "I would not like to invest in a volatile market in the first place"),
            )
    OPTIONS7 = (
            (1, "I would not even consider doing a job. I think business is most preferable form of earning"),
            (2, "I would like to quit now and start a business"),
            (3, "High likely"),
            (4, "Likely, but in the future"),
            (5, "Highly unlikely"),
            (6, "I would not even think of doing a job as I think that a job is the most secure"),
            )
    OPTIONS8 = (
            (1, "I would like to start a similar business myself"),
            (2, "All the money I have"),
            (3, "6 month's salary"),
            (4, "3 month's salary"),
            (5, "1 month's salary"),
            (6, "Nothing"),
            )
    name1 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func1(this.id);'}), required=True, choices=OPTIONS1)
    name2 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func2(this.id);'}), required=True, choices=OPTIONS2)
    name3 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func3(this.id);'}), required=True, choices=OPTIONS3)
    name4 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func4(this.id);'}), required=True, choices=OPTIONS4)
    name5 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func5(this.id);'}), required=True, choices=OPTIONS5)
    name6 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func6(this.id);'}), required=True, choices=OPTIONS6)
    name7 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func7(this.id);'}), required=True, choices=OPTIONS7)
    name8 = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick':'func8(this.id);'}), required=True, choices=OPTIONS8)
    name9 = forms.CharField(required=True)
