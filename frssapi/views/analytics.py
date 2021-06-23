from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class AnalyticsView(ViewSet):

    def list(self, request):
        """Handle GET requests to answers resource
        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user

        # Budget & Protection
        # Subtract Users totalAssets from totalLiabilities
        liabilities = user.answers_set.filter(question__id__in=[7, 8])
        totalLiabilities = liabilities[1].input_answer - \
            liabilities[0].input_answer

        # Add Users total income with any additional income to provide a totalAssets
        assets = user.answers_set.filter(question__id__in=[4, 5])
        totalAnnualIncome = assets[1].input_answer+assets[0].input_answer

        # Users monthly income
        income = user.answers_set.filter(question__id__in=[4])
        monthlyIncome = round(income[0].input_answer/12, 2)

        # Monthly Bills
        livingExpenses = user.answers_set.get(question__id=10).input_answer
        monthlyDebts = user.answers_set.get(question__id=9).input_answer
        totalMonthlyBills = livingExpenses + monthlyDebts

        # Retirement Data
        retirementSavings = user.answers_set.get(question__id=25).input_answer
        monthlyRetirementSavings = user.answers_set.get(question__id=24).input_answer
        lifeExpectancy = user.answers_set.get(question__id=23).input_answer
        retirementAge = user.answers_set.get(question__id=22).input_answer
        yearsRetired = lifeExpectancy - retirementAge

        retirementExpectation = yearsRetired * totalAnnualIncome

        # Data for bar chart
        retirementData = [
            {
                "Financial Contributions": "Actual",
                "traditional IRA": 37000,
                "traditional IRAColor": "hsl(204, 70%, 50%)",
                "Roth IRA": 58000,
                "Roth IRAColor": "hsl(227, 70%, 50%)",
                "Mutual Fund": 114000,
                "Mutual FundColor": "hsl(159, 70%, 50%)",
                "401k": 89000,
                "401kColor": "hsl(320, 70%, 50%)",
                "Stocks/Bonds": 92000,
                "Stocks/BondsColor": "hsl(165, 70%, 50%)",
                "Other": 37000,
                "OtherColor": "hsl(255, 70%, 50%)"
            },
            {
                "Financial Contributions": "Goal",
                "traditional IRA": 100000,
                "traditional IRAColor": "hsl(233, 70%, 50%)",
                "Roth IRA": 100000,
                "Roth IRAColor": "hsl(270, 70%, 50%)",
                "Mutual Fund": 200000,
                "Mutual FundColor": "hsl(319, 70%, 50%)",
                "401k": 150000,
                "401kColor": "hsl(172, 70%, 50%)",
                "Stocks/Bonds": 200000,
                "Stocks/BondsColor": "hsl(160, 70%, 50%)",
                "Other": 250000,
                "OtherColor": "hsl(105, 70%, 50%)"
            }
        ]

        lineData = [
    {
        "id": "Actual",
        "color": "hsl(6, 70%, 50%)",
        "data": [
        {
            "x": "January",
            "y": 60
        },
        {
            "x": "February",
            "y": 266
        },
        {
            "x": "March",
            "y": 9
        },
        {
            "x": "April",
            "y": 212
        },
        {
            "x": "May",
            "y": 105
        },
        {
            "x": "June",
            "y": 21
        },
        {
            "x": "July",
            "y": 212
        },
        {
            "x": "August",
            "y": 212
        },
        {
            "x": "September",
            "y": 154
        },
        {
            "x": "October",
            "y": 128
        },
        {
            "x": "November",
            "y": 34
        },
        {
            "x": "December",
            "y": 156
        }
        ]
    },
    {
        "id": "Goal",
        "color": "hsl(340, 70%, 50%)",
        "data": [
        {
            "x": "January",
            "y": 250
        },
        {
            "x": "February",
            "y": 250
        },
        {
            "x": "March",
            "y": 250
        },
        {
            "x": "April",
            "y": 250
        },
        {
            "x": "May",
            "y": 250
        },
        {
            "x": "June",
            "y": 250
        },
        {
            "x": "July",
            "y": 250
        },
        {
            "x": "August",
            "y": 250
        },
        {
            "x": "September",
            "y": 250
        },
        {
            "x": "October",
            "y": 250
        },
        {
            "x": "November",
            "y": 250
        },
        {
            "x": "December",
            "y": 250
        }
        ]
    }
    ]

        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "retirementAnalysis": {
                "retirementExpectation": retirementExpectation,
                "retirementSavings": retirementSavings
            },
            "incomeAnalysis": {
                "monthlyIncome": monthlyIncome,
                "totalMonthlyBills": totalMonthlyBills
            },
            "retirementData": retirementData,
            "lineData": lineData
        }
        # Send the object to the client
        return Response(analysis)
